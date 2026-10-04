"""
Basic LLM vs RAG Comparison
---------------------------
Compares answers from:
1. Basic LLM - answers without college document context
2. RAG - retrieves relevant college documents before answering
"""

from pathlib import Path

from src.llm import get_llm
from src.rag import retrieve_documents_with_scores
from src.prompts import ACADEMIC_QA_PROMPT


# ---------------------------------------------------------
# TEST QUESTIONS
# ---------------------------------------------------------

TEST_QUESTIONS = [
    "What is the minimum attendance requirement?",
    "What are the weekly meeting requirements for the 8th semester project?",
    "What is the college hostel curfew time?",
]


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def get_response_text(response):
    """Safely extract text from a LangChain response."""
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            item.get("text", str(item))
            if isinstance(item, dict)
            else str(item)
            for item in content
        )

    return str(content)


def build_rag_context(documents):
    """Build context from retrieved documents."""
    context_parts = []

    for i, document in enumerate(documents, start=1):
        source = document.metadata.get("source_file", "Unknown")
        page = document.metadata.get("page")

        if page is not None:
            page += 1

        location = source

        if page is not None:
            location += f", page {page}"

        context_parts.append(
            f"[Source {i}: {location}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


# ---------------------------------------------------------
# BASIC LLM
# ---------------------------------------------------------

def basic_llm_answer(llm, question):
    """
    Ask the LLM directly without retrieving college documents.
    """

    prompt = f"""
You are a college academic assistant.

Answer the following question using only your general language-model
knowledge.

Do NOT claim that you checked college documents.

Question:
{question}
"""

    response = llm.invoke(prompt)

    return get_response_text(response)


# ---------------------------------------------------------
# RAG
# ---------------------------------------------------------

def rag_answer(llm, question):
    """
    Retrieve college documents and answer using the RAG prompt.
    """

    documents_with_scores = retrieve_documents_with_scores(
        question,
        k=5,
    )

    documents = [
        document
        for document, score in documents_with_scores
        if score <= 1.2
    ]

    if not documents:
        return (
            "No sufficiently relevant college document was found "
            "for this question."
        ), documents_with_scores

    context = build_rag_context(documents)

    prompt = ACADEMIC_QA_PROMPT.format(
        context=context,
        question=question,
    )

    response = llm.invoke(prompt)

    return get_response_text(response), documents_with_scores


# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------

def save_results(results):
    """Save comparison results to Markdown."""

    output_path = Path("evaluation/basic_vs_rag_results.md")

    lines = []

    lines.append("# Basic LLM vs RAG Comparison")
    lines.append("")
    lines.append(
        "This evaluation compares a basic LLM response with a "
        "Retrieval-Augmented Generation (RAG) response."
    )
    lines.append("")

    for index, result in enumerate(results, start=1):

        lines.append(f"## Test {index}")
        lines.append("")
        lines.append(f"**Question:** {result['question']}")
        lines.append("")

        lines.append("### Basic LLM")
        lines.append("")
        lines.append(result["basic"])
        lines.append("")

        lines.append("### RAG")
        lines.append("")
        lines.append(result["rag"])
        lines.append("")

        lines.append("### Retrieved Sources")
        lines.append("")

        if result["sources"]:

            for source, score in result["sources"]:

                filename = source.metadata.get(
                    "source_file",
                    "Unknown",
                )

                page = source.metadata.get("page")

                if page is not None:
                    page += 1

                if page is not None:
                    location = f"{filename}, page {page}"
                else:
                    location = filename

                lines.append(
                    f"- {location} "
                    f"(distance: {score:.4f})"
                )

        else:
            lines.append("- No sources retrieved.")

        lines.append("")

        lines.append("---")
        lines.append("")

    lines.append("## Overall Observation")
    lines.append("")
    lines.append(
        "The basic LLM answers using its general language knowledge "
        "without access to the college knowledge base."
    )
    lines.append("")
    lines.append(
        "The RAG system first retrieves relevant college documents "
        "and then generates an answer using that retrieved context."
    )
    lines.append("")
    lines.append(
        "For college-specific questions, RAG is expected to provide "
        "answers grounded in the uploaded institutional documents, "
        "while questions outside the knowledge base should be "
        "identified as unsupported rather than answered with "
        "invented college-specific information."
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output_path


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("BASIC LLM vs RAG COMPARISON")
    print("=" * 60)

    print("\nLoading Gemini LLM...")
    llm = get_llm()

    results = []

    for number, question in enumerate(TEST_QUESTIONS, start=1):

        print("\n" + "-" * 60)
        print(f"TEST {number}")
        print("-" * 60)

        print(f"Question: {question}")

        print("\nRunning Basic LLM...")
        basic_answer = basic_llm_answer(
            llm,
            question,
        )

        print("Basic LLM response received.")

        print("\nRunning RAG...")
        rag_answer_text, sources = rag_answer(
            llm,
            question,
        )

        print("RAG response received.")

        results.append(
            {
                "question": question,
                "basic": basic_answer,
                "rag": rag_answer_text,
                "sources": sources,
            }
        )

    output_path = save_results(results)

    print("\n" + "=" * 60)
    print("COMPARISON COMPLETE")
    print("=" * 60)

    print(f"\nResults saved to:")
    print(output_path)

    print("\nYou can open that file to compare the answers.")


if __name__ == "__main__":
    main()
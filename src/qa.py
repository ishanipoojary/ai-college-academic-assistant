from rag import retrieve_documents
from llm import get_llm


def answer_question(question):
    # 1. Retrieve relevant information from ChromaDB
    documents = retrieve_documents(question, k=5)

    # 2. Build context from retrieved documents
    context_parts = []

    for document in documents:
        page = document.metadata.get("page")

        if page is not None:
            page += 1

        context_parts.append(
            f"[Source: Page {page}]\n{document.page_content}"
        )

    context = "\n\n".join(context_parts)

    # 3. Give the retrieved information to Gemini
    prompt = f"""
You are a college academic assistant.

Answer the student's question using ONLY the information
provided in the context below.

If the context does not contain enough information to answer
the question, say:
"I couldn't find this information in the college documents."

Do not invent rules, numbers, dates, or policies.

Always mention the relevant source page(s).

CONTEXT:
{context}

STUDENT QUESTION:
{question}

ANSWER:
"""

    # 4. Generate the answer
    llm = get_llm()
    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":
    question = input("Ask your academic question: ")

    answer = answer_question(question)

    print("\n===== ACADEMIC ASSISTANT =====\n")
    print(answer)
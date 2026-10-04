from langchain_chroma import Chroma
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from src.config import CHROMA_DIR


# ============================================================
# CHROMA EMBEDDING ADAPTER
# ============================================================

class ChromaEmbeddingAdapter:
    """Adapt Chroma's ONNX embedding function for LangChain."""

    def __init__(self):
        self.embedding_function = DefaultEmbeddingFunction()

    def embed_documents(self, texts):
        return self.embedding_function(texts)

    def embed_query(self, text):
        return self.embedding_function([text])[0]


# ============================================================
# VECTOR STORE
# ============================================================

def get_vector_store():
    """Connect to the existing ChromaDB database."""

    embedding_function = ChromaEmbeddingAdapter()

    vector_store = Chroma(
        collection_name="college_academic_documents",
        embedding_function=embedding_function,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_documents(query, k=5):
    """
    Retrieve the most relevant college-document chunks.
    """

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results


# ============================================================
# RELEVANCE CHECK
# ============================================================

def retrieve_documents_with_scores(query, k=5):
    """
    Retrieve documents together with their similarity scores.

    Chroma returns distances where:
        lower distance = more similar
        higher distance = less similar
    """

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    return results


def is_relevant(
    results,
    threshold=1.2
):
    """
    Decide whether the retrieved documents are relevant.

    If the best retrieved document has a distance greater
    than the threshold, treat the question as unknown.

    Lower distance means better similarity.
    """

    if not results:
        return False

    best_distance = results[0][1]

    return best_distance <= threshold


# ============================================================
# SOURCE FORMATTING
# ============================================================

def format_sources(documents):
    """
    Format retrieved documents so they can be shown
    to the user.
    """

    sources = []

    for document in documents:

        page = document.metadata.get("page")

        # PyPDFLoader pages are zero-indexed.
        if page is not None:
            page = page + 1

        sources.append({
            "page": page,
            "source": document.metadata.get(
                "source_file",
                "Unknown"
            ),
            "content": document.page_content,
        })

    return sources


# ============================================================
# UNKNOWN QUESTION TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    results = retrieve_documents_with_scores(
        question,
        k=5
    )

    print("\n===== RETRIEVAL RESULTS =====\n")

    for i, (document, score) in enumerate(
        results,
        start=1
    ):

        page = document.metadata.get("page")

        if page is not None:
            page += 1

        print(
            f"--- Result {i} | "
            f"Page {page} | "
            f"Distance {score:.4f} ---"
        )

        print(
            document.page_content[:500]
        )

        print()

    print(
        "===== RELEVANCE CHECK ====="
    )

    if is_relevant(results):

        print(
            "RELEVANT: "
            "Question appears to be covered "
            "by the college documents."
        )

    else:

        print(
            "UNKNOWN: "
            "Question does not appear to be "
            "covered by the college documents."
        )
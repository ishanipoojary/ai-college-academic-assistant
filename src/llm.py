from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    """Create the Gemini LLM."""

    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
    )


if __name__ == "__main__":
    llm = get_llm()

    response = llm.invoke(
        "Say hello in one short sentence."
    )

    print(response.content)
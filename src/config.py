from pathlib import Path
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Project root folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data folder
DATA_DIR = PROJECT_ROOT / "data"

# Main college PDF
PDF_PATH = DATA_DIR / "14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf"

# ChromaDB storage
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

# Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Embedding model
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Number of documents retrieved for a question
TOP_K = 5

# Chunking configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
import os

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# API CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-20b"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")


# ============================================================
# RAG CONFIGURATION
# ============================================================

CANDIDATE_K = int(
    os.getenv("CANDIDATE_K", "5")
)

FINAL_K = int(
    os.getenv("FINAL_K", "3")
)


# ============================================================
# VALIDATION
# ============================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Add it to the .env file."
    )
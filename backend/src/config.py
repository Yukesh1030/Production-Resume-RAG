import os

from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-20b"
)

API_TOKEN = os.getenv(
    "API_TOKEN"
)


CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]


CANDIDATE_K = int(
    os.getenv(
        "CANDIDATE_K",
        "5"
    )
)


FINAL_K = int(
    os.getenv(
        "FINAL_K",
        "3"
    )
)


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured."
    )


if not API_TOKEN:
    raise ValueError(
        "API_TOKEN is not configured."
    )
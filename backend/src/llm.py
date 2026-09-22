from openai import OpenAI

from src.config import (
    GROQ_API_KEY,
    MODEL_NAME
)


# ============================================================
# GROQ CLIENT
# ============================================================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(prompt: str):

    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": "You are a helpful resume assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1
    )

    return response.choices[0].message.content
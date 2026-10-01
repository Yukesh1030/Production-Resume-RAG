from openai import OpenAI

from src.config import (
    GROQ_API_KEY,
    MODEL_NAME
)

from src.logger import logger


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_answer(prompt: str):
    """
    Generate a complete LLM response.
    """

    logger.info(
        "Sending request to LLM | model=%s | "
        "prompt_characters=%s",
        MODEL_NAME,
        len(prompt)
    )


    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful "
                    "resume assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )


    answer = response.choices[0].message.content


    logger.info(
        "LLM response received | "
        "characters=%s",
        len(answer)
    )


    return answer


def stream_answer(prompt: str):
    """
    Stream the LLM response chunk by chunk.
    """

    logger.info(
        "Opening LLM streaming connection | "
        "model=%s | prompt_characters=%s",
        MODEL_NAME,
        len(prompt)
    )


    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful "
                    "resume assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        stream=True
    )


    for chunk in stream:

        if not chunk.choices:
            continue


        delta = chunk.choices[0].delta


        if delta.content:
            yield delta.content


    logger.info(
        "LLM streaming connection closed"
    )
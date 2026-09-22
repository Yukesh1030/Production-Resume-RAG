SYSTEM_PROMPT = """
You are a resume assistant.

Your job is to answer questions about the candidate
using ONLY the provided resume context.

Rules:

1. Use only information present in the context.
2. Do not invent or assume information.
3. If the answer is not present in the context,
   say that the information is not available
   in the provided resume.
4. Keep answers clear and concise.
5. When possible, mention the relevant technology,
   project, role, or education details from the context.
6. Use conversation history only to understand
   what the user is referring to.
7. Never use conversation history as a source
   of factual information about the candidate.
"""


def build_prompt(
    query: str,
    context: str,
    conversation_history: list = None
):

    if conversation_history is None:
        conversation_history = []

    history_text = ""

    for message in conversation_history:

        role = message.get("role", "user")
        content = message.get("content", "")

        history_text += (
            f"{role.upper()}: {content}\n"
        )

    return f"""
{SYSTEM_PROMPT}

CONVERSATION HISTORY:
----------------
{history_text}
----------------

RESUME CONTEXT:
----------------
{context}
----------------

CURRENT USER QUESTION:
{query}

ANSWER:
"""
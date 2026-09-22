def contextualize_query(
    query: str,
    conversation_history: list = None
) -> str:

    if not conversation_history:
        return query

    recent_messages = conversation_history[-4:]

    history_parts = []

    for message in recent_messages:

        role = message.get(
            "role",
            "user"
        )

        content = message.get(
            "content",
            ""
        )

        if content:
            history_parts.append(
                f"{role}: {content}"
            )

    if not history_parts:
        return query

    history_text = "\n".join(
        history_parts
    )

    return f"""
Previous conversation:
{history_text}

Current question:
{query}
""".strip()
def build_context(results):

    context_parts = []

    for index, result in enumerate(
        results,
        start=1
    ):

        document = result["document"]

        context_parts.append(
            f"""
Document {index}:
{document}
"""
        )

    return "\n".join(context_parts)
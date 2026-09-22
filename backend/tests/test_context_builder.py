from src.context_builder import build_context


results = [

    {
        "id": "resume_chunk_1",
        "document": "Yukesh knows Java and Python.",
        "score": 0.90
    },

    {
        "id": "resume_chunk_2",
        "document": "Yukesh has experience with ReactJS.",
        "score": 0.85
    }

]


context = build_context(results)


print(context)
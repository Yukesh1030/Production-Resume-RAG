from src.rag import ResumeRAG


# Create RAG instance
rag = ResumeRAG()


# ============================================================
# BASIC RAG TESTS
# ============================================================

questions = [
    "What technologies does Yukesh know?",
    "What projects has Yukesh worked on?",
    "What is Yukesh's educational background?",
    "Does Yukesh know ChromaDB?",
    "What is Yukesh's favorite food?"
]


for question in questions:

    print("\n" + "=" * 80)
    print("QUESTION:")
    print(question)
    print("=" * 80)

    response = rag.ask(
        question,
        candidate_k=5,
        final_k=3
    )

    print("\nANSWER:")
    print(response["answer"])

    print("\nSOURCES / RETRIEVED CHUNKS:")

    sources = response["sources"]

    if not sources:
        print("No relevant sources found.")
        continue

    for source in sources:

        print(f"\n- {source['id']}")

        print(
            f"  Source: {source['source']}"
        )

        print(
            f"  Chunk: {source['chunk_index']}"
        )

        score = source.get("score")

        if score is not None:
            print(
                f"  Score: {score:.4f}"
            )


# ============================================================
# CONVERSATION TEST
# ============================================================

print("\n" + "=" * 80)
print("CONVERSATION TEST")
print("=" * 80)


history = []


# ------------------------------------------------------------
# First question
# ------------------------------------------------------------

question_1 = "What technologies does Yukesh know?"


response_1 = rag.ask(
    question_1,
    conversation_history=history
)


print("\nUSER:")
print(question_1)


print("\nAI:")
print(response_1["answer"])


# Add first conversation turn
history.append({
    "role": "user",
    "content": question_1
})


history.append({
    "role": "assistant",
    "content": response_1["answer"]
})


# ------------------------------------------------------------
# Follow-up question
# ------------------------------------------------------------

question_2 = "What about React?"


response_2 = rag.ask(
    question_2,
    conversation_history=history
)


print("\nUSER:")
print(question_2)


print("\nAI:")
print(response_2["answer"])


# Show conversation history
print("\nCONVERSATION HISTORY:")
print("-" * 80)

for message in history:

    print(
        f"{message['role'].upper()}: "
        f"{message['content']}"
    )
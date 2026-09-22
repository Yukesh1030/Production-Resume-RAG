from src.llm import generate_answer


prompt = """
You are a resume assistant.

Use only the following context.

CONTEXT:
Yukesh has experience with ReactJS,
Java, Python and MySQL.

QUESTION:
What programming languages does Yukesh know?
"""


answer = generate_answer(prompt)


print("\nANSWER:")
print(answer)
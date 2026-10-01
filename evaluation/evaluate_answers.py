import sys
import json
import re
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))


# ============================================================
# IMPORT RAG SYSTEM
# ============================================================

from src.rag import ResumeRAG


# ============================================================
# DATASET
# ============================================================

DATASET_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "evaluation_dataset.json"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize generated answers and expected facts
    before comparison.
    """

    text = text.lower()

    # --------------------------------------------------------
    # Normalize Unicode dash / hyphen characters
    # --------------------------------------------------------

    dash_characters = [
        "\u2010",  # Hyphen
        "\u2011",  # Non-breaking hyphen
        "\u2012",  # Figure dash
        "\u2013",  # En dash
        "\u2014",  # Em dash
        "\u2015",  # Horizontal bar
        "\u2212",  # Minus sign
    ]

    for dash in dash_characters:
        text = text.replace(dash, "-")

    # --------------------------------------------------------
    # Normalize non-breaking spaces
    # --------------------------------------------------------

    text = text.replace(
        "\u00a0",
        " "
    )

    # --------------------------------------------------------
    # Remove Markdown formatting
    # --------------------------------------------------------

    text = re.sub(
        r"[*_`]",
        "",
        text
    )

    # --------------------------------------------------------
    # Normalize common wording differences
    # --------------------------------------------------------

    replacements = {
        "bachelor of engineering": "b.e.",
        "over 20": "20+",
        "more than 20": "20+",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new
        )

    # --------------------------------------------------------
    # Normalize educational date ranges
    #
    # Examples:
    # 2020 to 2024
    # 2020 - 2024
    # 2020–2024
    #
    # becomes:
    # 2020-2024
    # --------------------------------------------------------

    text = re.sub(
        r"\b(20\d{2})\s*(?:to|-)\s*(20\d{2})\b",
        r"\1-\2",
        text
    )

    # --------------------------------------------------------
    # Normalize whitespace
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FACT CHECKING
# ============================================================

def fact_present(
    answer: str,
    fact: str
) -> bool:
    """
    Check whether an expected fact appears
    in the generated answer.
    """

    normalized_answer = normalize_text(
        answer
    )

    normalized_fact = normalize_text(
        fact
    )

    return normalized_fact in normalized_answer


# ============================================================
# EVALUATE SINGLE ANSWER
# ============================================================

def evaluate_answer(
    answer: str,
    item: dict
):
    """
    Evaluate one generated answer against
    the expected facts.
    """

    answerable = item.get(
        "answerable",
        True
    )

    required_facts = item.get(
        "required_facts",
        []
    )

    normalized_answer = normalize_text(
        answer
    )

    # ========================================================
    # UNANSWERABLE QUESTION
    # ========================================================

    if not answerable:

        abstention_phrases = [
            "not available",
            "don't have enough",
            "do not have enough",
            "not mentioned",
            "not provided",
            "cannot answer",
            "can't answer",
            "information is not available",
            "information is not provided",
            "information is not present",
            "does not contain any information",
            "doesn't contain any information",
            "not present in the provided resume",
            "not found in the provided resume",
            "resume does not contain",
            "resume doesn't contain",
        ]

        abstained = any(
            phrase in normalized_answer
            for phrase in abstention_phrases
        )

        return {
            "passed": abstained,
            "fact_score": (
                1.0
                if abstained
                else 0.0
            ),
            "matched_facts": [],
            "missing_facts": [],
            "abstained": abstained,
        }

    # ========================================================
    # ANSWERABLE QUESTION
    # ========================================================

    matched_facts = []
    missing_facts = []

    for fact in required_facts:

        if fact_present(
            answer,
            fact
        ):
            matched_facts.append(
                fact
            )
        else:
            missing_facts.append(
                fact
            )

    if required_facts:

        fact_score = (
            len(matched_facts)
            / len(required_facts)
        )

    else:

        fact_score = 1.0

    passed = (
        len(missing_facts) == 0
    )

    return {
        "passed": passed,
        "fact_score": fact_score,
        "matched_facts": matched_facts,
        "missing_facts": missing_facts,
        "abstained": False,
    }


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print("=" * 80)
    print(
        "PRODUCTION RESUME RAG - ANSWER EVALUATION"
    )
    print("=" * 80)

    dataset = load_dataset()

    print(
        f"\nLoaded {len(dataset)} "
        f"evaluation questions."
    )

    rag = ResumeRAG()

    total_questions = len(dataset)
    passed_questions = 0
    total_fact_score = 0.0

    results = []

    # ========================================================
    # RUN EACH QUESTION
    # ========================================================

    for index, item in enumerate(
        dataset,
        start=1
    ):

        question_id = item["id"]
        question = item["question"]

        print(
            "\n" + "=" * 80
        )

        print(
            f"QUESTION {index}/{total_questions}"
        )

        print(
            f"ID: {question_id}"
        )

        print(
            f"QUESTION: {question}"
        )

        print(
            "=" * 80
        )

        try:

            # ------------------------------------------------
            # Run RAG
            # ------------------------------------------------

            result = rag.ask(
                question,
                candidate_k=10,
                final_k=6
            )

            answer = result.get(
                "answer",
                ""
            )

            sources = result.get(
                "sources",
                []
            )

            # ------------------------------------------------
            # Print generated answer
            # ------------------------------------------------

            print("\nANSWER:")
            print(answer)

            # ------------------------------------------------
            # Print sources
            # ------------------------------------------------

            print("\nSOURCES:")

            if sources:

                for source in sources:

                    print(
                        f"- {source.get('id')} "
                        f"| chunk="
                        f"{source.get('chunk_index')} "
                        f"| score="
                        f"{source.get('score')}"
                    )

            else:

                print(
                    "- No sources"
                )

            # ------------------------------------------------
            # Evaluate answer
            # ------------------------------------------------

            evaluation = evaluate_answer(
                answer,
                item
            )

            fact_score = (
                evaluation["fact_score"]
            )

            total_fact_score += (
                fact_score
            )

            if evaluation["passed"]:
                passed_questions += 1

            # ------------------------------------------------
            # Print evaluation
            # ------------------------------------------------

            print("\nEVALUATION:")

            print(
                "Passed: "
                f"{'YES' if evaluation['passed'] else 'NO'}"
            )

            print(
                f"Fact Score: "
                f"{fact_score:.2f}"
            )

            if evaluation[
                "matched_facts"
            ]:

                print(
                    "\nMatched Facts:"
                )

                for fact in evaluation[
                    "matched_facts"
                ]:

                    print(
                        f"  ✓ {fact}"
                    )

            if evaluation[
                "missing_facts"
            ]:

                print(
                    "\nMissing Facts:"
                )

                for fact in evaluation[
                    "missing_facts"
                ]:

                    print(
                        f"  ✗ {fact}"
                    )

            if evaluation[
                "abstained"
            ]:

                print(
                    "\nAbstention:"
                    " Correctly refused "
                    "to invent information."
                )

            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            results.append(
                {
                    "id": question_id,
                    "question": question,
                    "answer": answer,
                    "passed": evaluation[
                        "passed"
                    ],
                    "fact_score": fact_score,
                    "matched_facts": evaluation[
                        "matched_facts"
                    ],
                    "missing_facts": evaluation[
                        "missing_facts"
                    ],
                    "sources": sources,
                }
            )

        except Exception as error:

            print(
                "\nERROR:"
            )

            print(error)

            results.append(
                {
                    "id": question_id,
                    "question": question,
                    "answer": "",
                    "passed": False,
                    "fact_score": 0.0,
                    "matched_facts": [],
                    "missing_facts": item.get(
                        "required_facts",
                        []
                    ),
                    "sources": [],
                    "error": str(error),
                }
            )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    average_fact_score = (
        total_fact_score
        / total_questions
        if total_questions
        else 0.0
    )

    pass_rate = (
        passed_questions
        / total_questions
        * 100
        if total_questions
        else 0.0
    )

    print("\n\n")

    print(
        "=" * 80
    )

    print(
        "FINAL EVALUATION SUMMARY"
    )

    print(
        "=" * 80
    )

    print(
        f"\nTotal Questions: "
        f"{total_questions}"
    )

    print(
        f"Passed: "
        f"{passed_questions}/"
        f"{total_questions}"
    )

    print(
        f"Pass Rate: "
        f"{pass_rate:.1f}%"
    )

    print(
        f"Average Fact Score: "
        f"{average_fact_score:.3f}"
    )

    print(
        "\nQuestion Results:"
    )

    print(
        "-" * 80
    )

    for result in results:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"{result['id']} | "
            f"{status} | "
            f"Fact Score: "
            f"{result['fact_score']:.2f}"
        )

    print(
        "=" * 80
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
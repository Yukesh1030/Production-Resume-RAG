from src.advanced_retriever import AdvancedRetriever
from src.context_builder import build_context
from src.prompts import build_prompt
from src.llm import generate_answer
from src.relevance import is_relevant
from src.source_builder import build_sources
from src.query_contextualizer import contextualize_query


class ResumeRAG:

    def __init__(self):
        self.retriever = AdvancedRetriever()

    def ask(
        self,
        query: str,
        candidate_k: int = 5,
        final_k: int = 3,
        conversation_history: list = None
    ):

        if conversation_history is None:
            conversation_history = []

        # --------------------------------------------------
        # 1. Contextualize query for retrieval
        # --------------------------------------------------

        retrieval_query = contextualize_query(
            query,
            conversation_history
        )

        print("\nRETRIEVAL QUERY:")
        print(retrieval_query)

        # --------------------------------------------------
        # 2. Retrieve documents
        # --------------------------------------------------

        results = self.retriever.search(
            retrieval_query,
            candidate_k=candidate_k,
            final_k=final_k
        )

        # --------------------------------------------------
        # 3. Relevance check
        # --------------------------------------------------

        if not is_relevant(results):

            return {
                "answer": (
                    "I don't have enough relevant "
                    "information in the provided "
                    "resume to answer this question."
                ),
                "sources": []
            }

        # --------------------------------------------------
        # 4. Build resume context
        # --------------------------------------------------

        context = build_context(
            results
        )

        # --------------------------------------------------
        # 5. Build final LLM prompt
        # --------------------------------------------------

        prompt = build_prompt(
            query,
            context,
            conversation_history
        )

        # --------------------------------------------------
        # 6. Generate answer
        # --------------------------------------------------

        answer = generate_answer(
            prompt
        )

        # --------------------------------------------------
        # 7. Build sources
        # --------------------------------------------------

        sources = build_sources(
            results
        )

        return {
            "answer": answer,
            "sources": sources
        }
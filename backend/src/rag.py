import time

from src.advanced_retriever import AdvancedRetriever
from src.context_builder import build_context
from src.prompts import build_prompt
from src.llm import generate_answer, stream_answer
from src.relevance import is_relevant
from src.source_builder import build_sources
from src.query_contextualizer import contextualize_query
from src.logger import logger


class ResumeRAG:

    def __init__(self):
        logger.info(
            "Initializing Resume RAG retriever"
        )

        self.retriever = AdvancedRetriever()

        logger.info(
            "Resume RAG retriever initialized"
        )


    def prepare_request(
        self,
        query: str,
        candidate_k: int = 5,
        final_k: int = 3,
        conversation_history: list = None
    ):
        """
        Prepare retrieval, context and prompt.
        """

        start_time = time.perf_counter()

        if conversation_history is None:
            conversation_history = []


        logger.info(
            "RAG request received | query=%s | "
            "candidate_k=%s | final_k=%s | "
            "history_messages=%s",
            query,
            candidate_k,
            final_k,
            len(conversation_history)
        )


        retrieval_query = contextualize_query(
            query,
            conversation_history
        )


        logger.info(
            "Query contextualization completed"
        )


        logger.info(
            "Starting advanced retrieval"
        )


        results = self.retriever.search(
            retrieval_query,
            candidate_k=candidate_k,
            final_k=final_k
        )


        retrieval_time = (
            time.perf_counter() - start_time
        )


        logger.info(
            "Retrieval completed | results=%s | "
            "duration=%.3fs",
            len(results),
            retrieval_time
        )


        if not is_relevant(results):

            logger.warning(
                "No relevant retrieval evidence found | "
                "query=%s",
                query
            )

            return {
                "prompt": None,
                "results": results,
                "sources": [],
                "error": (
                    "I don't have enough relevant "
                    "information in the provided "
                    "resume to answer this question."
                )
            }


        context = build_context(
            results
        )


        logger.info(
            "Context built | documents=%s | "
            "characters=%s",
            len(results),
            len(context)
        )


        prompt = build_prompt(
            query,
            context,
            conversation_history
        )


        logger.info(
            "LLM prompt prepared | "
            "prompt_characters=%s",
            len(prompt)
        )


        sources = build_sources(
            results
        )


        total_time = (
            time.perf_counter() - start_time
        )


        logger.info(
            "RAG preparation completed | "
            "duration=%.3fs",
            total_time
        )


        return {
            "prompt": prompt,
            "results": results,
            "sources": sources,
            "error": None
        }


    def ask(
        self,
        query: str,
        candidate_k: int = 5,
        final_k: int = 3,
        conversation_history: list = None
    ):
        """
        Generate a complete response.
        """

        start_time = time.perf_counter()


        prepared = self.prepare_request(
            query=query,
            candidate_k=candidate_k,
            final_k=final_k,
            conversation_history=conversation_history
        )


        if prepared["error"]:

            logger.warning(
                "RAG request completed without "
                "LLM generation"
            )

            return {
                "answer": prepared["error"],
                "sources": []
            }


        logger.info(
            "Starting non-streaming LLM generation"
        )


        answer = generate_answer(
            prepared["prompt"]
        )


        duration = (
            time.perf_counter() - start_time
        )


        logger.info(
            "LLM generation completed | "
            "answer_characters=%s | "
            "duration=%.3fs",
            len(answer),
            duration
        )


        return {
            "answer": answer,
            "sources": prepared["sources"]
        }


    def stream(
        self,
        query: str,
        candidate_k: int = 5,
        final_k: int = 3,
        conversation_history: list = None
    ):
        """
        Stream the LLM answer chunk by chunk.
        """

        prepared = self.prepare_request(
            query=query,
            candidate_k=candidate_k,
            final_k=final_k,
            conversation_history=conversation_history
        )


        if prepared["error"]:

            logger.warning(
                "Streaming request completed "
                "without LLM generation"
            )


            def error_generator():

                logger.info(
                    "Sending RAG fallback response"
                )

                yield prepared["error"]


            return {
                "chunks": error_generator(),
                "sources": []
            }


        logger.info(
            "Starting LLM streaming"
        )


        def logged_stream():

            start_time = time.perf_counter()

            chunk_count = 0
            character_count = 0


            try:

                for chunk in stream_answer(
                    prepared["prompt"]
                ):

                    chunk_count += 1
                    character_count += len(chunk)

                    yield chunk


                duration = (
                    time.perf_counter()
                    - start_time
                )


                logger.info(
                    "LLM streaming completed | "
                    "chunks=%s | "
                    "characters=%s | "
                    "duration=%.3fs",
                    chunk_count,
                    character_count,
                    duration
                )


            except Exception:

                logger.exception(
                    "LLM streaming failed"
                )

                raise


        return {
            "chunks": logged_stream(),
            "sources": prepared["sources"]
        }
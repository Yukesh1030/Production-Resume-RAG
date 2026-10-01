import json
import time

from fastapi import (
    FastAPI,
    HTTPException,
    Depends
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from fastapi.security import (
    HTTPAuthorizationCredentials
)

from pydantic import BaseModel, Field

from src.config import (
    CORS_ORIGINS,
    CANDIDATE_K,
    FINAL_K
)

from src.rag import ResumeRAG
from src.logger import logger
from src.auth import (
    security,
    verify_api_token
)


app = FastAPI(
    title="Production Resume RAG API",
    description=(
        "AI-powered Resume Question Answering API "
        "using Hybrid Search, Re-ranking and LLMs."
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ],
)


rag = ResumeRAG()


class ChatMessage(BaseModel):

    role: str = Field(
        ...,
        min_length=1,
        max_length=20
    )

    content: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="Question about the resume"
    )

    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
        description="Previous conversation messages"
    )


class ChatResponse(BaseModel):

    answer: str
    sources: list


@app.on_event("startup")
def startup_event():

    logger.info(
        "=================================================="
    )

    logger.info(
        "Production Resume RAG API starting"
    )

    logger.info(
        "Candidate K: %s",
        CANDIDATE_K
    )

    logger.info(
        "Final K: %s",
        FINAL_K
    )

    logger.info(
        "CORS origins: %s",
        CORS_ORIGINS
    )

    logger.info(
        "API authentication enabled"
    )

    logger.info(
        "Production Resume RAG API started"
    )


@app.get("/")
def root():

    logger.info(
        "GET / request"
    )

    return {
        "message": (
            "Production Resume RAG API is running"
        ),
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    logger.info(
        "GET /health request"
    )

    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    request_start = time.perf_counter()

    logger.info(
        "POST /chat request received"
    )


    verify_api_token(credentials)


    logger.info(
        "API token authentication successful"
    )


    try:

        for message in request.conversation_history:

            if message.role not in {
                "user",
                "assistant"
            }:

                logger.warning(
                    "Invalid conversation role: %s",
                    message.role
                )

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Invalid message role. "
                        "Use 'user' or 'assistant'."
                    )
                )


        history = [
            {
                "role": message.role,
                "content": message.content
            }

            for message in request.conversation_history
        ]


        logger.info(
            "Processing /chat | "
            "history_messages=%s",
            len(history)
        )


        result = rag.ask(
            request.question,
            candidate_k=CANDIDATE_K,
            final_k=FINAL_K,
            conversation_history=history
        )


        duration = (
            time.perf_counter()
            - request_start
        )


        logger.info(
            "POST /chat completed | "
            "duration=%.3fs",
            duration
        )


        return result


    except HTTPException:
        raise


    except Exception:

        logger.exception(
            "Unhandled error in POST /chat"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An error occurred while "
                "processing the question."
            )
        )


@app.post("/chat/stream")
def chat_stream(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    request_start = time.perf_counter()

    logger.info(
        "POST /chat/stream request received"
    )


    verify_api_token(credentials)


    logger.info(
        "API token authentication successful"
    )


    try:

        for message in request.conversation_history:

            if message.role not in {
                "user",
                "assistant"
            }:

                logger.warning(
                    "Invalid conversation role: %s",
                    message.role
                )

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Invalid message role. "
                        "Use 'user' or 'assistant'."
                    )
                )


        history = [
            {
                "role": message.role,
                "content": message.content
            }

            for message in request.conversation_history
        ]


        logger.info(
            "Preparing streaming request | "
            "history_messages=%s",
            len(history)
        )


        result = rag.stream(
            request.question,
            candidate_k=CANDIDATE_K,
            final_k=FINAL_K,
            conversation_history=history
        )


        def event_generator():

            try:

                metadata = {
                    "type": "sources",
                    "sources": result["sources"]
                }


                logger.info(
                    "Sending source metadata | "
                    "sources=%s",
                    len(result["sources"])
                )


                yield (
                    f"data: "
                    f"{json.dumps(metadata)}"
                    f"\n\n"
                )


                for chunk in result["chunks"]:

                    payload = {
                        "type": "content",
                        "content": chunk
                    }


                    yield (
                        f"data: "
                        f"{json.dumps(payload)}"
                        f"\n\n"
                    )


                yield (
                    f"data: "
                    f"{json.dumps({'type': 'done'})}"
                    f"\n\n"
                )


                duration = (
                    time.perf_counter()
                    - request_start
                )


                logger.info(
                    "POST /chat/stream completed | "
                    "duration=%.3fs",
                    duration
                )


            except Exception:

                logger.exception(
                    "Error during streaming response"
                )

                raise


        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )


    except HTTPException:
        raise


    except Exception:

        logger.exception(
            "Unhandled error in "
            "POST /chat/stream"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An error occurred while "
                "processing the streaming request."
            )
        )
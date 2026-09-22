from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import (
    CORS_ORIGINS,
    CANDIDATE_K,
    FINAL_K
)

from src.rag import ResumeRAG


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Production Resume RAG API",
    description=(
        "AI-powered Resume Question Answering API "
        "using Hybrid Search, Reranking and LLMs."
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=CORS_ORIGINS,

    allow_credentials=False,

    allow_methods=[
        "GET",
        "POST"
    ],

    allow_headers=[
        "Content-Type"
    ],
)


# ============================================================
# RAG ENGINE
# ============================================================

rag = ResumeRAG()


# ============================================================
# REQUEST MODELS
# ============================================================

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


# ============================================================
# RESPONSE MODEL
# ============================================================

class ChatResponse(BaseModel):

    answer: str

    sources: list


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Production Resume RAG API is running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# CHAT
# ============================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:

        # ----------------------------------------------------
        # Validate message roles
        # ----------------------------------------------------

        for message in request.conversation_history:

            if message.role not in {
                "user",
                "assistant"
            }:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Invalid message role. "
                        "Use 'user' or 'assistant'."
                    )
                )


        # ----------------------------------------------------
        # Convert messages to dictionaries
        # ----------------------------------------------------

        history = [
            {
                "role": message.role,
                "content": message.content
            }

            for message in request.conversation_history
        ]


        # ----------------------------------------------------
        # RAG
        # ----------------------------------------------------

        result = rag.ask(

            request.question,

            candidate_k=CANDIDATE_K,

            final_k=FINAL_K,

            conversation_history=history
        )


        return result


    except HTTPException:

        raise


    except Exception as error:

        print(
            f"ERROR /chat: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An error occurred while "
                "processing the question."
            )
        )
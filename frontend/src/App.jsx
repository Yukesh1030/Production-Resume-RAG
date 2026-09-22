import { useEffect, useRef, useState } from "react";
import "./App.css";


// ============================================================
// SUGGESTIONS
// ============================================================

const suggestions = [
  "What technologies does Yukesh know?",
  "What projects has Yukesh worked on?",
  "What is Yukesh's educational background?",
  "What is Yukesh's experience with React?",
];


// ============================================================
// FORMAT AI ANSWER
// ============================================================

function formatAnswer(text) {
  if (!text) {
    return null;
  }

  return text.split("\n").map((line, index) => {

    const formatted = line.replace(
      /\*\*(.*?)\*\*/g,
      "<strong>$1</strong>"
    );

    return (
      <span
        key={index}
        dangerouslySetInnerHTML={{
          __html: formatted || "&nbsp;",
        }}
      />
    );
  });
}


// ============================================================
// APP
// ============================================================

function App() {

  // ----------------------------------------------------------
  // INPUT
  // ----------------------------------------------------------

  const [question, setQuestion] = useState("");


  // ----------------------------------------------------------
  // CONVERSATION
  // ----------------------------------------------------------

  const [messages, setMessages] = useState([]);


  // ----------------------------------------------------------
  // UI STATE
  // ----------------------------------------------------------

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // ----------------------------------------------------------
  // AUTO SCROLL
  // ----------------------------------------------------------

  const messagesEndRef = useRef(null);


  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);


  // ==========================================================
  // ASK QUESTION
  // ==========================================================

  const askQuestion = async () => {

    const trimmedQuestion = question.trim();


    // --------------------------------------------------------
    // Validation
    // --------------------------------------------------------

    if (!trimmedQuestion || loading) {
      return;
    }


    // --------------------------------------------------------
    // Clear error
    // --------------------------------------------------------

    setError("");


    // --------------------------------------------------------
    // Save current conversation history BEFORE adding
    // current user question.
    //
    // This is important because the backend should receive
    // previous conversation turns as context.
    // --------------------------------------------------------

    const conversationHistory = messages.map((message) => ({
      role: message.role,
      content: message.content,
    }));


    // --------------------------------------------------------
    // Add user message immediately to UI
    // --------------------------------------------------------

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);


    // --------------------------------------------------------
    // Clear input
    // --------------------------------------------------------

    setQuestion("");

    setLoading(true);


    try {

      // ======================================================
      // API REQUEST
      // ======================================================

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: trimmedQuestion,

            conversation_history:
              conversationHistory,
          }),
        }
      );


      // ------------------------------------------------------
      // HTTP ERROR
      // ------------------------------------------------------

      if (!response.ok) {

        const errorData = await response.json()
          .catch(() => null);

        throw new Error(
          errorData?.detail ||
          "API request failed"
        );
      }


      // ------------------------------------------------------
      // RESPONSE
      // ------------------------------------------------------

      const data = await response.json();


      // ======================================================
      // ADD AI RESPONSE
      // ======================================================

      const assistantMessage = {
        id: Date.now() + 1,

        role: "assistant",

        content: data.answer,

        sources: data.sources || [],
      };


      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);

    } catch (error) {

      console.error(error);


      // ------------------------------------------------------
      // Error message
      // ------------------------------------------------------

      setError(
        error.message ||
        "Unable to connect to the AI server. Make sure FastAPI is running."
      );


    } finally {

      setLoading(false);

    }
  };


  // ==========================================================
  // KEYBOARD HANDLER
  // ==========================================================

  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();
    }
  };


  // ==========================================================
  // SUGGESTION
  // ==========================================================

  const selectSuggestion = (suggestion) => {

    setQuestion(suggestion);

  };


  // ==========================================================
  // CLEAR CHAT
  // ==========================================================

  const clearChat = () => {

    setMessages([]);

    setQuestion("");

    setError("");

  };


  // ==========================================================
  // RENDER
  // ==========================================================

  return (

    <div className="app">

      {/* ====================================================
          BACKGROUND GLOW
      ==================================================== */}

      <div className="glow glow-one"></div>

      <div className="glow glow-two"></div>


      {/* ====================================================
          NAVBAR
      ==================================================== */}

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            ✦
          </div>

          <div>

            <div className="brand-name">
              Resume<span>RAG</span>
            </div>

            <div className="brand-subtitle">
              AI Resume Intelligence
            </div>

          </div>

        </div>


        <div className="navbar-actions">

          <div className="status">

            <span className="status-dot"></span>

            API Online

          </div>


          {messages.length > 0 && (

            <button
              className="clear-button"
              onClick={clearChat}
            >
              Clear Chat
            </button>

          )}

        </div>

      </header>


      {/* ====================================================
          MAIN
      ==================================================== */}

      <main className="main">


        {/* ==================================================
            HERO
        ================================================== */}

        {messages.length === 0 && (

          <section className="hero">

            <div className="hero-badge">

              <span>✦</span>

              Production RAG System

            </div>


            <h1>

              Ask anything about

              <span>
                {" "}Yukesh's resume.
              </span>

            </h1>


            <p>

              An AI-powered resume assistant using
              semantic search, hybrid retrieval,
              re-ranking and LLM generation.

            </p>

          </section>

        )}


        {/* ==================================================
            CHAT AREA
        ================================================== */}

        {messages.length > 0 && (

          <section className="chat-container">

            {messages.map((message) => (

              <div
                key={message.id}
                className={`message-row ${message.role}`}
              >

                {/* ------------------------------------------
                    MESSAGE ICON
                ------------------------------------------ */}

                <div className="message-avatar">

                  {message.role === "user"
                    ? "Y"
                    : "✦"}

                </div>


                {/* ------------------------------------------
                    MESSAGE CONTENT
                ------------------------------------------ */}

                <div className="message-wrapper">

                  <div className="message-name">

                    {message.role === "user"
                      ? "You"
                      : "Resume AI"}

                  </div>


                  <div className="message-bubble">

                    <div className="message-content">

                      {message.role === "assistant"
                        ? formatAnswer(message.content)
                        : message.content}

                    </div>


                    {/* ----------------------------------------
                        SOURCES
                    ---------------------------------------- */}

                    {message.role === "assistant" &&
                      message.sources &&
                      message.sources.length > 0 && (

                        <div className="message-sources">

                          <div className="sources-heading">

                            <span>
                              Sources
                            </span>

                            <span className="source-count">

                              {message.sources.length}
                              {" "}chunks

                            </span>

                          </div>


                          <div className="sources-grid">

                            {message.sources.map(
                              (source) => (

                                <div
                                  className="source-card"
                                  key={source.id}
                                >

                                  <div className="source-top">

                                    <div className="file-icon">
                                      PDF
                                    </div>


                                    <div className="source-info">

                                      <strong>
                                        {source.source}
                                      </strong>

                                      <span>
                                        Chunk{" "}
                                        {source.chunk_index}
                                      </span>

                                    </div>

                                  </div>


                                  {source.score !== null &&
                                    source.score !== undefined && (

                                      <div className="score">

                                        <span>
                                          Relevance
                                        </span>

                                        <strong>
                                          {source.score.toFixed(2)}
                                        </strong>

                                      </div>

                                    )}

                                </div>

                              )
                            )}

                          </div>

                        </div>

                      )}

                  </div>

                </div>

              </div>

            ))}


            {/* =================================================
                LOADING MESSAGE
            ================================================= */}

            {loading && (

              <div className="message-row assistant">

                <div className="message-avatar">
                  ✦
                </div>


                <div className="message-wrapper">

                  <div className="message-name">
                    Resume AI
                  </div>


                  <div className="message-bubble loading-bubble">

                    <div className="thinking">

                      <span className="thinking-dot"></span>

                      <span className="thinking-dot"></span>

                      <span className="thinking-dot"></span>

                    </div>


                    <span>
                      Searching the resume...
                    </span>

                  </div>

                </div>

              </div>

            )}


            <div ref={messagesEndRef}></div>

          </section>

        )}


        {/* ==================================================
            ERROR
        ================================================== */}

        {error && (

          <div className="error-card">

            <span>⚠</span>

            <div>

              <strong>
                Connection error
              </strong>

              <p>
                {error}
              </p>

            </div>

          </div>

        )}


        {/* ==================================================
            INITIAL SUGGESTIONS
        ================================================== */}

        {messages.length === 0 && (

          <section className="suggestions">

            <span className="suggestion-title">
              Try asking
            </span>


            <div className="suggestion-list">

              {suggestions.map((suggestion) => (

                <button
                  key={suggestion}
                  className="suggestion"
                  onClick={() =>
                    selectSuggestion(suggestion)
                  }
                >

                  {suggestion}

                </button>

              ))}

            </div>

          </section>

        )}


        {/* ==================================================
            INPUT CARD
        ================================================== */}

        <section className="ask-card">

          <div className="input-header">

            <span className="input-label">
              {messages.length > 0
                ? "Continue the conversation"
                : "Ask a question"}
            </span>


            <span className="input-hint">
              Enter ↵ to send
            </span>

          </div>


          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder={
              messages.length > 0
                ? "Ask a follow-up question..."
                : "e.g. What technologies does Yukesh know?"
            }
            rows={4}
            maxLength={500}
          />


          <div className="input-footer">

            <span className="character-count">
              {question.length}/500
            </span>


            <button
              className="ask-button"
              onClick={askQuestion}
              disabled={
                loading ||
                !question.trim()
              }
            >

              {loading ? (

                <>

                  <span className="spinner"></span>

                  Thinking...

                </>

              ) : (

                <>

                  Ask AI

                  <span className="arrow">
                    ↗
                  </span>

                </>

              )}

            </button>

          </div>

        </section>


        {/* ==================================================
            FOOTER
        ================================================== */}

        <footer>

          <div>

            Built with

            <strong>
              {" "}React
            </strong>

            {" + "}

            <strong>
              FastAPI
            </strong>

            {" + "}

            <strong>
              RAG
            </strong>

          </div>


          <span>
            Production Resume RAG · v1.0
          </span>

        </footer>


      </main>

    </div>

  );
}


export default App;
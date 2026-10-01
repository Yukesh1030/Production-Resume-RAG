import { useEffect, useState } from "react";
import "./App.css";


const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


const API_TOKEN =
  import.meta.env.VITE_API_TOKEN || "";


const suggestions = [
  "What programming languages does Yukesh know?",
  "What projects has Yukesh worked on?",
  "What is Yukesh's educational background?",
  "What did Yukesh achieve on HackerRank?"
];


function App() {

  const [messages, setMessages] = useState([]);

  const [question, setQuestion] = useState("");

  const [isStreaming, setIsStreaming] = useState(false);

  const [apiOnline, setApiOnline] = useState(false);

  const [sources, setSources] = useState([]);

  const [error, setError] = useState("");


  /*
   * Check whether the FastAPI server is available.
   */

  const checkApiHealth = async () => {

    try {

      const response = await fetch(
        `${API_URL}/health`
      );

      if (response.ok) {
        setApiOnline(true);
      } else {
        setApiOnline(false);
      }

    } catch {
      setApiOnline(false);
    }
  };


  /*
   * Check API status when the application starts.
   */

  useEffect(() => {

    checkApiHealth();

    const interval = setInterval(
      checkApiHealth,
      15000
    );

    return () => {
      clearInterval(interval);
    };

  }, []);


  /*
   * Send a question to FastAPI
   * using authenticated SSE streaming.
   */

  const askQuestion = async (
    submittedQuestion = question
  ) => {

    const trimmedQuestion =
      submittedQuestion.trim();


    if (!trimmedQuestion) {
      return;
    }


    if (isStreaming) {
      return;
    }


    if (!API_TOKEN) {

      setError(
        "API token is not configured. " +
        "Check frontend/.env."
      );

      return;
    }


    setError("");

    setSources([]);

    setIsStreaming(true);


    /*
     * Add the user's message.
     */

    const userMessage = {
      role: "user",
      content: trimmedQuestion
    };


    /*
     * Add an empty assistant message.
     * It will be filled progressively
     * as streaming chunks arrive.
     */

    const assistantMessage = {
      role: "assistant",
      content: ""
    };


    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
      assistantMessage
    ]);


    setQuestion("");


    try {

      /*
       * Convert previous messages into the
       * format expected by FastAPI.
       *
       * We exclude the newly-created assistant
       * message because it is currently empty.
       */

      const conversationHistory =
        messages.map((message) => ({
          role: message.role,
          content: message.content
        }));


      /*
       * Authenticated streaming request.
       */

      const response = await fetch(
        `${API_URL}/chat/stream`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",

            "Authorization":
              `Bearer ${API_TOKEN}`
          },

          body: JSON.stringify({
            question: trimmedQuestion,
            conversation_history:
              conversationHistory
          })
        }
      );


      /*
       * Handle authentication failure.
       */

      if (response.status === 401) {

        throw new Error(
          "Authentication failed. " +
          "Check VITE_API_TOKEN in frontend/.env."
        );
      }


      /*
       * Handle other API errors.
       */

      if (!response.ok) {

        let errorMessage =
          `API request failed: ${response.status}`;

        try {

          const errorData =
            await response.json();

          if (errorData.detail) {
            errorMessage =
              errorData.detail;
          }

        } catch {
          // Keep the default error message.
        }

        throw new Error(errorMessage);
      }


      /*
       * Make sure the browser received
       * a streaming response body.
       */

      if (!response.body) {

        throw new Error(
          "Streaming response is not available."
        );
      }


      const reader =
        response.body.getReader();


      const decoder =
        new TextDecoder("utf-8");


      let buffer = "";


      /*
       * Read SSE data continuously.
       */

      while (true) {

        const {
          value,
          done
        } = await reader.read();


        if (done) {
          break;
        }


        buffer += decoder.decode(
          value,
          {
            stream: true
          }
        );


        /*
         * SSE events are separated by
         * two newline characters.
         */

        const events =
          buffer.split("\n\n");


        /*
         * Keep the incomplete event for
         * the next iteration.
         */

        buffer =
          events.pop() || "";


        for (const event of events) {

          const lines =
            event.split("\n");


          for (const line of lines) {

            if (
              !line.startsWith("data:")
            ) {
              continue;
            }


            const jsonText =
              line.substring(5).trim();


            if (!jsonText) {
              continue;
            }


            let payload;


            try {

              payload =
                JSON.parse(jsonText);

            } catch {

              continue;
            }


            /*
             * Receive source metadata.
             */

            if (
              payload.type === "sources"
            ) {

              setSources(
                payload.sources || []
              );

              continue;
            }


            /*
             * Receive streamed LLM content.
             */

            if (
              payload.type === "content"
            ) {

              setMessages(
                (previousMessages) => {

                  const updatedMessages =
                    [...previousMessages];


                  const lastIndex =
                    updatedMessages.length - 1;


                  if (
                    updatedMessages[lastIndex]
                    ?.role === "assistant"
                  ) {

                    updatedMessages[
                      lastIndex
                    ] = {
                      ...updatedMessages[
                        lastIndex
                      ],

                      content:
                        updatedMessages[
                          lastIndex
                        ].content +
                        payload.content
                    };

                  }


                  return updatedMessages;
                }
              );

              continue;
            }


            /*
             * Streaming completed.
             */

            if (
              payload.type === "done"
            ) {

              continue;
            }
          }
        }
      }


      /*
       * Flush any remaining decoder data.
       */

      buffer += decoder.decode();


    } catch (err) {

      console.error(
        "Streaming error:",
        err
      );


      setError(
        err.message ||
        "Unable to communicate with the API."
      );


      /*
       * Remove the empty assistant
       * message if the request failed
       * before receiving any content.
       */

      setMessages(
        (previousMessages) => {

          const lastMessage =
            previousMessages[
              previousMessages.length - 1
            ];


          if (
            lastMessage?.role === "assistant" &&
            !lastMessage.content
          ) {

            return previousMessages.slice(
              0,
              -1
            );
          }


          return previousMessages;
        }
      );

    } finally {

      setIsStreaming(false);
    }
  };


  /*
   * Submit form.
   */

  const handleSubmit = (event) => {

    event.preventDefault();

    askQuestion();
  };


  /*
   * Use one of the suggested questions.
   */

  const handleSuggestion = (
    suggestion
  ) => {

    if (isStreaming) {
      return;
    }

    setQuestion(suggestion);

    askQuestion(suggestion);
  };


  return (
    <div className="app">

      {/* ================================
          NAVBAR
          ================================ */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-mark">
            R
          </div>

          <div>
            <div className="brand-name">
              ResumeRAG
            </div>

            <div className="brand-subtitle">
              Production AI
            </div>
          </div>

        </div>


        <div className="api-status">

          <span
            className={
              apiOnline
                ? "status-dot online"
                : "status-dot offline"
            }
          />

          <span>
            {apiOnline
              ? "API Online"
              : "API Offline"}
          </span>

        </div>

      </nav>


      {/* ================================
          HERO
          ================================ */}

      <main className="main-container">

        <section className="hero">

          <div className="hero-badge">
            <span>✦</span>
            AI-Powered Resume Assistant
          </div>


          <h1>
            Ask questions.
            <br />

            <span>
              Get grounded answers.
            </span>
          </h1>


          <p className="hero-description">

            A production-ready RAG system that
            searches Yukesh's resume using
            semantic search, keyword retrieval,
            re-ranking and LLM generation.

          </p>


          <div className="architecture">

            <span>HYBRID SEARCH</span>

            <span className="arrow">
              →
            </span>

            <span>RE-RANKING</span>

            <span className="arrow">
              →
            </span>

            <span>LLM</span>

          </div>

        </section>


        {/* ================================
            CHAT CONTAINER
            ================================ */}

        <section className="chat-container">

          <div className="chat-header">

            <div>

              <div className="chat-title">
                Resume Assistant
              </div>

              <div className="chat-subtitle">
                Ask anything about the resume
              </div>

            </div>


            <div className="grounded-badge">
              <span>●</span>
              RAG Grounded
            </div>

          </div>


          {/* ==============================
              MESSAGES
              ============================== */}

          <div className="messages">

            {messages.length === 0 && (

              <div className="empty-state">

                <div className="empty-icon">
                  ✦
                </div>

                <h2>
                  Start a conversation
                </h2>

                <p>
                  Ask about skills, projects,
                  education, experience or
                  achievements.
                </p>

              </div>

            )}


            {messages.map(
              (message, index) => (

                <div
                  key={index}
                  className={
                    message.role === "user"
                      ? "message user-message"
                      : "message assistant-message"
                  }
                >

                  <div className="message-label">

                    {message.role === "user"
                      ? "YOU"
                      : "AI"}

                  </div>


                  <div className="message-content">

                    {message.content}


                    {message.role === "assistant" &&
                      isStreaming &&
                      index ===
                        messages.length - 1 && (

                        <span className="cursor">
                          ▋
                        </span>

                    )}

                  </div>

                </div>

            ))}


            {/* ==============================
                SOURCES
                ============================== */}

            {sources.length > 0 && (

              <div className="sources-section">

                <div className="sources-title">
                  Sources
                </div>


                <div className="sources-grid">

                  {sources.map(
                    (source, index) => (

                      <div
                        key={
                          source.id ||
                          index
                        }
                        className="source-card"
                      >

                        <div className="source-icon">
                          ◈
                        </div>

                        <div>

                          <div className="source-name">
                            {source.source ||
                              "resume.pdf"}
                          </div>

                          <div className="source-meta">

                            Chunk{" "}
                            {source.chunk_index ??
                              "N/A"}

                          </div>

                        </div>

                      </div>

                  ))}

                </div>

              </div>

            )}


            {/* ==============================
                ERROR
                ============================== */}

            {error && (

              <div className="error-card">

                <div className="error-icon">
                  !
                </div>

                <div>

                  <div className="error-title">
                    Request failed
                  </div>

                  <div className="error-message">
                    {error}
                  </div>

                </div>

              </div>

            )}

          </div>


          {/* ================================
              SUGGESTIONS
              ================================ */}

          <div className="suggestions">

            <div className="suggestions-title">
              Try asking
            </div>


            <div className="suggestions-list">

              {suggestions.map(
                (suggestion, index) => (

                  <button
                    key={index}
                    className="suggestion"
                    onClick={() =>
                      handleSuggestion(
                        suggestion
                      )
                    }
                    disabled={isStreaming}
                  >
                    {suggestion}
                  </button>

              ))}

            </div>

          </div>


          {/* ================================
              INPUT
              ================================ */}

          <form
            className="input-area"
            onSubmit={handleSubmit}
          >

            <input
              type="text"
              value={question}
              onChange={(event) =>
                setQuestion(
                  event.target.value
                )
              }
              placeholder={
                isStreaming
                  ? "AI is responding..."
                  : "Ask a question about the resume..."
              }
              disabled={
                isStreaming ||
                !apiOnline
              }
            />


            <button
              type="submit"
              className="ask-button"
              disabled={
                isStreaming ||
                !question.trim() ||
                !apiOnline
              }
            >

              {isStreaming
                ? "Thinking..."
                : "Ask AI →"}

            </button>

          </form>


          <div className="input-footer">

            <span>
              🔒 Authenticated API
            </span>

            <span>
              •
            </span>

            <span>
              Streaming enabled
            </span>

            <span>
              •
            </span>

            <span>
              Resume grounded
            </span>

          </div>

        </section>


        {/* ================================
            INFO CARD
            ================================ */}

        <section className="info-card">

          <div className="info-item">

            <div className="info-number">
              01
            </div>

            <div>

              <h3>
                Hybrid Retrieval
              </h3>

              <p>
                Semantic search combined with
                BM25 keyword retrieval.
              </p>

            </div>

          </div>


          <div className="info-item">

            <div className="info-number">
              02
            </div>

            <div>

              <h3>
                Re-ranking
              </h3>

              <p>
                Cross-encoder scoring improves
                retrieved context quality.
              </p>

            </div>

          </div>


          <div className="info-item">

            <div className="info-number">
              03
            </div>

            <div>

              <h3>
                Grounded Generation
              </h3>

              <p>
                LLM responses are generated
                using retrieved resume evidence.
              </p>

            </div>

          </div>

        </section>


        {/* ================================
            FOOTER
            ================================ */}

        <footer className="footer">

          <span>
            Production Resume RAG
          </span>

          <span>
            Built with React + FastAPI +
            ChromaDB + Groq
          </span>

        </footer>

      </main>

    </div>
  );
}


export default App;
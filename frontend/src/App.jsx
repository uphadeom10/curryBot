import { useState, useRef, useEffect } from "react"
import axios from "axios"
import ReactMarkdown from "react-markdown"
import "./App.css"

// API URL
const API_URL = "https://om10-currybot.hf.space"  // ✅

function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      content: "Namaste! 🙏 I am CurryBot, your Indian food assistant. Ask me anything about Indian recipes — ingredients, cooking steps, cost, and more! 🍛"
    }
  ])
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  // Auto scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Send message to FastAPI
  const sendMessage = async () => {
    // Don't send empty message
    if (!question.trim()) return

    // Add user message to chat
    const userMessage = { role: "user", content: question }
    setMessages(prev => [...prev, userMessage])
    setQuestion("")
    setLoading(true)

    try {
      // Call FastAPI /chat endpoint
      const response = await axios.post(`${API_URL}/chat`, {
        question: question
      })

      // Add bot response to chat
      const botMessage = { role: "bot", content: response.data.answer }
      setMessages(prev => [...prev, botMessage])

    } catch (error) {
      // Show error if API fails
      setMessages(prev => [...prev, {
        role: "bot",
        content: "Sorry, something went wrong. Please try again! 🙏"
      }])
    }

    setLoading(false)
  }

  // Reset chat history
  const resetChat = async () => {
    await axios.post(`${API_URL}/reset`)
    setMessages([
      {
        role: "bot",
        content: "Namaste! 🙏 I am CurryBot, your Indian food assistant. Ask me anything about Indian recipes! 🍛"
      }
    ])
  }

  // Send on Enter key
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app">

      {/* Header */}
      <div className="header">
        <div className="header-left">
          <span className="logo">🍛</span>
          <div>
            <h1>CurryBot</h1>
            <p>Your Indian Food Assistant</p>
          </div>
        </div>
        <button className="reset-btn" onClick={resetChat}>
          New Chat 🗑️
        </button>
      </div>

      {/* Chat Messages */}
      <div className="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="avatar">
              {msg.role === "bot" ? "🍛" : "👤"}
            </div>
            <div className="bubble">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="message bot">
            <div className="avatar">🍛</div>
            <div className="bubble loading">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="input-area">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
         placeholder="Ask me any Indian recipe..."
          rows={1}
        />
        <button
          className="send-btn"
          onClick={sendMessage}
          disabled={loading || !question.trim()}
        >
          {loading ? "..." : "➤"}
        </button>
      </div>

    </div>
  )
}

export default App

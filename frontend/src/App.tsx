import { useState, useRef, useEffect } from 'react'
import './App.css'

interface Message {
  id: string
  text: string
  sender: 'user' | 'assistant'
  timestamp: Date
}

function App() {
  const BASE_URL = "http://127.0.0.1:8000"
  const [videoUrl, setVideoUrl] = useState('')
  const [videoId, setVideoId] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [messages, isLoading])

  const extractYouTubeId = (url: string): string | null => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
    const match = url.match(regExp)
    return (match && match[2].length === 11) ? match[2] : null
  }

  const handleVideoSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    const id = extractYouTubeId(videoUrl)
    
    if (!id) {
      alert('Please enter a valid YouTube URL')
      return
    }

    setVideoId(id)
    setIsProcessing(true)
    
    try {
        const response = await fetch(`${BASE_URL}/process-video?video_link=${encodeURIComponent(videoUrl)}`, {
          method: 'POST',
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      setMessages([{
        id: '1',
        text: `Video processed successfully! I found ${data.chunk_count} text chunks from the video. You can now ask me questions about this YouTube video.`,
        sender: 'assistant',
        timestamp: new Date()
      }])
    } catch (error) {
      console.error('Error processing video:', error)
      setMessages([{
        id: '1',
        text: `Error processing video: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        sender: 'assistant',
        timestamp: new Date()
      }])
    } finally {
      setIsProcessing(false)
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !videoId) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const currentInput = inputMessage
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentInput,
          message_history: messages
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer,
        sender: 'assistant',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error asking question:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `Error getting response: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        sender: 'assistant',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSendMessage()
    }
  }

  const resetApp = () => {
    setVideoUrl('')
    setVideoId(null)
    setMessages([])
    setInputMessage('')
    setIsLoading(false)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>YouTube Video Assistant</h1>
        <p>Paste a YouTube URL and chat with AI about the video content</p>
      </header>

      <main className="main">
        {!videoId ? (
          <div className="url-section">
            <div className="url-form-container">
              <div className="url-icon">📺</div>
              <h2>Enter YouTube Video URL</h2>
              <p>Paste a YouTube video link to start chatting about its content</p>
              
              <form onSubmit={handleVideoSubmit} className="url-form">
                <div className="input-group">
                  <input
                    type="url"
                    value={videoUrl}
                    onChange={(e) => setVideoUrl(e.target.value)}
                    placeholder="https://www.youtube.com/watch?v=..."
                    className="url-input"
                    required
                  />
                  <button 
                    type="submit" 
                    className="submit-button"
                    disabled={!videoUrl.trim() || isProcessing}
                  >
                    {isProcessing ? 'Processing...' : 'Load Video'}
                  </button>
                </div>
              </form>
              
              <div className="example-urls">
                <p>Example formats:</p>
                <ul>
                  <li>https://www.youtube.com/watch?v=dQw4w9WgXcQ</li>
                  <li>https://youtu.be/dQw4w9WgXcQ</li>
                  <li>https://youtube.com/embed/dQw4w9WgXcQ</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="chat-section">
            <div className="video-info">
              <div className="video-preview">
                <iframe
                  src={`https://www.youtube.com/embed/${videoId}`}
                  title="YouTube video player"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="video-player"
                />
              </div>
              <div className="video-details">
                <h3>YouTube Video</h3>
                <p>Video ID: {videoId}</p>
                <button onClick={resetApp} className="reset-button">
                  Load New Video
                </button>
              </div>
            </div>

            <div className="chat-container">
              <div className="chat-messages" ref={chatContainerRef}>
                {messages.map((message) => (
                  <div 
                    key={message.id} 
                    className={`message ${message.sender}`}
                  >
                    <div className="message-content">
                      {message.text}
                    </div>
                    <div className="message-time">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="message assistant">
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="chat-input">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a question about the video..."
                  disabled={isLoading}
                  rows={3}
                />
                <button 
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  className="send-button"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {isProcessing && (
          <div className="upload-overlay">
            <div className="upload-progress">
              <div className="spinner"></div>
              <p>Processing video...</p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

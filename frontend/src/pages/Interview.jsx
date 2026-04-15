import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar.jsx'
import API from '../api/axios'

// Mic Animation Component
function MicAnimation({ isActive }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', gap: '12px', margin: '16px 0'
    }}>
      {/* Mic Button */}
      <div style={{
        width: '80px', height: '80px', borderRadius: '50%',
        background: isActive
          ? 'linear-gradient(135deg, #6366f1, #8b5cf6)'
          : '#e5e7eb',
        display: 'flex', alignItems: 'center',
        justifyContent: 'center', fontSize: '32px',
        animation: isActive ? 'micPulse 1.5s infinite' : 'none',
        transition: 'all 0.3s',
        boxShadow: isActive
          ? '0 0 0 0 rgba(99,102,241,0.4)'
          : 'none'
      }}>
        🎤
      </div>

      {/* Sound Waves */}
      {isActive && (
        <div style={{
          display: 'flex', alignItems: 'center',
          gap: '4px', height: '30px'
        }}>
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} style={{
              width: '4px',
              background: '#6366f1',
              borderRadius: '2px',
              animation: `wave 0.8s ease-in-out infinite`,
              animationDelay: `${i * 0.1}s`,
              height: '8px'
            }} />
          ))}
        </div>
      )}

      <p style={{
        fontSize: '13px', color: isActive ? '#6366f1' : '#9ca3af',
        fontWeight: '500'
      }}>
        {isActive ? 'Listening...' : 'Click to speak'}
      </p>
    </div>
  )
}

function Interview() {
  const [role, setRole] = useState('ML Engineer')
  const [difficulty, setDifficulty] = useState('medium')
  const [session, setSession] = useState(null)
  const [currentQ, setCurrentQ] = useState(0)
  const [answer, setAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)
  const [started, setStarted] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [allFeedback, setAllFeedback] = useState([])
  const [isListening, setIsListening] = useState(false)
  const [inputMode, setInputMode] = useState('text') // 'text' or 'mic'

  // Speech Recognition Setup
  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) &&
        !('SpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser!')
      return
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'en-US'

    recognition.onstart = () => setIsListening(true)
    recognition.onend = () => setIsListening(false)

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript
      }
      setAnswer(transcript)
    }

    recognition.onerror = () => setIsListening(false)

    recognition.start()

    // Auto stop after 30 seconds
    setTimeout(() => recognition.stop(), 30000)
  }

  const startInterview = async () => {
    setLoading(true)
    try {
      const response = await API.post('/interview/start', {
        role, difficulty, num_questions: 5
      })
      setSession(response.data)
      setStarted(true)
      setCurrentQ(0)
      setFeedback(null)
      setAllFeedback([])
      setCompleted(false)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const submitAnswer = async () => {
    if (!answer.trim()) return
    setLoading(true)
    try {
      const question = session.questions[currentQ]
      const response = await API.post('/interview/answer', {
        session_id: session.session_id,
        question_id: question.id,
        question: question.question,
        answer: answer
      })
      const fb = response.data.feedback
      setFeedback(fb)
      setAllFeedback(prev => [...prev, {
        question: question.question,
        answer, feedback: fb
      }])
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const nextQuestion = () => {
    if (currentQ < session.questions.length - 1) {
      setCurrentQ(currentQ + 1)
      setAnswer('')
      setFeedback(null)
      setIsListening(false)
    } else {
      setCompleted(true)
    }
  }

  const getOverallScore = () => {
    if (allFeedback.length === 0) return 0
    const total = allFeedback.reduce(
      (sum, item) => sum + (item.feedback?.score || 0), 0
    )
    return Math.round((total / (allFeedback.length * 10)) * 100)
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <Navbar active="interview" />
      <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>

        {/* Header */}
        <div style={{
          background: 'linear-gradient(135deg, #1e1b4b, #312e81)',
          borderRadius: '20px', padding: '2rem',
          color: 'white', marginBottom: '2rem',
          boxShadow: '0 10px 40px rgba(30,27,75,0.3)'
        }}>
          <h1 style={{ fontSize: '28px', fontWeight: '800', marginBottom: '8px' }}>
            🎤 AI Mock Interview
          </h1>
          <p style={{ opacity: '0.8', fontSize: '16px' }}>
            Practice with AI interviewer — Type or Speak your answers!
          </p>
        </div>

        {/* Setup Screen */}
        {!started && (
          <div style={{
            background: 'white', borderRadius: '20px',
            padding: '2rem', border: '1px solid #e5e7eb',
            boxShadow: '0 4px 20px rgba(0,0,0,0.05)'
          }}>
            <h2 style={{
              fontSize: '20px', fontWeight: '700',
              marginBottom: '1.5rem', color: '#1a1a1a'
            }}>
              ⚙️ Interview Setup
            </h2>

            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block', fontSize: '13px',
                fontWeight: '600', color: '#6b7280',
                marginBottom: '8px', textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Job Role
              </label>
              <input
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g. ML Engineer, Software Developer"
                style={{
                  width: '100%', padding: '14px 16px',
                  border: '2px solid #e5e7eb', borderRadius: '10px',
                  fontSize: '15px', outline: 'none', boxSizing: 'border-box'
                }}
                onFocus={e => e.target.style.borderColor = '#6366f1'}
                onBlur={e => e.target.style.borderColor = '#e5e7eb'}
              />
            </div>

            <div style={{ marginBottom: '28px' }}>
              <label style={{
                display: 'block', fontSize: '13px',
                fontWeight: '600', color: '#6b7280',
                marginBottom: '12px', textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Difficulty Level
              </label>
              <div style={{ display: 'flex', gap: '12px' }}>
                {[
                  { id: 'easy', label: '😊 Easy', color: '#10b981' },
                  { id: 'medium', label: '🔥 Medium', color: '#f59e0b' },
                  { id: 'hard', label: '💪 Hard', color: '#ef4444' }
                ].map(d => (
                  <button
                    key={d.id}
                    onClick={() => setDifficulty(d.id)}
                    style={{
                      flex: 1, padding: '12px',
                      border: '2px solid',
                      borderColor: difficulty === d.id ? d.color : '#e5e7eb',
                      background: difficulty === d.id
                        ? `${d.color}15` : 'white',
                      color: difficulty === d.id ? d.color : '#6b7280',
                      borderRadius: '10px', fontWeight: '700',
                      cursor: 'pointer', fontSize: '14px',
                      transition: 'all 0.2s'
                    }}
                  >
                    {d.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Input Mode Selection */}
            <div style={{ marginBottom: '24px' }}>
              <label style={{
                display: 'block', fontSize: '13px',
                fontWeight: '600', color: '#6b7280',
                marginBottom: '12px', textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Answer Input Mode
              </label>
              <div style={{ display: 'flex', gap: '12px' }}>
                <button
                  onClick={() => setInputMode('text')}
                  style={{
                    flex: 1, padding: '12px',
                    border: '2px solid',
                    borderColor: inputMode === 'text' ? '#6366f1' : '#e5e7eb',
                    background: inputMode === 'text' ? '#ede9fe' : 'white',
                    color: inputMode === 'text' ? '#6366f1' : '#6b7280',
                    borderRadius: '10px', fontWeight: '600',
                    cursor: 'pointer', fontSize: '14px'
                  }}
                >
                  ⌨️ Type Answer
                </button>
                <button
                  onClick={() => setInputMode('mic')}
                  style={{
                    flex: 1, padding: '12px',
                    border: '2px solid',
                    borderColor: inputMode === 'mic' ? '#6366f1' : '#e5e7eb',
                    background: inputMode === 'mic' ? '#ede9fe' : 'white',
                    color: inputMode === 'mic' ? '#6366f1' : '#6b7280',
                    borderRadius: '10px', fontWeight: '600',
                    cursor: 'pointer', fontSize: '14px'
                  }}
                >
                  🎤 Speak Answer
                </button>
              </div>
            </div>

            <button
              onClick={startInterview}
              disabled={loading}
              style={{
                width: '100%', padding: '16px',
                background: loading ? '#9ca3af'
                  : 'linear-gradient(135deg, #1e1b4b, #4338ca)',
                color: 'white', border: 'none', borderRadius: '12px',
                fontSize: '17px', fontWeight: '700', cursor: 'pointer',
                boxShadow: loading ? 'none'
                  : '0 4px 15px rgba(67,56,202,0.4)',
                transition: 'all 0.2s'
              }}
            >
              {loading ? '⏳ Loading questions...' : '🎤 Start Interview'}
            </button>
          </div>
        )}

        {/* Completed Screen */}
        {completed && (
          <div style={{
            background: 'white', borderRadius: '20px',
            padding: '3rem', border: '1px solid #e5e7eb',
            textAlign: 'center',
            boxShadow: '0 4px 20px rgba(0,0,0,0.05)'
          }}>
            <div style={{ fontSize: '80px', marginBottom: '16px' }}>🎉</div>
            <h2 style={{
              fontSize: '28px', fontWeight: '800',
              marginBottom: '8px', color: '#1a1a1a'
            }}>
              Interview Complete!
            </h2>
            <p style={{ fontSize: '16px', color: '#6b7280', marginBottom: '8px' }}>
              Your overall score:
            </p>
            <div style={{
              fontSize: '64px', fontWeight: '900',
              color: getOverallScore() >= 70 ? '#10b981' : '#f59e0b',
              marginBottom: '24px'
            }}>
              {getOverallScore()}%
            </div>
            <p style={{
              fontSize: '16px', color: '#6b7280',
              marginBottom: '32px'
            }}>
              {getOverallScore() >= 80
                ? "Excellent! You're ready to apply! 🌟"
                : getOverallScore() >= 60
                  ? "Good job! Keep practicing! 👍"
                  : "Keep practicing! You'll get better! 💪"}
            </p>
            <button
              onClick={() => {
                setStarted(false)
                setCompleted(false)
                setSession(null)
                setAnswer('')
                setFeedback(null)
              }}
              style={{
                padding: '14px 40px',
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                color: 'white', border: 'none', borderRadius: '12px',
                fontSize: '16px', fontWeight: '700', cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(99,102,241,0.4)'
              }}
            >
              🔄 Practice Again
            </button>
          </div>
        )}

        {/* Interview In Progress */}
        {started && !completed && session && (
          <div>
            {/* Progress */}
            <div style={{
              background: 'white', borderRadius: '14px',
              padding: '1.25rem 1.5rem', marginBottom: '1.5rem',
              border: '1px solid #e5e7eb',
              boxShadow: '0 2px 10px rgba(0,0,0,0.04)'
            }}>
              <div style={{
                display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', marginBottom: '10px'
              }}>
                <span style={{ fontWeight: '700', fontSize: '15px', color: '#1a1a1a' }}>
                  Question {currentQ + 1} of {session.questions.length}
                </span>
                <span style={{
                  background: '#ede9fe', color: '#6d28d9',
                  padding: '4px 14px', borderRadius: '20px',
                  fontSize: '13px', fontWeight: '600'
                }}>
                  {session.questions[currentQ]?.category}
                </span>
              </div>
              <div style={{
                height: '8px', background: '#f3f4f6',
                borderRadius: '4px', overflow: 'hidden'
              }}>
                <div style={{
                  height: '100%',
                  background: 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                  width: `${((currentQ + 1) / session.questions.length) * 100}%`,
                  transition: 'width 0.5s ease',
                  borderRadius: '4px'
                }} />
              </div>
            </div>

            {/* Question Card */}
            <div style={{
              background: 'linear-gradient(135deg, #f8f7ff, #ede9fe)',
              borderRadius: '16px', padding: '2rem',
              marginBottom: '1.5rem',
              border: '1px solid #c4b5fd'
            }}>
              <p style={{
                fontSize: '13px', color: '#6d28d9',
                fontWeight: '700', marginBottom: '10px',
                textTransform: 'uppercase', letterSpacing: '1px'
              }}>
                Question {currentQ + 1}
              </p>
              <h3 style={{
                fontSize: '19px', fontWeight: '600',
                color: '#1a1a1a', lineHeight: '1.7'
              }}>
                {session.questions[currentQ]?.question}
              </h3>
            </div>

            {/* Answer Section */}
            {!feedback && (
              <div style={{
                background: 'white', borderRadius: '16px',
                padding: '1.5rem', border: '1px solid #e5e7eb',
                marginBottom: '1rem',
                boxShadow: '0 2px 10px rgba(0,0,0,0.04)'
              }}>
                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  alignItems: 'center', marginBottom: '16px'
                }}>
                  <h4 style={{ fontWeight: '700', color: '#374151' }}>
                    Your Answer
                  </h4>
                  {/* Toggle input mode */}
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      onClick={() => setInputMode('text')}
                      style={{
                        padding: '6px 14px',
                        background: inputMode === 'text' ? '#6366f1' : '#f3f4f6',
                        color: inputMode === 'text' ? 'white' : '#6b7280',
                        border: 'none', borderRadius: '20px',
                        fontSize: '12px', fontWeight: '600', cursor: 'pointer'
                      }}
                    >
                      ⌨️ Type
                    </button>
                    <button
                      onClick={() => setInputMode('mic')}
                      style={{
                        padding: '6px 14px',
                        background: inputMode === 'mic' ? '#6366f1' : '#f3f4f6',
                        color: inputMode === 'mic' ? 'white' : '#6b7280',
                        border: 'none', borderRadius: '20px',
                        fontSize: '12px', fontWeight: '600', cursor: 'pointer'
                      }}
                    >
                      🎤 Speak
                    </button>
                  </div>
                </div>

                {/* Mic Mode */}
                {inputMode === 'mic' && (
                  <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                    <MicAnimation isActive={isListening} />
                    <button
                      onClick={startListening}
                      disabled={isListening}
                      style={{
                        padding: '12px 32px',
                        background: isListening
                          ? '#9ca3af'
                          : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                        color: 'white', border: 'none',
                        borderRadius: '25px', fontSize: '15px',
                        fontWeight: '600', cursor: isListening
                          ? 'not-allowed' : 'pointer',
                        marginBottom: '12px'
                      }}
                    >
                      {isListening ? '🔴 Listening...' : '🎤 Start Speaking'}
                    </button>
                  </div>
                )}

                {/* Text Area */}
                <textarea
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  placeholder={inputMode === 'mic'
                    ? 'Your speech will appear here...'
                    : 'Type your answer here...'}
                  rows={5}
                  style={{
                    width: '100%', padding: '16px',
                    border: '2px solid #e5e7eb', borderRadius: '12px',
                    fontSize: '15px', outline: 'none',
                    resize: 'vertical', boxSizing: 'border-box',
                    fontFamily: 'inherit', lineHeight: '1.7',
                    color: '#374151', background: '#f9fafb'
                  }}
                  onFocus={e => e.target.style.borderColor = '#6366f1'}
                  onBlur={e => e.target.style.borderColor = '#e5e7eb'}
                />

                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  alignItems: 'center', marginTop: '12px'
                }}>
                  <span style={{ fontSize: '13px', color: '#9ca3af' }}>
                    {answer.length} characters
                  </span>
                  <button
                    onClick={submitAnswer}
                    disabled={loading || !answer.trim()}
                    style={{
                      padding: '12px 32px',
                      background: !answer.trim() ? '#e5e7eb'
                        : 'linear-gradient(135deg, #10b981, #059669)',
                      color: !answer.trim() ? '#9ca3af' : 'white',
                      border: 'none', borderRadius: '10px',
                      fontSize: '15px', fontWeight: '700',
                      cursor: !answer.trim() ? 'not-allowed' : 'pointer',
                      boxShadow: !answer.trim() ? 'none'
                        : '0 4px 15px rgba(16,185,129,0.4)',
                      transition: 'all 0.2s'
                    }}
                  >
                    {loading ? '⏳ Evaluating...' : '📤 Submit Answer'}
                  </button>
                </div>
              </div>
            )}

            {/* Feedback */}
            {feedback && (
              <div style={{
                background: 'white', borderRadius: '16px',
                padding: '1.5rem', border: '1px solid #e5e7eb',
                marginBottom: '1.5rem',
                boxShadow: '0 4px 20px rgba(0,0,0,0.06)',
                animation: 'fadeIn 0.4s ease'
              }}>
                {/* Score Header */}
                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  alignItems: 'center', marginBottom: '1.5rem',
                  padding: '1rem',
                  background: feedback.score >= 7 ? '#ecfdf5' : '#fef2f2',
                  borderRadius: '12px'
                }}>
                  <div>
                    <p style={{
                      fontSize: '13px',
                      color: feedback.score >= 7 ? '#065f46' : '#dc2626',
                      fontWeight: '600', marginBottom: '2px'
                    }}>
                      AI Evaluation
                    </p>
                    <p style={{
                      fontSize: '14px',
                      color: feedback.score >= 7 ? '#065f46' : '#dc2626'
                    }}>
                      {feedback.score >= 9 ? 'Excellent! 🌟'
                        : feedback.score >= 7 ? 'Good Answer! 👍'
                        : feedback.score >= 5 ? 'Average 📈'
                        : 'Needs Improvement 💡'}
                    </p>
                  </div>
                  <div style={{
                    fontSize: '48px', fontWeight: '900',
                    color: feedback.score >= 7 ? '#10b981' : '#f59e0b'
                  }}>
                    {feedback.score}
                    <span style={{ fontSize: '20px', fontWeight: '500', color: '#6b7280' }}>
                      /10
                    </span>
                  </div>
                </div>

                {/* Strengths */}
                <div style={{
                  marginBottom: '16px', padding: '14px',
                  background: '#f0fdf4', borderRadius: '10px',
                  border: '1px solid #bbf7d0'
                }}>
                  <p style={{
                    fontWeight: '700', color: '#065f46',
                    marginBottom: '8px', fontSize: '14px'
                  }}>
                    ✅ Strengths
                  </p>
                  {feedback.strengths?.map((s, i) => (
                    <p key={i} style={{
                      color: '#166534', fontSize: '14px',
                      marginBottom: '4px', paddingLeft: '8px',
                      lineHeight: '1.5'
                    }}>
                      • {s}
                    </p>
                  ))}
                </div>

                {/* Improvements */}
                <div style={{
                  marginBottom: '16px', padding: '14px',
                  background: '#fff7ed', borderRadius: '10px',
                  border: '1px solid #fed7aa'
                }}>
                  <p style={{
                    fontWeight: '700', color: '#c2410c',
                    marginBottom: '8px', fontSize: '14px'
                  }}>
                    💡 Areas to Improve
                  </p>
                  {feedback.improvements?.map((s, i) => (
                    <p key={i} style={{
                      color: '#9a3412', fontSize: '14px',
                      marginBottom: '4px', paddingLeft: '8px',
                      lineHeight: '1.5'
                    }}>
                      • {s}
                    </p>
                  ))}
                </div>

                {/* Encouragement */}
                <div style={{
                  padding: '14px',
                  background: 'linear-gradient(135deg, #eff6ff, #dbeafe)',
                  borderRadius: '10px', marginBottom: '20px',
                  border: '1px solid #bfdbfe'
                }}>
                  <p style={{
                    color: '#1d4ed8', fontSize: '14px',
                    fontWeight: '600', lineHeight: '1.5'
                  }}>
                    💪 {feedback.encouragement}
                  </p>
                </div>

                <button
                  onClick={nextQuestion}
                  style={{
                    width: '100%', padding: '14px',
                    background: currentQ < session.questions.length - 1
                      ? 'linear-gradient(135deg, #10b981, #059669)'
                      : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                    color: 'white', border: 'none', borderRadius: '12px',
                    fontSize: '16px', fontWeight: '700', cursor: 'pointer',
                    boxShadow: '0 4px 15px rgba(16,185,129,0.3)',
                    transition: 'all 0.2s'
                  }}
                >
                  {currentQ < session.questions.length - 1
                    ? 'Next Question →'
                    : '🎉 Complete Interview'}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Interview
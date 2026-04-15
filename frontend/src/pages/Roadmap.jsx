import { useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import API from '../api/axios'

function Roadmap() {
  const [role, setRole] = useState('ML Engineer')
  const [weeks, setWeeks] = useState(12)
  const [loading, setLoading] = useState(false)
  const [roadmap, setRoadmap] = useState(null)
  const [error, setError] = useState('')

  const generateRoadmap = async () => {
    setLoading(true)
    setError('')
    setRoadmap(null)
    try {
      const response = await API.post('/roadmap/generate', {
        target_role: role,
        timeline_weeks: weeks
      })

      // Debug
      console.log('Full API Response:', response.data)
      console.log('Roadmap data:', response.data.roadmap)
      console.log('Weekly plan:', response.data.roadmap?.weekly_plan)

      setRoadmap(response.data)
    } catch (err) {
      console.error('Error:', err)
      setError(err.response?.data?.detail || 'Generation failed!')
    }
    setLoading(false)
  }

  // Weekly plan safe access
  const weeklyPlan = roadmap?.roadmap?.weekly_plan ||
    roadmap?.weekly_plan || []

  const summaryText = roadmap?.skill_gap_summary ||
    roadmap?.roadmap?.final_goal || ''

  const roadmapTitle = roadmap?.roadmap?.roadmap_title ||
    `Journey to ${role}`

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <Navbar active="roadmap" />
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>

        {/* Header */}
        <div style={{
          background: 'linear-gradient(135deg, #667eea, #764ba2)',
          borderRadius: '20px', padding: '2rem',
          color: 'white', marginBottom: '2rem',
          boxShadow: '0 10px 40px rgba(102,126,234,0.3)'
        }}>
          <h1 style={{ fontSize: '28px', fontWeight: '800', marginBottom: '8px' }}>
            🗺️ Career Roadmap Generator
          </h1>
          <p style={{ opacity: '0.85', fontSize: '16px' }}>
            Get your personalized weekly learning plan powered by AI!
          </p>
        </div>

        {/* Input Card */}
        <div style={{
          background: 'white', borderRadius: '16px',
          padding: '2rem', marginBottom: '2rem',
          border: '1px solid #e5e7eb',
          boxShadow: '0 4px 20px rgba(0,0,0,0.05)'
        }}>
          <h2 style={{
            fontSize: '18px', fontWeight: '700',
            marginBottom: '1.5rem', color: '#374151'
          }}>
            Configure Your Roadmap
          </h2>

          <div style={{
            display: 'flex', gap: '16px',
            flexWrap: 'wrap', marginBottom: '20px'
          }}>
            {/* Role Input */}
            <div style={{ flex: 1, minWidth: '200px' }}>
              <label style={{
                display: 'block', fontSize: '13px',
                fontWeight: '600', color: '#6b7280',
                marginBottom: '8px', textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Target Role
              </label>
              <input
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g. ML Engineer, Full Stack Dev"
                style={{
                  width: '100%', padding: '12px 16px',
                  border: '2px solid #e5e7eb', borderRadius: '10px',
                  fontSize: '15px', outline: 'none',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            {/* Timeline Dropdown */}
            <div style={{ minWidth: '180px' }}>
              <label style={{
                display: 'block', fontSize: '13px',
                fontWeight: '600', color: '#6b7280',
                marginBottom: '8px', textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Timeline
              </label>
              <select
                value={weeks}
                onChange={(e) => setWeeks(Number(e.target.value))}
                style={{
                  width: '100%', padding: '12px 16px',
                  border: '2px solid #e5e7eb', borderRadius: '10px',
                  fontSize: '15px', outline: 'none',
                  background: 'white', cursor: 'pointer'
                }}
              >
                <option value={8}>8 weeks (2 months)</option>
                <option value={12}>12 weeks (3 months)</option>
                <option value={16}>16 weeks (4 months)</option>
                <option value={24}>24 weeks (6 months)</option>
              </select>
            </div>
          </div>

          <button
            onClick={generateRoadmap}
            disabled={loading || !role.trim()}
            style={{
              padding: '14px 40px',
              background: loading ? '#9ca3af'
                : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: 'white', border: 'none', borderRadius: '10px',
              fontSize: '16px', fontWeight: '700',
              cursor: loading ? 'not-allowed' : 'pointer',
              boxShadow: loading ? 'none'
                : '0 4px 15px rgba(99,102,241,0.4)'
            }}
          >
            {loading ? '⏳ Generating your roadmap...' : '🗺️ Generate My Roadmap'}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div style={{
            background: '#fef2f2', border: '1px solid #fca5a5',
            color: '#dc2626', padding: '14px 16px',
            borderRadius: '10px', marginBottom: '1rem', fontSize: '14px'
          }}>
            ❌ {error}
          </div>
        )}

        {/* Results */}
        {roadmap && (
          <div>

            {/* Summary Card */}
            <div style={{
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              borderRadius: '20px', padding: '2rem',
              color: 'white', marginBottom: '2rem',
              boxShadow: '0 10px 30px rgba(99,102,241,0.3)'
            }}>
              <h2 style={{
                fontSize: '22px', fontWeight: '800', marginBottom: '16px'
              }}>
                {roadmapTitle}
              </h2>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '12px'
              }}>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  borderRadius: '12px', padding: '14px'
                }}>
                  <p style={{ fontSize: '12px', opacity: '0.8', marginBottom: '4px' }}>
                    Current Match
                  </p>
                  <p style={{ fontSize: '24px', fontWeight: '800' }}>
                    {roadmap.current_match || '0%'}
                  </p>
                </div>

                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  borderRadius: '12px', padding: '14px'
                }}>
                  <p style={{ fontSize: '12px', opacity: '0.8', marginBottom: '4px' }}>
                    Timeline
                  </p>
                  <p style={{ fontSize: '24px', fontWeight: '800' }}>
                    {weeks} weeks
                  </p>
                </div>

                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  borderRadius: '12px', padding: '14px',
                  gridColumn: 'span 2'
                }}>
                  <p style={{ fontSize: '12px', opacity: '0.8', marginBottom: '4px' }}>
                    Summary
                  </p>
                  <p style={{ fontSize: '14px', fontWeight: '500', lineHeight: '1.5' }}>
                    {summaryText || `${weeks}-week roadmap to become ${role}`}
                  </p>
                </div>
              </div>
            </div>

            {/* Missing Skills */}
            {roadmap.missing_skills?.length > 0 && (
              <div style={{
                background: 'white', borderRadius: '16px',
                padding: '1.5rem', border: '1px solid #e5e7eb',
                marginBottom: '1.5rem'
              }}>
                <h3 style={{
                  fontSize: '18px', fontWeight: '700',
                  marginBottom: '14px', color: '#1a1a1a'
                }}>
                  📚 Skills to Master
                </h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {roadmap.missing_skills.map((skill, i) => (
                    <span key={i} style={{
                      background: '#fef3c7', color: '#92400e',
                      padding: '6px 14px', borderRadius: '20px',
                      fontSize: '13px', fontWeight: '600',
                      border: '1px solid #fcd34d'
                    }}>
                      📌 {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Weekly Plan */}
            <h3 style={{
              fontSize: '22px', fontWeight: '800',
              marginBottom: '1rem', color: '#1a1a1a'
            }}>
              📅 Your Weekly Learning Plan
            </h3>

            {weeklyPlan.length === 0 ? (
              <div style={{
                background: 'white', borderRadius: '12px',
                padding: '2rem', textAlign: 'center',
                border: '1px solid #e5e7eb', color: '#6b7280'
              }}>
                <p>No weekly plan available. Try generating again!</p>
                <p style={{ fontSize: '12px', marginTop: '8px' }}>
                  Debug: {JSON.stringify(Object.keys(roadmap))}
                </p>
              </div>
            ) : (
              <div style={{
                display: 'flex', flexDirection: 'column', gap: '16px'
              }}>
                {weeklyPlan.map((week, i) => (
                  <div key={i} style={{
                    background: 'white', borderRadius: '14px',
                    padding: '1.5rem', border: '1px solid #e5e7eb',
                    borderLeft: `5px solid ${
                      i < Math.floor(weeks/3) ? '#6366f1'
                        : i < Math.floor(weeks * 2/3) ? '#10b981'
                        : '#f59e0b'
                    }`,
                    boxShadow: '0 2px 10px rgba(0,0,0,0.04)'
                  }}>
                    {/* Week Header */}
                    <div style={{
                      display: 'flex', justifyContent: 'space-between',
                      alignItems: 'center', marginBottom: '12px',
                      flexWrap: 'wrap', gap: '8px'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <div style={{
                          background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                          color: 'white', width: '36px', height: '36px',
                          borderRadius: '50%', display: 'flex',
                          alignItems: 'center', justifyContent: 'center',
                          fontSize: '14px', fontWeight: '800', flexShrink: 0
                        }}>
                          {week.week || i + 1}
                        </div>
                        <div>
                          <h4 style={{
                            fontSize: '16px', fontWeight: '700',
                            color: '#1a1a1a', marginBottom: '2px'
                          }}>
                            Week {week.week || i + 1}: {week.theme || week.title || 'Learning Phase'}
                          </h4>
                          {week.phase && (
                            <span style={{
                              fontSize: '11px', color: '#6d28d9',
                              fontWeight: '600', background: '#ede9fe',
                              padding: '2px 8px', borderRadius: '10px'
                            }}>
                              {week.phase}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Goal & Project */}
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: '1fr 1fr',
                      gap: '10px', marginBottom: '12px'
                    }}>
                      <div style={{
                        background: '#f0f9ff', borderRadius: '10px',
                        padding: '10px 14px', border: '1px solid #bae6fd'
                      }}>
                        <p style={{
                          fontSize: '11px', fontWeight: '700',
                          color: '#0369a1', marginBottom: '4px',
                          textTransform: 'uppercase'
                        }}>
                          🎯 Goal
                        </p>
                        <p style={{ fontSize: '13px', color: '#1a1a1a' }}>
                          {week.goal || 'Complete weekly objectives'}
                        </p>
                      </div>

                      <div style={{
                        background: '#f0fdf4', borderRadius: '10px',
                        padding: '10px 14px', border: '1px solid #bbf7d0'
                      }}>
                        <p style={{
                          fontSize: '11px', fontWeight: '700',
                          color: '#15803d', marginBottom: '4px',
                          textTransform: 'uppercase'
                        }}>
                          🔨 Project
                        </p>
                        <p style={{ fontSize: '13px', color: '#1a1a1a' }}>
                          {week.project || 'Hands-on practice'}
                        </p>
                      </div>
                    </div>

                    {/* Day-wise Topics */}
                    {week.daily_tasks && week.daily_tasks.length > 0 && (
                      <div style={{ marginBottom: '12px' }}>
                        <p style={{
                          fontSize: '12px', fontWeight: '700',
                          color: '#6b7280', marginBottom: '8px',
                          textTransform: 'uppercase', letterSpacing: '0.5px'
                        }}>
                          📆 Daily Tasks
                        </p>
                        <div style={{
                          display: 'flex', flexDirection: 'column', gap: '6px'
                        }}>
                          {week.daily_tasks.map((task, j) => (
                            <div key={j} style={{
                              display: 'flex', alignItems: 'flex-start',
                              gap: '8px', padding: '8px 12px',
                              background: '#f9fafb', borderRadius: '8px',
                              fontSize: '13px', color: '#374151'
                            }}>
                              <span style={{
                                background: '#6366f1', color: 'white',
                                minWidth: '20px', height: '20px',
                                borderRadius: '50%', display: 'flex',
                                alignItems: 'center', justifyContent: 'center',
                                fontSize: '10px', fontWeight: '700',
                                flexShrink: 0
                              }}>
                                {j + 1}
                              </span>
                              {task}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Skills */}
                    {week.skills_to_learn?.length > 0 && (
                      <div>
                        <p style={{
                          fontSize: '12px', fontWeight: '700',
                          color: '#6b7280', marginBottom: '8px',
                          textTransform: 'uppercase', letterSpacing: '0.5px'
                        }}>
                          ⚡ Skills This Week
                        </p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                          {week.skills_to_learn.map((skill, j) => (
                            <span key={j} style={{
                              background: '#eff6ff', color: '#1d4ed8',
                              padding: '4px 12px', borderRadius: '20px',
                              fontSize: '12px', fontWeight: '600',
                              border: '1px solid #bfdbfe'
                            }}>
                              ⚡ {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Resources */}
                    {week.resources?.length > 0 && (
                      <div style={{ marginTop: '10px' }}>
                        <p style={{
                          fontSize: '12px', fontWeight: '700',
                          color: '#6b7280', marginBottom: '8px',
                          textTransform: 'uppercase', letterSpacing: '0.5px'
                        }}>
                          📖 Resources
                        </p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                          {week.resources.map((resource, j) => (
                            <span key={j} style={{
                              background: '#fef3c7', color: '#92400e',
                              padding: '4px 12px', borderRadius: '20px',
                              fontSize: '12px', fontWeight: '500',
                              border: '1px solid #fcd34d'
                            }}>
                              📚 {resource}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Pro Tips */}
            {(roadmap.roadmap?.tips || roadmap.tips)?.length > 0 && (
              <div style={{
                background: 'linear-gradient(135deg, #ecfdf5, #d1fae5)',
                borderRadius: '16px', padding: '1.5rem',
                border: '1px solid #6ee7b7', marginTop: '1.5rem'
              }}>
                <h3 style={{
                  fontSize: '18px', fontWeight: '700',
                  marginBottom: '12px', color: '#065f46'
                }}>
                  💡 Pro Tips for Success
                </h3>
                {(roadmap.roadmap?.tips || roadmap.tips).map((tip, i) => (
                  <p key={i} style={{
                    fontSize: '14px', color: '#065f46',
                    padding: '8px 0', lineHeight: '1.6',
                    borderBottom: '1px solid #a7f3d0'
                  }}>
                    ✅ {tip}
                  </p>
                ))}
              </div>
            )}

            {/* Final Goal */}
            {(roadmap.roadmap?.final_goal) && (
              <div style={{
                background: 'linear-gradient(135deg, #1e1b4b, #312e81)',
                borderRadius: '16px', padding: '1.5rem 2rem',
                color: 'white', marginTop: '1.5rem',
                textAlign: 'center'
              }}>
                <p style={{ fontSize: '14px', opacity: '0.7', marginBottom: '8px' }}>
                  🏆 Final Goal
                </p>
                <p style={{ fontSize: '18px', fontWeight: '700', lineHeight: '1.5' }}>
                  {roadmap.roadmap.final_goal}
                </p>
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  )
}

export default Roadmap
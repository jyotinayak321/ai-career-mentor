import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar.jsx'
import API from '../api/axios'

function Dashboard() {
  const [user, setUser] = useState(null)
  const [tips, setTips] = useState(null)
  const [skillGap, setSkillGap] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const userData = JSON.parse(
        localStorage.getItem('user') || '{}'
      )
      setUser(userData)

      // Career tips fetch karo
      const tipsRes = await API.get('/agent/tips')
      setTips(tipsRes.data)

      // Skill gap fetch karo
      const gapRes = await API.get(
        '/jobs/analysis?target_role=software engineer'
      )
      setSkillGap(gapRes.data?.skill_gap)

    } catch (err) {
      console.error('Dashboard load error:', err)
    }
    setLoading(false)
  }

  if (loading) {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        height: '100vh', gap: '16px', color: '#6b7280'
      }}>
        <div style={styles.spinner}></div>
        <p>Loading your dashboard... ⏳</p>
      </div>
    )
  }

  const quickActions = [
    { icon: '📤', title: 'Upload Resume', desc: 'AI se instant feedback lo', color: '#6366f1', path: '/resume' },
    { icon: '💼', title: 'Find Jobs', desc: 'Matching jobs dekho', color: '#10b981', path: '/jobs' },
    { icon: '🗺️', title: 'Career Roadmap', desc: 'Weekly learning plan lo', color: '#f59e0b', path: '/roadmap' },
    { icon: '🎤', title: 'Mock Interview', desc: 'AI se practice karo', color: '#ef4444', path: '/interview' }
  ]

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <Navbar active="dashboard" />
      <div style={styles.content}>

        {/* Welcome */}
        <div style={styles.welcomeSection}>
          <h1 style={styles.welcomeTitle}>
            Namaste, {user?.name || 'Friend'}! 👋
          </h1>
          <p style={styles.welcomeSubtitle}>
            Your AI-powered career journey starts here!
          </p>
        </div>

        {/* Stats Cards */}
        <div style={styles.statsGrid}>
          <div style={{ ...styles.statCard, borderLeft: '4px solid #6366f1' }}>
            <div style={styles.statIcon}>📄</div>
            <div>
              <p style={styles.statLabel}>Resume Score</p>
              <p style={{ ...styles.statValue, color: '#6366f1' }}>
                {tips?.resume_score ? `${tips.resume_score}/100` : 'Upload karo!'}
              </p>
            </div>
          </div>

          <div style={{ ...styles.statCard, borderLeft: '4px solid #10b981' }}>
            <div style={styles.statIcon}>⚡</div>
            <div>
              <p style={styles.statLabel}>Skills Found</p>
              <p style={{ ...styles.statValue, color: '#10b981' }}>
                {tips?.skills_count || 0} skills
              </p>
            </div>
          </div>

          <div style={{ ...styles.statCard, borderLeft: '4px solid #f59e0b' }}>
            <div style={styles.statIcon}>🎯</div>
            <div>
              <p style={styles.statLabel}>Career Match</p>
              <p style={{ ...styles.statValue, color: '#f59e0b' }}>
                {skillGap?.match_percentage
                  ? `${skillGap.match_percentage}%`
                  : 'Calculating...'}
              </p>
            </div>
          </div>

          <div style={{ ...styles.statCard, borderLeft: '4px solid #8b5cf6' }}>
            <div style={styles.statIcon}>👤</div>
            <div>
              <p style={styles.statLabel}>Account</p>
              <p style={{ ...styles.statValue, color: '#8b5cf6', fontSize: '13px' }}>
                {user?.email || ''}
              </p>
            </div>
          </div>
        </div>

        {/* ---------------------------------------- */}
        {/* SKILL GAP SECTION */}
        {/* ---------------------------------------- */}
        {skillGap && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>
              🎯 Skill Gap Analysis
            </h2>

            <div style={{
              background: 'white', borderRadius: '16px',
              padding: '1.5rem', border: '1px solid #e5e7eb',
              boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
            }}>
              {/* Readiness Level */}
              <div style={{
                display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', marginBottom: '1.5rem',
                flexWrap: 'wrap', gap: '12px'
              }}>
                <div>
                  <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '4px' }}>
                    Career Readiness Level
                  </p>
                  <p style={{ fontSize: '22px', fontWeight: '700', color: '#1a1a1a' }}>
                    {skillGap.readiness_level}
                  </p>
                </div>

                {/* Match Score Circle */}
                <div style={{
                  width: '80px', height: '80px',
                  borderRadius: '50%',
                  background: `conic-gradient(
                    #6366f1 ${skillGap.match_percentage * 3.6}deg,
                    #e5e7eb 0deg
                  )`,
                  display: 'flex', alignItems: 'center',
                  justifyContent: 'center', position: 'relative'
                }}>
                  <div style={{
                    width: '60px', height: '60px',
                    borderRadius: '50%', background: 'white',
                    display: 'flex', alignItems: 'center',
                    justifyContent: 'center', position: 'absolute'
                  }}>
                    <span style={{ fontSize: '14px', fontWeight: '800', color: '#6366f1' }}>
                      {skillGap.match_percentage}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  marginBottom: '6px'
                }}>
                  <span style={{ fontSize: '13px', color: '#6b7280' }}>
                    Overall Match
                  </span>
                  <span style={{ fontSize: '13px', fontWeight: '600', color: '#6366f1' }}>
                    {skillGap.match_percentage}%
                  </span>
                </div>
                <div style={{
                  height: '10px', background: '#f3f4f6',
                  borderRadius: '5px', overflow: 'hidden'
                }}>
                  <div style={{
                    height: '100%',
                    width: `${skillGap.match_percentage}%`,
                    background: 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                    borderRadius: '5px',
                    transition: 'width 1s ease'
                  }} />
                </div>
              </div>

              {/* Skills Grid */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '16px'
              }}>

                {/* Strong Skills */}
                {skillGap.gap_analysis?.existing_essential?.length > 0 && (
                  <div style={{
                    background: '#f0fdf4', borderRadius: '12px',
                    padding: '1rem', border: '1px solid #bbf7d0'
                  }}>
                    <p style={{
                      fontSize: '13px', fontWeight: '700',
                      color: '#065f46', marginBottom: '10px'
                    }}>
                      ✅ Strong Skills ({skillGap.gap_analysis.existing_essential.length})
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {skillGap.gap_analysis.existing_essential.map((s, i) => (
                        <span key={i} style={{
                          background: '#dcfce7', color: '#166534',
                          padding: '3px 10px', borderRadius: '20px',
                          fontSize: '12px', fontWeight: '600'
                        }}>
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Missing Essential Skills */}
                {skillGap.gap_analysis?.missing_essential?.length > 0 && (
                  <div style={{
                    background: '#fef2f2', borderRadius: '12px',
                    padding: '1rem', border: '1px solid #fca5a5'
                  }}>
                    <p style={{
                      fontSize: '13px', fontWeight: '700',
                      color: '#dc2626', marginBottom: '10px'
                    }}>
                      ❌ Must Learn ({skillGap.gap_analysis.missing_essential.length})
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {skillGap.gap_analysis.missing_essential.map((s, i) => (
                        <span key={i} style={{
                          background: '#fee2e2', color: '#dc2626',
                          padding: '3px 10px', borderRadius: '20px',
                          fontSize: '12px', fontWeight: '600'
                        }}>
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Missing Important Skills */}
                {skillGap.gap_analysis?.missing_important?.length > 0 && (
                  <div style={{
                    background: '#fef3c7', borderRadius: '12px',
                    padding: '1rem', border: '1px solid #fcd34d'
                  }}>
                    <p style={{
                      fontSize: '13px', fontWeight: '700',
                      color: '#92400e', marginBottom: '10px'
                    }}>
                      💡 Good to Learn ({skillGap.gap_analysis.missing_important.length})
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {skillGap.gap_analysis.missing_important.map((s, i) => (
                        <span key={i} style={{
                          background: '#fde68a', color: '#92400e',
                          padding: '3px 10px', borderRadius: '20px',
                          fontSize: '12px', fontWeight: '600'
                        }}>
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Summary */}
              {skillGap.summary && (
                <div style={{
                  marginTop: '1rem', padding: '12px 16px',
                  background: '#eff6ff', borderRadius: '10px',
                  border: '1px solid #bfdbfe'
                }}>
                  <p style={{ fontSize: '14px', color: '#1d4ed8', lineHeight: '1.6' }}>
                    💡 {skillGap.summary}
                  </p>
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={() => navigate('/roadmap')}
                style={{
                  marginTop: '1rem', padding: '12px 24px',
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  color: 'white', border: 'none', borderRadius: '10px',
                  fontSize: '14px', fontWeight: '700', cursor: 'pointer',
                  boxShadow: '0 4px 15px rgba(99,102,241,0.3)'
                }}
              >
                🗺️ Generate Learning Roadmap
              </button>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Quick Actions</h2>
          <div style={styles.actionsGrid}>
            {quickActions.map((action, index) => (
              <ActionCard
                key={index}
                action={action}
                onClick={() => navigate(action.path)}
              />
            ))}
          </div>
        </div>

        {/* AI Tips */}
        {tips?.personalized_tips && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>💡 Personalized Tips</h2>
            <div style={styles.tipsGrid}>
              {tips.personalized_tips.map((tip, i) => (
                <div key={i} style={styles.tipCard}>{tip}</div>
              ))}
            </div>
          </div>
        )}

        {/* Motivation Banner */}
        <div style={styles.banner}>
          <h3 style={styles.bannerTitle}>🚀 Today's Goal</h3>
          <p style={styles.bannerText}>
            Consistency beats intensity!
            Practice 1-2 hours daily.
            Small steps lead to big achievements! 💪
          </p>
        </div>

      </div>
    </div>
  )
}

function ActionCard({ action, onClick }) {
  const [hovered, setHovered] = useState(false)
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: 'white',
        border: `1.5px solid ${hovered ? action.color : '#e5e7eb'}`,
        borderRadius: '12px', padding: '1.5rem',
        cursor: 'pointer', transition: 'all 0.2s',
        transform: hovered ? 'translateY(-4px)' : 'none',
        boxShadow: hovered ? `0 8px 25px ${action.color}30` : '0 2px 8px rgba(0,0,0,0.06)'
      }}
    >
      <div style={{ fontSize: '32px', marginBottom: '10px' }}>{action.icon}</div>
      <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1a1a1a', marginBottom: '6px' }}>
        {action.title}
      </h3>
      <p style={{ fontSize: '13px', color: '#6b7280' }}>{action.desc}</p>
    </div>
  )
}

const styles = {
  content: { maxWidth: '1100px', margin: '0 auto', padding: '2rem' },
  spinner: {
    width: '40px', height: '40px',
    border: '4px solid #e5e7eb', borderTop: '4px solid #6366f1',
    borderRadius: '50%', animation: 'spin 0.8s linear infinite'
  },
  welcomeSection: { marginBottom: '2rem' },
  welcomeTitle: { fontSize: '28px', fontWeight: '700', color: '#1a1a1a', marginBottom: '6px' },
  welcomeSubtitle: { color: '#6b7280', fontSize: '16px' },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px', marginBottom: '2rem'
  },
  statCard: {
    background: 'white', borderRadius: '12px', padding: '1.25rem',
    display: 'flex', alignItems: 'center', gap: '16px',
    border: '1px solid #e5e7eb'
  },
  statIcon: { fontSize: '28px' },
  statLabel: { fontSize: '13px', color: '#6b7280', marginBottom: '4px' },
  statValue: { fontSize: '20px', fontWeight: '700' },
  section: { marginBottom: '2rem' },
  sectionTitle: { fontSize: '20px', fontWeight: '700', color: '#1a1a1a', marginBottom: '1rem' },
  actionsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
    gap: '16px'
  },
  tipsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '12px'
  },
  tipCard: {
    background: 'white', border: '1px solid #e5e7eb',
    borderRadius: '10px', padding: '1rem',
    fontSize: '14px', color: '#374151', lineHeight: '1.6'
  },
  banner: {
    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    borderRadius: '16px', padding: '1.5rem 2rem', color: 'white'
  },
  bannerTitle: { fontSize: '18px', fontWeight: '700', marginBottom: '8px' },
  bannerText: { fontSize: '15px', lineHeight: '1.6', opacity: '0.95' }
}

export default Dashboard
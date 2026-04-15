import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar.jsx'
import API from '../api/axios'

const getMatchColor = (score) => {
  if (score >= 80) return { bg: '#ecfdf5', color: '#065f46', border: '#6ee7b7' }
  if (score >= 60) return { bg: '#eff6ff', color: '#1d4ed8', border: '#bfdbfe' }
  if (score >= 40) return { bg: '#fef3c7', color: '#92400e', border: '#fcd34d' }
  return { bg: '#fef2f2', color: '#dc2626', border: '#fca5a5' }
}

const getDaysLeft = (dateStr) => {
  if (!dateStr) return null
  const today = new Date()
  const deadline = new Date(dateStr)
  const diff = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24))
  return diff
}

function JobSearch() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [role, setRole] = useState('')
  const [location, setLocation] = useState('India')
  const [expandedJob, setExpandedJob] = useState(null)
  const [filter, setFilter] = useState('all')

  useEffect(() => { loadJobs() }, [])

  const loadJobs = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (role) params.append('role', role)
      if (location) params.append('location', location)
      const response = await API.get(`/jobs/recommend?${params}`)
      setJobs(response.data.jobs || [])
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const popularRoles = [
    'ML Engineer', 'Software Engineer', 'Data Scientist',
    'Full Stack Developer', 'AI Engineer', 'Backend Developer',
    'Frontend Developer', 'DevOps Engineer', 'Defence AI',
    'GenAI Engineer', 'NLP Engineer', 'Prompt Engineer'
  ]

  const filteredJobs = jobs.filter(job => {
    if (filter === 'remote') return job.remote === true
    if (filter === 'fresher') return job.experience === 'Fresher' || job.experience?.includes('0')
    if (filter === 'internship') return job.job_type === 'Internship'
    if (filter === 'defence') return job.title?.toLowerCase().includes('defence') || job.company?.toLowerCase().includes('drdo') || job.company?.toLowerCase().includes('idex')
    return true
  })

  const portals = [
    { name: 'LinkedIn Jobs', desc: 'Professional jobs', url: 'https://www.linkedin.com/jobs/search/?location=India', color: '#0077b5', icon: '💼' },
    { name: 'Naukri.com', desc: 'India largest portal', url: 'https://www.naukri.com/', color: '#ff7555', icon: '🎯' },
    { name: 'Indeed India', desc: 'Millions of listings', url: 'https://in.indeed.com/', color: '#003a9b', icon: '🔍' },
    { name: 'Glassdoor', desc: 'Jobs with reviews', url: 'https://www.glassdoor.co.in/', color: '#0caa41', icon: '⭐' },
    { name: 'Internshala', desc: 'Fresher and intern', url: 'https://internshala.com/jobs/', color: '#0058d6', icon: '🎓' },
    { name: 'Wellfound', desc: 'Startup jobs', url: 'https://wellfound.com/jobs', color: '#ff5722', icon: '🚀' },
    { name: 'iDEX Defence', desc: 'Defence AI jobs', url: 'https://idex.gov.in/', color: '#1a237e', icon: '🛡️' },
    { name: 'DRDO Careers', desc: 'Government defence', url: 'https://www.drdo.gov.in/careers', color: '#4a148c', icon: '🔬' }
  ]

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <Navbar active="jobs" />
      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '2rem' }}>

        {/* Header */}
        <div style={{
          background: 'linear-gradient(135deg, #0f172a, #1e3a5f)',
          borderRadius: '20px', padding: '2rem',
          color: 'white', marginBottom: '2rem'
        }}>
          <h1 style={{ fontSize: '28px', fontWeight: '800', marginBottom: '8px' }}>
            💼 Job Recommendations
          </h1>
          <p style={{ opacity: '0.8', fontSize: '16px' }}>
            {jobs.length}+ jobs matching your skills — with direct apply links!
          </p>
        </div>

        {/* Search Card */}
        <div style={{
          background: 'white', borderRadius: '16px',
          padding: '1.5rem', marginBottom: '1.5rem',
          border: '1px solid #e5e7eb'
        }}>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '16px' }}>
            <input
              placeholder="Job role / keywords"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && loadJobs()}
              style={{
                flex: 2, minWidth: '200px', padding: '12px 16px',
                border: '2px solid #e5e7eb', borderRadius: '10px',
                fontSize: '15px', outline: 'none', boxSizing: 'border-box'
              }}
              onFocus={e => e.target.style.borderColor = '#6366f1'}
              onBlur={e => e.target.style.borderColor = '#e5e7eb'}
            />
            <input
              placeholder="Location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              style={{
                flex: 1, minWidth: '150px', padding: '12px 16px',
                border: '2px solid #e5e7eb', borderRadius: '10px',
                fontSize: '15px', outline: 'none', boxSizing: 'border-box'
              }}
            />
            <button
              onClick={loadJobs}
              style={{
                padding: '12px 28px',
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                color: 'white', border: 'none', borderRadius: '10px',
                fontSize: '15px', fontWeight: '700', cursor: 'pointer'
              }}
            >
              Search
            </button>
          </div>

          {/* Popular roles */}
          <div style={{ marginBottom: '12px' }}>
            <p style={{ fontSize: '12px', fontWeight: '700', color: '#6b7280', marginBottom: '8px' }}>
              POPULAR SEARCHES:
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {popularRoles.map((r, i) => (
                <button key={i}
                  onClick={() => { setRole(r); setTimeout(loadJobs, 100) }}
                  style={{
                    padding: '5px 12px',
                    background: role === r ? '#6366f1' : '#f3f4f6',
                    color: role === r ? 'white' : '#374151',
                    border: 'none', borderRadius: '20px',
                    fontSize: '12px', cursor: 'pointer'
                  }}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {/* Filters */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' }}>
            <p style={{ fontSize: '12px', fontWeight: '700', color: '#6b7280' }}>Filter:</p>
            {[
              { id: 'all', label: 'All Jobs' },
              { id: 'remote', label: 'Remote' },
              { id: 'fresher', label: 'Fresher' },
              { id: 'internship', label: 'Internship' },
              { id: 'defence', label: 'Defence AI' }
            ].map(f => (
              <button key={f.id} onClick={() => setFilter(f.id)}
                style={{
                  padding: '5px 12px',
                  background: filter === f.id ? '#1e1b4b' : '#f3f4f6',
                  color: filter === f.id ? 'white' : '#374151',
                  border: 'none', borderRadius: '20px',
                  fontSize: '12px', fontWeight: '600', cursor: 'pointer'
                }}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results count */}
        {!loading && (
          <p style={{ color: '#6b7280', fontSize: '14px', marginBottom: '1rem' }}>
            Showing {filteredJobs.length} jobs {role && `for "${role}"`}
          </p>
        )}

        {/* Loading */}
        {loading && (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{
              width: '48px', height: '48px',
              border: '4px solid #e5e7eb',
              borderTop: '4px solid #6366f1',
              borderRadius: '50%',
              animation: 'spin 0.8s linear infinite',
              margin: '0 auto 16px'
            }} />
            <p style={{ color: '#6b7280' }}>Finding best jobs for you...</p>
          </div>
        )}

        {/* No jobs */}
        {!loading && filteredJobs.length === 0 && (
          <div style={{
            background: 'white', borderRadius: '16px',
            padding: '3rem', textAlign: 'center',
            border: '1px solid #e5e7eb'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</div>
            <h3 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '8px' }}>
              No jobs found
            </h3>
            <p style={{ color: '#6b7280' }}>Try different keywords</p>
          </div>
        )}

        {/* Jobs list */}
        {!loading && filteredJobs.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {filteredJobs.map((job, i) => {
              const matchColors = getMatchColor(job.match_score)
              const daysLeft = getDaysLeft(job.apply_date)
              const isExpanded = expandedJob === i

              // Apply links
              const linkedinUrl = (job.apply_links && job.apply_links.linkedin)
                ? job.apply_links.linkedin
                : `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(job.title || '')}&location=India`

              const naukriUrl = (job.apply_links && job.apply_links.naukri)
                ? job.apply_links.naukri
                : `https://www.naukri.com/${(job.title || '').toLowerCase().replace(/\s+/g, '-')}-jobs`

              const companyUrl = (job.apply_links && job.apply_links.company)
                ? job.apply_links.company
                : null

              // Only show jobs with days remaining
              // Skip if expired (daysLeft <= 0)
              if (daysLeft !== null && daysLeft <= 0) return null

              return (
                <div key={i} style={{
                  background: 'white', borderRadius: '16px',
                  border: '1px solid #e5e7eb',
                  boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
                  overflow: 'hidden'
                }}>
                  <div style={{ padding: '1.5rem' }}>

                    {/* Top row */}
                    <div style={{
                      display: 'flex', justifyContent: 'space-between',
                      alignItems: 'flex-start', marginBottom: '12px',
                      flexWrap: 'wrap', gap: '12px'
                    }}>
                      <div style={{ flex: 1 }}>
                        <div style={{
                          display: 'flex', alignItems: 'center',
                          gap: '8px', marginBottom: '4px', flexWrap: 'wrap'
                        }}>
                          <h3 style={{ fontSize: '19px', fontWeight: '700', color: '#1a1a1a' }}>
                            {job.title}
                          </h3>
                          {job.job_type === 'Internship' && (
                            <span style={{
                              background: '#fef3c7', color: '#92400e',
                              padding: '2px 8px', borderRadius: '10px',
                              fontSize: '11px', fontWeight: '700'
                            }}>INTERNSHIP</span>
                          )}
                          {job.remote && (
                            <span style={{
                              background: '#ecfdf5', color: '#065f46',
                              padding: '2px 8px', borderRadius: '10px',
                              fontSize: '11px', fontWeight: '700'
                            }}>REMOTE</span>
                          )}
                        </div>
                        <p style={{ color: '#6b7280', fontSize: '14px' }}>
                          🏢 {job.company} &nbsp;•&nbsp; 📍 {job.location}
                        </p>
                      </div>

                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '6px' }}>
                        <div style={{
                          background: matchColors.bg, color: matchColors.color,
                          border: `1px solid ${matchColors.border}`,
                          padding: '6px 14px', borderRadius: '20px',
                          fontWeight: '800', fontSize: '14px'
                        }}>
                          {job.match_score}% match
                        </div>
                        {daysLeft !== null && daysLeft > 0 && (
                          <div style={{
                            background: daysLeft <= 7 ? '#fef2f2' : daysLeft <= 14 ? '#fef3c7' : '#ecfdf5',
                            color: daysLeft <= 7 ? '#dc2626' : daysLeft <= 14 ? '#92400e' : '#065f46',
                            padding: '4px 10px', borderRadius: '10px',
                            fontSize: '12px', fontWeight: '700',
                            border: `1px solid ${daysLeft <= 7 ? '#fca5a5' : daysLeft <= 14 ? '#fcd34d' : '#6ee7b7'}`
                          }}>
                            ⏰ {daysLeft} days left
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Tags */}
                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '12px' }}>
                      <span style={{
                        background: '#f0fdf4', color: '#166534',
                        padding: '4px 12px', borderRadius: '20px',
                        fontSize: '13px', fontWeight: '600', border: '1px solid #bbf7d0'
                      }}>
                        💰 {job.salary}
                      </span>
                      <span style={{
                        background: '#eff6ff', color: '#1d4ed8',
                        padding: '4px 12px', borderRadius: '20px',
                        fontSize: '13px', fontWeight: '600', border: '1px solid #bfdbfe'
                      }}>
                        📅 {job.experience}
                      </span>
                      <span style={{
                        background: '#f9fafb', color: '#374151',
                        padding: '4px 12px', borderRadius: '20px',
                        fontSize: '13px', fontWeight: '600', border: '1px solid #e5e7eb'
                      }}>
                        💼 {job.job_type}
                      </span>
                    </div>

                    {/* Description */}
                    {job.description && (
                      <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '12px', lineHeight: '1.6' }}>
                        {job.description}
                      </p>
                    )}

                    {/* Skills */}
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
                      {job.matched_skills && job.matched_skills.map((skill, j) => (
                        <span key={j} style={{
                          background: '#ecfdf5', color: '#065f46',
                          padding: '3px 10px', borderRadius: '20px',
                          fontSize: '12px', fontWeight: '600', border: '1px solid #bbf7d0'
                        }}>
                          ✅ {skill}
                        </span>
                      ))}
                      {job.missing_skills && job.missing_skills.map((skill, j) => (
                        <span key={j} style={{
                          background: '#fef2f2', color: '#dc2626',
                          padding: '3px 10px', borderRadius: '20px',
                          fontSize: '12px', fontWeight: '600', border: '1px solid #fca5a5'
                        }}>
                          ❌ {skill}
                        </span>
                      ))}
                    </div>

                    {/* Apply Buttons */}
                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' }}>
                      <a
                        href={linkedinUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          padding: '10px 20px', background: '#0077b5',
                          color: 'white', borderRadius: '8px',
                          fontSize: '13px', fontWeight: '700',
                          textDecoration: 'none', display: 'inline-block'
                        }}
                      >
                        Apply LinkedIn →
                      </a>
                      
                        href={naukriUrl}
                      <a
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          padding: '10px 20px', background: '#ff7555',
                          color: 'white', borderRadius: '8px',
                          fontSize: '13px', fontWeight: '700',
                          textDecoration: 'none', display: 'inline-block'
                        }}
                      >
                        Apply Naukri →
                      </a>
                      {companyUrl && (
                        <a
                          href={companyUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{
                            padding: '10px 20px',
                            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                            color: 'white', borderRadius: '8px',
                            fontSize: '13px', fontWeight: '700',
                            textDecoration: 'none', display: 'inline-block'
                          }}
                        >
                          Company Site →
                        </a>
                      )}
                      <button
                        onClick={() => setExpandedJob(isExpanded ? null : i)}
                        style={{
                          padding: '10px 14px', background: '#f3f4f6',
                          color: '#374151', border: 'none', borderRadius: '8px',
                          fontSize: '13px', fontWeight: '600', cursor: 'pointer'
                        }}
                      >
                        {isExpanded ? 'Less' : 'More Details'}
                      </button>
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {isExpanded && (
                    <div style={{
                      padding: '1.5rem',
                      borderTop: '1px solid #f3f4f6',
                      background: '#f9fafb'
                    }}>
                      {job.required_skills && (
                        <div style={{ marginBottom: '14px' }}>
                          <p style={{ fontSize: '13px', fontWeight: '700', color: '#374151', marginBottom: '8px' }}>
                            Required Skills
                          </p>
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                            {job.required_skills.map((s, j) => (
                              <span key={j} style={{
                                background: '#ede9fe', color: '#6d28d9',
                                padding: '4px 12px', borderRadius: '20px',
                                fontSize: '12px', fontWeight: '600'
                              }}>
                                {s}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {job.good_to_have && job.good_to_have.length > 0 && (
                        <div style={{ marginBottom: '14px' }}>
                          <p style={{ fontSize: '13px', fontWeight: '700', color: '#374151', marginBottom: '8px' }}>
                            Good to Have
                          </p>
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                            {job.good_to_have.map((s, j) => (
                              <span key={j} style={{
                                background: '#fef3c7', color: '#92400e',
                                padding: '4px 12px', borderRadius: '20px',
                                fontSize: '12px', fontWeight: '600'
                              }}>
                                {s}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {job.apply_date && (
                        <p style={{ fontSize: '13px', color: '#6b7280', fontWeight: '500' }}>
                          Apply before: <strong>
                            {new Date(job.apply_date).toLocaleDateString('en-IN', {
                              day: 'numeric', month: 'long', year: 'numeric'
                            })}
                          </strong>
                        </p>
                      )}

                      {/* All portals */}
                      <div style={{ marginTop: '14px' }}>
                        <p style={{ fontSize: '13px', fontWeight: '700', color: '#374151', marginBottom: '8px' }}>
                          Apply on More Portals:
                        </p>
                        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                          <a href={linkedinUrl} target="_blank" rel="noopener noreferrer"
                            style={{ padding: '8px 16px', background: '#0077b5', color: 'white', borderRadius: '8px', fontSize: '13px', fontWeight: '600', textDecoration: 'none' }}>
                            LinkedIn
                          </a>
                          <a href={naukriUrl} target="_blank" rel="noopener noreferrer"
                            style={{ padding: '8px 16px', background: '#ff7555', color: 'white', borderRadius: '8px', fontSize: '13px', fontWeight: '600', textDecoration: 'none' }}>
                            Naukri
                          </a>
                          
                            <a
  href={`https://in.indeed.com/jobs?q=${encodeURIComponent(job.title || '')}&l=India`}
  target="_blank"
  rel="noopener noreferrer"
  style={{
    padding: '8px 16px',
    background: '#0058d6',
    color: 'white',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
    textDecoration: 'none'
  }}
>
  Indeed
</a>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}

        {/* Job Portals Section */}
        <div style={{
          background: 'white', borderRadius: '16px',
          padding: '1.5rem', marginTop: '2rem',
          border: '1px solid #e5e7eb'
        }}>
          <h3 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '14px', color: '#1a1a1a' }}>
            Browse All Job Portals
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '12px'
          }}>
            {portals.map((portal, i) => (
              <a key={i} href={portal.url} target="_blank" rel="noopener noreferrer"
                style={{
                  display: 'flex', alignItems: 'center', gap: '12px',
                  padding: '14px', background: portal.color + '10',
                  border: `1px solid ${portal.color}30`,
                  borderRadius: '12px', textDecoration: 'none',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = portal.color + '20'
                  e.currentTarget.style.transform = 'translateY(-2px)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = portal.color + '10'
                  e.currentTarget.style.transform = 'none'
                }}
              >
                <span style={{ fontSize: '28px' }}>{portal.icon}</span>
                <div>
                  <p style={{ fontSize: '14px', fontWeight: '700', color: portal.color, marginBottom: '2px' }}>
                    {portal.name}
                  </p>
                  <p style={{ fontSize: '12px', color: '#6b7280' }}>{portal.desc}</p>
                </div>
              </a>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}

export default JobSearch
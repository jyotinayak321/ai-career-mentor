// ================================================
// ResumeUpload.jsx — Resume Upload Page (UPDATED)
// ================================================
// NEW SECTIONS ADDED:
// 1. ❌ Fail Points — kya galat hai resume mein
// 2. ✅ Correct Way — sahi tarika kya hona chahiye
// 3. 📈 Improve Section — kaise improve karein
// ================================================

import { useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import API from '../api/axios'

function ResumeUpload() {

  // ------------------------------------------------
  // STATE VARIABLES
  // ------------------------------------------------
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [dragOver, setDragOver] = useState(false)

  // ------------------------------------------------
  // FILE VALIDATION
  // ------------------------------------------------

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false

    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ]

    const isValidType = allowedTypes.includes(selectedFile.type) ||
      selectedFile.name.endsWith('.pdf') ||
      selectedFile.name.endsWith('.docx') ||
      selectedFile.name.endsWith('.txt')

    if (!isValidType) {
      setError('Only PDF, DOCX or TXT files allowed!')
      return false
    }

    const maxSize = 5 * 1024 * 1024
    if (selectedFile.size > maxSize) {
      setError('File size must be less than 5MB!')
      return false
    }

    setError('')
    return true
  }

  // ------------------------------------------------
  // FILE SELECT HANDLER
  // ------------------------------------------------

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    if (validateFile(selectedFile)) {
      setFile(selectedFile)
      setResult(null)
    }
  }

  // ------------------------------------------------
  // DRAG AND DROP HANDLERS
  // ------------------------------------------------

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = () => {
    setDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const droppedFile = e.dataTransfer.files[0]
    if (validateFile(droppedFile)) {
      setFile(droppedFile)
      setResult(null)
    }
  }

  // ------------------------------------------------
  // UPLOAD HANDLER
  // ------------------------------------------------

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first!')
      return
    }

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await API.post(
        '/resume/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )

      setResult(response.data)

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Upload failed! Please try again.'
      )
    }

    setLoading(false)
  }

  // ------------------------------------------------
  // GET SCORE COLOR
  // ------------------------------------------------

  const getScoreColor = (score) => {
    if (score >= 85) return '#10b981'
    if (score >= 70) return '#6366f1'
    if (score >= 55) return '#f59e0b'
    return '#ef4444'
  }

  // ------------------------------------------------
  // JSX
  // ------------------------------------------------

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <Navbar active="resume" />

      <div style={styles.content}>

        {/* Header */}
        <div style={styles.header}>
          <h1 style={styles.title}>📄 Resume Analyzer</h1>
          <p style={styles.subtitle}>
            Upload your resume and get instant AI-powered feedback!
          </p>
        </div>

        {/* Upload Area */}
        <div
          style={{
            ...styles.uploadArea,
            borderColor: dragOver ? '#6366f1' : '#d1d5db',
            background: dragOver ? '#f0f0ff' : 'white'
          }}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileInput').click()}
        >
          <div style={styles.uploadIcon}>
            {file ? '✅' : '📂'}
          </div>

          <p style={styles.uploadText}>
            {file ? file.name : 'Drop PDF, DOCX or TXT here'}
          </p>
          <p style={styles.uploadSubtext}>
            Or click to select file (max 5MB)
          </p>

          {file && (
            <p style={styles.fileSize}>
              Size: {(file.size / 1024).toFixed(1)} KB
            </p>
          )}

          <input
            type="file"
            id="fileInput"
            accept=".pdf,.docx,.txt"
            style={{ display: 'none' }}
            onChange={handleFileSelect}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div style={styles.errorBox}>
            ❌ {error}
          </div>
        )}

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          style={{
            ...styles.uploadBtn,
            background: !file || loading ? '#9ca3af' : '#6366f1',
            cursor: !file || loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.8 : 1
          }}
        >
          {loading ? '⏳ Analyzing your resume...' : '🚀 Analyze Resume'}
        </button>

        {/* ---------------------------------------- */}
        {/* RESULTS SECTION                          */}
        {/* ---------------------------------------- */}

        {result && (
          <div style={styles.resultsSection}>

            {/* Score Card */}
            <div style={{
              ...styles.scoreCard,
              background: `linear-gradient(135deg, 
                ${getScoreColor(result.score_report?.score)}, 
                ${getScoreColor(result.score_report?.score)}99)`
            }}>
              <p style={styles.scoreLabel}>Resume Score</p>
              <p style={styles.scoreNumber}>
                {result.score_report?.score}
                <span style={styles.scoreOutOf}>/100</span>
              </p>
              <p style={styles.scoreGrade}>
                Grade: {result.score_report?.grade} —{' '}
                {result.score_report?.grade_label}
              </p>
            </div>

            {/* Score Breakdown */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>📊 Score Breakdown</h3>
              {result.score_report?.breakdown &&
                Object.entries(result.score_report.breakdown).map(
                  ([key, value]) => (
                    <div key={key} style={styles.breakdownRow}>
                      <span style={styles.breakdownLabel}>
                        {key.charAt(0).toUpperCase() + key.slice(1)}
                      </span>
                      <div style={styles.progressBar}>
                        <div style={{
                          ...styles.progressFill,
                          width: `${(value / 40) * 100}%`,
                          background: '#6366f1'
                        }} />
                      </div>
                      <span style={styles.breakdownValue}>
                        {value}
                      </span>
                    </div>
                  )
                )}
            </div>

            {/* ❌ FAIL POINTS SECTION */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>❌ Fail Points</h3>
              <p style={styles.sectionSubtitle}>
                Ye cheezein tumhare resume mein galat hain ya missing hain
              </p>
              {result.score_report?.fail_points?.length > 0 ? (
                result.score_report.fail_points.map((point, i) => (
                  <div key={i} style={styles.failItem}>
                    <span style={styles.failBadge}>✗</span>
                    <span style={styles.failText}>{point}</span>
                  </div>
                ))
              ) : (
                <p style={{ color: '#10b981', fontWeight: '600', fontSize: '14px' }}>
                  🎉 No major fail points found! Great resume!
                </p>
              )}
            </div>

            {/* ✅ CORRECT WAY SECTION */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>✅ Correct Way</h3>
              <p style={styles.sectionSubtitle}>
                Har fail point ka sahi tarika — aise hona chahiye tha
              </p>
              {result.score_report?.correct_ways?.length > 0 ? (
                result.score_report.correct_ways.map((way, i) => (
                  <div key={i} style={styles.correctItem}>
                    <span style={styles.correctBadge}>✓</span>
                    <span style={styles.correctText}>{way}</span>
                  </div>
                ))
              ) : (
                <p style={{ color: '#6b7280', fontSize: '14px' }}>
                  No corrections needed at this time.
                </p>
              )}
            </div>

            {/* 📈 IMPROVE SECTION */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>📈 How to Improve</h3>
              <p style={styles.sectionSubtitle}>
                Step-by-step tips to make your resume stronger
              </p>
              {result.score_report?.improvements?.length > 0 ? (
                result.score_report.improvements.map((tip, i) => (
                  <div key={i} style={styles.improveItem}>
                    <span style={styles.improveNumber}>{i + 1}</span>
                    <span style={styles.improveText}>{tip}</span>
                  </div>
                ))
              ) : (
                <p style={{ color: '#6b7280', fontSize: '14px' }}>
                  🎉 No improvements needed!
                </p>
              )}
            </div>

            {/* Skills Found */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>
                ⚡ Skills Found ({result.parsed_info?.skills_count})
              </h3>
              <div style={styles.skillsContainer}>
                {result.parsed_info?.skills_found?.map((skill, i) => (
                  <span key={i} style={styles.skillBadge}>
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Contact Info */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>📋 Extracted Info</h3>
              <div style={styles.infoGrid}>
                <div style={styles.infoItem}>
                  <span style={styles.infoLabel}>Email:</span>
                  <span style={styles.infoValue}>
                    {result.parsed_info?.email || 'Not found'}
                  </span>
                </div>
                <div style={styles.infoItem}>
                  <span style={styles.infoLabel}>Phone:</span>
                  <span style={styles.infoValue}>
                    {result.parsed_info?.phone || 'Not found'}
                  </span>
                </div>
              </div>
            </div>

            {/* 💡 AI Feedback */}
            <div style={styles.card}>
              <h3 style={styles.cardTitle}>💡 AI Feedback</h3>
              {result.score_report?.feedback?.length > 0 ? (
                result.score_report.feedback.map((item, i) => (
                  <div key={i} style={styles.feedbackItem}>
                    {item}
                  </div>
                ))
              ) : (
                <p style={{ color: '#10b981', fontWeight: '600' }}>
                  🎉 Excellent! No major issues found!
                </p>
              )}
            </div>

          </div>
        )}

      </div>
    </div>
  )
}

// ------------------------------------------------
// STYLES
// ------------------------------------------------

const styles = {
  content: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '2rem'
  },
  header: {
    marginBottom: '2rem'
  },
  title: {
    fontSize: '26px',
    fontWeight: '700',
    color: '#1a1a1a',
    marginBottom: '8px'
  },
  subtitle: {
    color: '#6b7280',
    fontSize: '16px'
  },
  uploadArea: {
    border: '2px dashed',
    borderRadius: '16px',
    padding: '3rem',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s',
    marginBottom: '1.5rem'
  },
  uploadIcon: {
    fontSize: '48px',
    marginBottom: '12px'
  },
  uploadText: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '8px'
  },
  uploadSubtext: {
    color: '#9ca3af',
    fontSize: '14px'
  },
  fileSize: {
    color: '#6366f1',
    fontSize: '13px',
    marginTop: '8px',
    fontWeight: '500'
  },
  errorBox: {
    background: '#fef2f2',
    border: '1px solid #fca5a5',
    color: '#dc2626',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '1rem',
    fontSize: '14px'
  },
  uploadBtn: {
    width: '100%',
    padding: '14px',
    color: 'white',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: '600',
    marginBottom: '2rem',
    transition: 'all 0.2s'
  },
  resultsSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  scoreCard: {
    borderRadius: '16px',
    padding: '2rem',
    color: 'white',
    textAlign: 'center'
  },
  scoreLabel: {
    fontSize: '14px',
    opacity: '0.85',
    marginBottom: '8px'
  },
  scoreNumber: {
    fontSize: '72px',
    fontWeight: '800',
    lineHeight: '1'
  },
  scoreOutOf: {
    fontSize: '28px',
    fontWeight: '400'
  },
  scoreGrade: {
    fontSize: '20px',
    fontWeight: '600',
    marginTop: '12px',
    opacity: '0.95'
  },
  card: {
    background: 'white',
    borderRadius: '12px',
    padding: '1.5rem',
    border: '1px solid #e5e7eb'
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: '700',
    marginBottom: '6px',
    color: '#1a1a1a'
  },
  sectionSubtitle: {
    fontSize: '13px',
    color: '#9ca3af',
    marginBottom: '16px',
    fontStyle: 'italic'
  },

  // ❌ Fail Points styles
  failItem: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    padding: '12px 14px',
    background: '#fef2f2',
    border: '1px solid #fca5a5',
    borderRadius: '10px',
    marginBottom: '10px',
  },
  failBadge: {
    background: '#ef4444',
    color: 'white',
    borderRadius: '50%',
    width: '22px',
    height: '22px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '13px',
    fontWeight: '700',
    flexShrink: 0,
    marginTop: '1px'
  },
  failText: {
    fontSize: '14px',
    color: '#dc2626',
    lineHeight: '1.6'
  },

  // ✅ Correct Way styles
  correctItem: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    padding: '12px 14px',
    background: '#f0fdf4',
    border: '1px solid #86efac',
    borderRadius: '10px',
    marginBottom: '10px',
  },
  correctBadge: {
    background: '#10b981',
    color: 'white',
    borderRadius: '50%',
    width: '22px',
    height: '22px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '13px',
    fontWeight: '700',
    flexShrink: 0,
    marginTop: '1px'
  },
  correctText: {
    fontSize: '14px',
    color: '#16a34a',
    lineHeight: '1.6'
  },

  // 📈 Improve Section styles
  improveItem: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    padding: '12px 14px',
    background: '#eff6ff',
    border: '1px solid #93c5fd',
    borderRadius: '10px',
    marginBottom: '10px',
  },
  improveNumber: {
    background: '#6366f1',
    color: 'white',
    borderRadius: '50%',
    minWidth: '26px',
    height: '26px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '13px',
    fontWeight: '700',
    flexShrink: 0,
    marginTop: '1px'
  },
  improveText: {
    fontSize: '14px',
    color: '#1d4ed8',
    lineHeight: '1.6'
  },

  // Skills
  breakdownRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '10px'
  },
  breakdownLabel: {
    width: '100px',
    fontSize: '14px',
    color: '#374151',
    textTransform: 'capitalize'
  },
  progressBar: {
    flex: 1,
    height: '8px',
    background: '#f3f4f6',
    borderRadius: '4px',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    borderRadius: '4px',
    transition: 'width 0.5s ease'
  },
  breakdownValue: {
    width: '30px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#6366f1',
    textAlign: 'right'
  },
  skillsContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '8px'
  },
  skillBadge: {
    background: '#ede9fe',
    color: '#6d28d9',
    padding: '4px 12px',
    borderRadius: '20px',
    fontSize: '13px',
    fontWeight: '500'
  },
  infoGrid: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px'
  },
  infoItem: {
    display: 'flex',
    gap: '12px',
    fontSize: '14px'
  },
  infoLabel: {
    fontWeight: '600',
    color: '#374151',
    minWidth: '60px'
  },
  infoValue: {
    color: '#6b7280'
  },
  feedbackItem: {
    padding: '10px 0',
    borderBottom: '1px solid #f3f4f6',
    fontSize: '14px',
    color: '#374151',
    lineHeight: '1.6'
  }
}

export default ResumeUpload

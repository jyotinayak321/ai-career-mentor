// ================================================
// Register.jsx — Registration Page
// ================================================

import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import API from '../api/axios'

function Register() {

  // ------------------------------------------------
  // STATE VARIABLES — 4 fields hain is baar
  // ------------------------------------------------
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const navigate = useNavigate()

  // ------------------------------------------------
  // REGISTER FUNCTION
  // ------------------------------------------------

  const handleRegister = async () => {

    // ----------------------------------------
    // VALIDATION — Pehle check karo
    // ----------------------------------------

    // Koi field khali toh nahi?
    if (!name || !email || !password || !confirmPassword) {
      setError('Saare fields fill karo!')
      return
    }

    // Password minimum 6 characters?
    if (password.length < 6) {
      setError('Password minimum 6 characters ka hona chahiye!')
      return
    }

    // Passwords match karte hain?
    // Ye bahut important check hai!
    if (password !== confirmPassword) {
      setError('Passwords match nahi kar rahe!')
      return
    }

    // Email valid format?
    // Simple regex check
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setError('Valid email address daalo!')
      return
    }

    setLoading(true)
    setError('')

    try {
      // ----------------------------------------
      // API CALL — Register endpoint
      // ----------------------------------------
      const response = await API.post('/auth/register', {
        name,
        email,
        password
        // confirmPassword backend ko nahi bhejte!
        // Ye sirf frontend validation ke liye hai
      })

      // Token save karo
      localStorage.setItem('token', response.data.token)
      localStorage.setItem(
        'user',
        JSON.stringify(response.data.user)
      )

      // Dashboard pe jao
      navigate('/dashboard')

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Registration failed! Please try again.'
      )
    }

    setLoading(false)
  }

  // ------------------------------------------------
  // JSX
  // ------------------------------------------------

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <div style={styles.logo}>🤖</div>
        <h1 style={styles.title}>Create Account</h1>
        <p style={styles.subtitle}>
          AI Career journey shuru karo!
        </p>

        {/* Error Box */}
        {error && (
          <div style={styles.errorBox}>
            ❌ {error}
          </div>
        )}

        {/* Name Field */}
        <div style={styles.formGroup}>
          <label style={styles.label}>Full Name</label>
          <input
            type="text"
            placeholder="Jyoti Nayak"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={styles.input}
          />
        </div>

        {/* Email Field */}
        <div style={styles.formGroup}>
          <label style={styles.label}>Email Address</label>
          <input
            type="email"
            placeholder="jyoti@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
          />
        </div>

        {/* Password Field */}
        <div style={styles.formGroup}>
          <label style={styles.label}>Password</label>
          <input
            type="password"
            placeholder="Minimum 6 characters"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
          />
        </div>

        {/* Confirm Password */}
        <div style={styles.formGroup}>
          <label style={styles.label}>
            Confirm Password
          </label>
          <input
            type="password"
            placeholder="Password dobara likho"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            style={{
              ...styles.input,
              // Password match check — real time!
              borderColor: confirmPassword && password !== confirmPassword
                ? '#ef4444'  // Red — match nahi
                : confirmPassword && password === confirmPassword
                  ? '#10b981' // Green — match!
                  : '#e5e7eb' // Default gray
            }}
          />
          {/* Real time password match feedback */}
          {confirmPassword && (
            <p style={{
              fontSize: '12px',
              marginTop: '4px',
              color: password === confirmPassword ? '#10b981' : '#ef4444'
            }}>
              {password === confirmPassword
                ? '✅ Passwords match!'
                : '❌ Passwords match nahi kar rahe'}
            </p>
          )}
        </div>

        {/* Register Button */}
        <button
          onClick={handleRegister}
          disabled={loading}
          style={{
            ...styles.registerBtn,
            opacity: loading ? 0.7 : 1,
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? '⏳ Account ban raha hai...' : '🚀 Create Account'}
        </button>

        {/* Login Link */}
        <p style={styles.switchText}>
          Already account hai?{' '}
          <Link to="/login" style={styles.link}>
            Login karo
          </Link>
        </p>

      </div>
    </div>
  )
}

// ------------------------------------------------
// STYLES
// ------------------------------------------------

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea, #764ba2)',
    padding: '1rem'
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '2.5rem',
    width: '100%',
    maxWidth: '420px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.2)'
  },
  logo: {
    fontSize: '48px',
    textAlign: 'center',
    marginBottom: '12px'
  },
  title: {
    fontSize: '26px',
    fontWeight: '700',
    textAlign: 'center',
    color: '#1a1a1a',
    marginBottom: '6px'
  },
  subtitle: {
    color: '#6b7280',
    textAlign: 'center',
    fontSize: '14px',
    marginBottom: '1.5rem'
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
  formGroup: {
    marginBottom: '14px'
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '6px'
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    border: '1.5px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '15px',
    outline: 'none',
    boxSizing: 'border-box',
    fontFamily: 'inherit',
    transition: 'border-color 0.2s'
  },
  registerBtn: {
    width: '100%',
    padding: '13px',
    background: '#6366f1',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    marginTop: '8px',
    marginBottom: '16px'
  },
  switchText: {
    textAlign: 'center',
    color: '#6b7280',
    fontSize: '14px'
  },
  link: {
    color: '#6366f1',
    fontWeight: '600',
    textDecoration: 'none'
  }
}

export default Register
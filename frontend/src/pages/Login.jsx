// ================================================
// Login.jsx — Login Page
// ================================================
// YE PAGE KYA KARTA HAI?
// 1. Email/Password form dikhata hai
// 2. Backend se login karta hai
// 3. Token localStorage mein save karta hai
// 4. Dashboard pe redirect karta hai
// ================================================

// useState = State variables ke liye
// useNavigate = Page change karne ke liye
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import API from '../api/axios'

function Login() {

  // ------------------------------------------------
  // STATE VARIABLES
  // ------------------------------------------------
  // Ye sab "reactive" hain
  // Change hone pe UI automatically update hoga!
  // ------------------------------------------------

  // Form fields
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // Loading = API call chal rahi hai
  const [loading, setLoading] = useState(false)

  // Error message dikhane ke liye
  const [error, setError] = useState('')

  // useNavigate = Programmatically page change karo
  // navigate('/dashboard') = Dashboard pe jao
  const navigate = useNavigate()

  // ------------------------------------------------
  // LOGIN FUNCTION
  // ------------------------------------------------

  const handleLogin = async () => {

    // Validation — Fields khali toh nahi?
    if (!email || !password) {
      setError('Email aur password dono zaroori hain!')
      return // Function yahan rok do
    }

    // Loading start karo
    setLoading(true)
    setError('') // Purana error clear karo

    try {
      // ----------------------------------------
      // API CALL
      // ----------------------------------------
      // API = hamara configured axios instance
      // .post() = POST request
      // '/auth/login' = Endpoint
      // {email, password} = Request body
      //
      // baseURL already set hai: localhost:8000/api
      // So full URL = localhost:8000/api/auth/login
      // ----------------------------------------

      const response = await API.post('/auth/login', {
        email,
        password
      })

      // ----------------------------------------
      // TOKEN SAVE KARO
      // ----------------------------------------
      // Login successful!
      // Token aur user info save karo

      localStorage.setItem(
        'token',
        response.data.token
      )

      localStorage.setItem(
        'user',
        JSON.stringify(response.data.user)
        // JSON.stringify = Object ko string mein
        // localStorage strings store karta hai!
      )

      // Dashboard pe redirect karo
      navigate('/dashboard')

    } catch (err) {
      // ----------------------------------------
      // ERROR HANDLE KARO
      // ----------------------------------------
      // err.response?.data?.detail = Backend ka error
      // ?. = Optional chaining
      //      Agar null/undefined toh crash mat karo!
      // ----------------------------------------

      setError(
        err.response?.data?.detail ||
        'Login failed! Server se connect nahi ho pa raha.'
      )
    }

    // Loading band karo
    setLoading(false)
  }

  // Enter key pe login karo
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleLogin()
    }
  }

  // ------------------------------------------------
  // JSX — UI Render karo
  // ------------------------------------------------
  // JSX = JavaScript + HTML mix
  // {} ke andar JavaScript code likh sakte hain
  // ------------------------------------------------

  return (
    // Outer container — full screen, centered
    <div style={styles.container}>

      {/* Card — white box */}
      <div style={styles.card}>

        {/* Logo */}
        <div style={styles.logo}>🤖</div>

        {/* Title */}
        <h1 style={styles.title}>Welcome Back!</h1>
        <p style={styles.subtitle}>
          AI Career Mentor mein login karo
        </p>

        {/* Error Message */}
        {/* Conditional Rendering: */}
        {/* error truthy hai toh dikhao */}
        {/* error falsy hai toh mat dikhao */}
        {error && (
          <div style={styles.errorBox}>
            ❌ {error}
          </div>
        )}

        {/* Email Input */}
        <div style={styles.formGroup}>
          <label style={styles.label}>
            Email Address
          </label>
          <input
            type="email"
            placeholder="jyoti@gmail.com"
            value={email}
            // onChange = Har keystroke pe
            // e.target.value = Jo likha gaya
            // setEmail = State update karo
            onChange={(e) => setEmail(e.target.value)}
            onKeyPress={handleKeyPress}
            style={styles.input}
          />
        </div>

        {/* Password Input */}
        <div style={styles.formGroup}>
          <label style={styles.label}>
            Password
          </label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyPress={handleKeyPress}
            style={styles.input}
          />
        </div>

        {/* Login Button */}
        <button
          onClick={handleLogin}
          disabled={loading}
          style={{
            ...styles.loginBtn,
            // Loading hone pe button dim karo
            opacity: loading ? 0.7 : 1,
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {/* Ternary operator: */}
          {/* condition ? true : false */}
          {loading ? '⏳ Login ho raha hai...' : '🚀 Login'}
        </button>

        {/* Register Link */}
        <p style={styles.switchText}>
          Account nahi hai?{' '}
          {/* Link = React Router ka component */}
          {/* Page reload nahi karta! */}
          <Link to="/register" style={styles.link}>
            Register karo
          </Link>
        </p>

      </div>
    </div>
  )
}

// ------------------------------------------------
// STYLES OBJECT
// ------------------------------------------------
// CSS in JavaScript
// camelCase use karo: backgroundColor, fontSize
// Strings mein values: '16px', 'white', '#6366f1'
// ------------------------------------------------
// Login.jsx ke andar sirf STYLES OBJECT replace karo
// Baaki sab code same rahega!

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    // 🎨 YAHAN CHANGE: Dark gradient background
    background: 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)',
    padding: '1rem',
    fontFamily: "'Plus Jakarta Sans', sans-serif",
  },
  card: {
    // 🎨 YAHAN CHANGE: Glass effect
    background: 'rgba(255, 255, 255, 0.05)',
    backdropFilter: 'blur(20px)',
    border: '1px solid rgba(255, 255, 255, 0.12)',
    borderRadius: '24px',
    padding: '2.5rem',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 25px 50px rgba(0,0,0,0.5)',
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
    // 🎨 YAHAN CHANGE: White text
    color: '#ffffff',
    marginBottom: '6px'
  },
  subtitle: {
    // 🎨 YAHAN CHANGE: Semi-transparent white
    color: 'rgba(255,255,255,0.5)',
    textAlign: 'center',
    fontSize: '14px',
    marginBottom: '1.5rem'
  },
  errorBox: {
    background: 'rgba(239,68,68,0.15)',
    border: '1px solid rgba(239,68,68,0.4)',
    color: '#fca5a5',
    padding: '12px 16px',
    borderRadius: '10px',
    marginBottom: '1rem',
    fontSize: '14px'
  },
  formGroup: {
    marginBottom: '16px'
  },
  label: {
    display: 'block',
    fontSize: '11px',
    fontWeight: '600',
    // 🎨 YAHAN CHANGE: Muted white label
    color: 'rgba(255,255,255,0.5)',
    marginBottom: '6px',
    letterSpacing: '0.5px',
    textTransform: 'uppercase'
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    // 🎨 YAHAN CHANGE: Glass input
    background: 'rgba(255,255,255,0.07)',
    border: '1px solid rgba(255,255,255,0.12)',
    borderRadius: '12px',
    fontSize: '14px',
    // 🎨 YAHAN CHANGE: White text inside input
    color: '#ffffff',
    outline: 'none',
    boxSizing: 'border-box',
    fontFamily: 'inherit',
  },
  loginBtn: {
    width: '100%',
    padding: '13px',
    // 🎨 YAHAN CHANGE: Purple gradient button
    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    fontSize: '15px',
    fontWeight: '600',
    marginTop: '8px',
    marginBottom: '16px',
  },
  switchText: {
    textAlign: 'center',
    color: 'rgba(255,255,255,0.4)',
    fontSize: '14px'
  },
  link: {
    // 🎨 YAHAN CHANGE: Light purple link
    color: '#818cf8',
    fontWeight: '600',
    textDecoration: 'none'
  }
}
export default Login
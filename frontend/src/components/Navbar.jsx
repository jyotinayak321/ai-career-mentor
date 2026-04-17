// ================================================
// Navbar.jsx — Responsive Navigation Bar
// ================================================
// WHAT DOES THIS DO?
// 1. Desktop pe full navbar dikhata hai
// 2. Mobile pe hamburger menu dikhata hai
// 3. Active page highlight karta hai
// 4. Logout functionality deta hai
//
// PROPS:
// active = Current page id
//          "dashboard", "resume", "jobs" etc.
// ================================================

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Navbar({ active }) {
  const navigate = useNavigate()

  // ------------------------------------------------
  // STATE — Mobile menu open/close
  // ------------------------------------------------
  const [menuOpen, setMenuOpen] = useState(false)

  // Current user info localStorage se lo
  const user = JSON.parse(
    localStorage.getItem('user') || '{}'
  )

  // ------------------------------------------------
  // LOGOUT FUNCTION
  // ------------------------------------------------
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  // ------------------------------------------------
  // NAV LINKS DATA
  // ------------------------------------------------
  // Array of objects = Clean aur maintainable
  // Icon + Label + Path + ID
  // ------------------------------------------------
  const navLinks = [
    {
      path: '/dashboard',
      label: 'Dashboard',
      icon: '🏠',
      id: 'dashboard'
    },
    {
      path: '/resume',
      label: 'Resume',
      icon: '📄',
      id: 'resume'
    },
    {
      path: '/jobs',
      label: 'Jobs',
      icon: '💼',
      id: 'jobs'
    },
    {
      path: '/roadmap',
      label: 'Roadmap',
      icon: '🗺️',
      id: 'roadmap'
    },
    {
      path: '/interview',
      label: 'Interview',
      icon: '🎤',
      id: 'interview'
    }
  ]

  // ------------------------------------------------
  // JSX
  // ------------------------------------------------

  return (
    <>
      {/* ---------------------------------------- */}
      {/* MAIN NAVBAR */}
      {/* ---------------------------------------- */}
      <nav style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 16px',
        background: 'white',
        borderBottom: '1px solid #e5e7eb',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
      }}>

        {/* Brand Logo */}
        <div
          onClick={() => navigate('/dashboard')}
          style={{
            fontSize: '16px',
            fontWeight: '700',
            color: '#6366f1',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          🤖 AI Career
        </div>

        {/* ---------------------------------------- */}
        {/* DESKTOP LINKS — Screen > 768px pe */}
        {/* Mobile pe CSS se hide ho jaata hai */}
        {/* ---------------------------------------- */}
        <div style={{
          display: 'flex',
          gap: '4px'
        }}>
          {navLinks.map(link => (
            <button
              key={link.id}
              onClick={() => navigate(link.path)}
              style={{
                padding: '6px 10px',
                border: 'none',
                borderRadius: '8px',
                fontSize: '12px',
                fontWeight: '500',
                cursor: 'pointer',
                // Active page purple background
                background: active === link.id
                  ? '#6366f1'
                  : 'transparent',
                color: active === link.id
                  ? 'white'
                  : '#6b7280'
              }}
            >
              {link.icon} {link.label}
            </button>
          ))}
        </div>

        {/* ---------------------------------------- */}
        {/* RIGHT SIDE — User name + Menu button */}
        {/* ---------------------------------------- */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          {/* User Name — First name only */}
          <span style={{
            fontSize: '12px',
            color: '#374151',
            fontWeight: '500',
            maxWidth: '80px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            👤 {user.name?.split(' ')[0] || 'User'}
          </span>

          {/* Hamburger Menu Button */}
          {/* ☰ = Open, ✕ = Close */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            style={{
              background: 'none',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '6px 10px',
              cursor: 'pointer',
              fontSize: '18px',
              color: '#374151'
            }}
          >
            {menuOpen ? '✕' : '☰'}
          </button>
        </div>
      </nav>

      {/* ---------------------------------------- */}
      {/* MOBILE DROPDOWN MENU */}
      {/* ---------------------------------------- */}
      {/* menuOpen true hone pe hi dikhega */}
      {/* Conditional rendering! */}
      {/* ---------------------------------------- */}
      {menuOpen && (
        <div style={{
          position: 'fixed',
          top: '57px',
          left: 0,
          right: 0,
          background: 'white',
          borderBottom: '1px solid #e5e7eb',
          zIndex: 99,
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
          padding: '8px'
        }}>

          {/* Nav Links */}
          {navLinks.map(link => (
            <button
              key={link.id}
              onClick={() => {
                // Page pe navigate karo
                navigate(link.path)
                // Menu band karo
                setMenuOpen(false)
              }}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                width: '100%',
                padding: '12px 16px',
                border: 'none',
                borderRadius: '10px',
                fontSize: '15px',
                fontWeight: '500',
                cursor: 'pointer',
                marginBottom: '4px',
                // Active page highlight
                background: active === link.id
                  ? '#6366f1'
                  : 'transparent',
                color: active === link.id
                  ? 'white'
                  : '#374151',
                textAlign: 'left'
              }}
            >
              <span style={{ fontSize: '20px' }}>
                {link.icon}
              </span>
              {link.label}
            </button>
          ))}

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              width: '100%',
              padding: '12px 16px',
              border: 'none',
              borderRadius: '10px',
              fontSize: '15px',
              fontWeight: '500',
              cursor: 'pointer',
              background: '#fef2f2',
              color: '#dc2626',
              textAlign: 'left',
              marginTop: '8px'
            }}
          >
            <span style={{ fontSize: '20px' }}>🚪</span>
            Logout
          </button>
        </div>
      )}
    </>
  )
}

export default Navbar
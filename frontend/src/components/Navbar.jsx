// ================================================
// Navbar.jsx — Navigation Bar Component
// ================================================
// YE COMPONENT KYA KARTA HAI?
// Har page pe top mein navigation dikhata hai
// Active page highlight karta hai
// Logout functionality deta hai
//
// PROPS:
// active = Current page ka naam
//          "dashboard", "resume", "jobs" etc.
//
// USE KAISE KAREIN:
// <Navbar active="dashboard" />
// <Navbar active="jobs" />
// ================================================

// useNavigate = Page change karne ke liye
import { useNavigate } from 'react-router-dom'

function Navbar({ active }) {
  // useNavigate hook
  // navigate('/path') = Us page pe jao
  const navigate = useNavigate()

  // Current user info localStorage se lo
  const user = JSON.parse(
    localStorage.getItem('user') || '{}'
  )

  // ------------------------------------------------
  // LOGOUT FUNCTION
  // ------------------------------------------------

  const handleLogout = () => {
    // Token aur user data hatao
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    // Login page pe jao
    navigate('/login')
  }

  // ------------------------------------------------
  // NAV LINKS — Array of objects
  // ------------------------------------------------
  // Array use karna better hai
  // Kyunki:
  // 1. Clean code
  // 2. Easy to add/remove links
  // 3. .map() se render karo
  // ------------------------------------------------

  const navLinks = [
    {
      id: 'dashboard',
      label: '🏠 Dashboard',
      path: '/dashboard'
    },
    {
      id: 'resume',
      label: '📄 Resume',
      path: '/resume'
    },
    {
      id: 'jobs',
      label: '💼 Jobs',
      path: '/jobs'
    },
    {
      id: 'roadmap',
      label: '🗺️ Roadmap',
      path: '/roadmap'
    },
    {
      id: 'interview',
      label: '🎤 Interview',
      path: '/interview'
    }
  ]

  // ------------------------------------------------
  // JSX
  // ------------------------------------------------

  return (
    <nav style={styles.navbar}>

      {/* Brand Logo */}
      <div
        style={styles.brand}
        onClick={() => navigate('/dashboard')}
      >
        🤖 AI Career Mentor
      </div>

      {/* Navigation Links */}
      <div style={styles.links}>
        {/* .map() = Array ko JSX mein convert karo */}
        {/* Har link ke liye ek button banao */}
        {navLinks.map((link) => (
          <button
            key={link.id}
            onClick={() => navigate(link.path)}
            style={{
              ...styles.navBtn,
              // Active page highlight karo
              // active prop se compare karo
              background: active === link.id
                ? '#6366f1'    // Purple — active
                : 'transparent', // Transparent — inactive
              color: active === link.id
                ? 'white'      // White text — active
                : '#6b7280'    // Gray text — inactive
            }}
          >
            {link.label}
          </button>
        ))}
      </div>

      {/* User Info + Logout */}
      <div style={styles.userSection}>

        {/* User Name */}
        <span style={styles.userName}>
          👤 {user.name || 'User'}
        </span>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          style={styles.logoutBtn}
        >
          Logout
        </button>

      </div>
    </nav>
  )
}

// ------------------------------------------------
// STYLES
// ------------------------------------------------

const styles = {
  navbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '12px 24px',
    background: 'white',
    borderBottom: '1px solid #e5e7eb',
    position: 'sticky',  // Scroll karne pe bhi upar rahe!
    top: 0,
    zIndex: 100,          // Sab ke upar dikhega
    boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
  },
  brand: {
    fontSize: '18px',
    fontWeight: '700',
    color: '#6366f1',
    cursor: 'pointer'
  },
  links: {
    display: 'flex',
    gap: '4px'
  },
  navBtn: {
    padding: '8px 14px',
    border: 'none',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s'
  },
  userSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px'
  },
  userName: {
    fontSize: '14px',
    color: '#374151',
    fontWeight: '500'
  },
  logoutBtn: {
    padding: '8px 16px',
    background: '#fef2f2',
    color: '#dc2626',
    border: '1px solid #fca5a5',
    borderRadius: '8px',
    fontSize: '13px',
    cursor: 'pointer',
    fontWeight: '500'
  }
}

export default Navbar
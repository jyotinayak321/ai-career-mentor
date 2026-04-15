// ================================================
// axios.js — API Configuration
// ================================================
// YE FILE KYA KARTI HAI?
// 1. Axios instance create karti hai
// 2. Backend URL set karti hai
// 3. JWT token automatically add karti hai
// 4. 401 error pe logout karti hai
//
// ANALOGY:
// Ye file = Ek trained courier boy
// Jo hamesha:
// → Sahi address pe jaata hai (baseURL)
// → ID card saath rakhta hai (token)
// → Rejection pe report karta hai (401)
// ================================================

import axios from 'axios'

// ------------------------------------------------
// AXIOS INSTANCE BANAO
// ------------------------------------------------
// axios.create() = Custom configured axios
//
// Jaise:
// Default axios = Plain courier boy
// Our API = Trained courier boy
//           Sab settings already set!
// ------------------------------------------------

const API = axios.create({
  // Backend ka address
  // Ye URL sab requests mein automatically lagega!
  // localhost:8000 = Hamara FastAPI server
  baseURL: 'http://localhost:8000/api',

  // 30 second timeout
  // Agar 30 sec mein response nahi aaya
  // Request cancel ho jayegi!
  timeout: 30000,

  // Default headers
  headers: {
    'Content-Type': 'application/json'
  }
})

// ------------------------------------------------
// REQUEST INTERCEPTOR
// ------------------------------------------------
// Har request BHEJNE SE PEHLE ye chalega
//
// Kya karta hai?
// localStorage se token lo
// Authorization header mein add karo
//
// Matlab:
// Har request mein automatically
// "Authorization: Bearer eyJ..."
// Add ho jayega!
// Manually add nahi karna padega!
// ------------------------------------------------

API.interceptors.request.use(
  (config) => {
    // localStorage se token lo
    const token = localStorage.getItem('token')

    // Token hai toh header mein add karo
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Modified config return karo
    return config
  },
  // Request error
  (error) => {
    return Promise.reject(error)
  }
)

// ------------------------------------------------
// RESPONSE INTERCEPTOR
// ------------------------------------------------
// Har response AANE KE BAAD ye chalega
//
// Kya karta hai?
// 401 = Unauthorized
// Token expire ya invalid
// → Token hatao
// → Login pe redirect karo
// ------------------------------------------------

API.interceptors.response.use(
  // Success response → seedha return karo
  (response) => response,

  // Error response → check karo
  (error) => {
    if (error.response?.status === 401) {
      // Token invalid hai
      // Hatao aur login pe bhejo
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }

    return Promise.reject(error)
  }
)

// Export karo
// Poore project mein yahi use hoga
export default API
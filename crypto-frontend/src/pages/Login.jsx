import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login, register } from '../api'

export default function Login() {
  const [email, setEmail] = useState('test@example.com')
  const [password, setPassword] = useState('Test@12345')
  const [name, setName] = useState('Test User')
  const [mode, setMode] = useState('login')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const onSubmit = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      if (mode === 'register') {
        await register(email, password, name)
      }
      const data = await login(email, password)
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      navigate('/')
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container" style={{maxWidth:480}}>
      <div className="card">
        <h2 style={{marginTop:0}}>{mode === 'login' ? 'Login' : 'Register'}</h2>
        <form onSubmit={onSubmit} className="row">
          {mode === 'register' && (
            <input className="input" placeholder="Full name" value={name} onChange={(e)=>setName(e.target.value)} required />
          )}
          <input className="input" placeholder="Email" type="email" value={email} onChange={(e)=>setEmail(e.target.value)} required />
          <input className="input" placeholder="Password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} required />
          {error && <div className="badge" style={{background:'var(--danger)'}}>{error}</div>}
          <button className="button" disabled={loading}>{loading ? 'Please wait...' : (mode === 'login' ? 'Login' : 'Create account')}</button>
        </form>
        <div style={{marginTop:12, color:'var(--muted)'}}>
          {mode === 'login' ? (
            <>No account? <button className="button" type="button" onClick={()=>setMode('register')}>Register</button></>
          ) : (
            <>Have an account? <button className="button" type="button" onClick={()=>setMode('login')}>Login</button></>
          )}
        </div>
      </div>
    </div>
  )
}
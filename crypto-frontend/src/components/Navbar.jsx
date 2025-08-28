import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const loggedIn = !!localStorage.getItem('access')
  return (
    <div className="nav">
      <div style={{fontWeight:700}}>₿ Crypto Task</div>
      <div>
        <NavLink to="/" className={({isActive}) => isActive ? 'active' : ''}>Dashboard</NavLink>
        <NavLink to="/wallet" className={({isActive}) => isActive ? 'active' : ''}>Wallet</NavLink>
        <NavLink to="/orders" className={({isActive}) => isActive ? 'active' : ''}>Orders</NavLink>
      </div>
      <div>
        {loggedIn ? (
          <button className="button" onClick={() => { localStorage.removeItem('access'); localStorage.removeItem('refresh'); navigate('/login') }}>Logout</button>
        ) : (
          <button className="button" onClick={() => navigate('/login')}>Login</button>
        )}
      </div>
    </div>
  )
}
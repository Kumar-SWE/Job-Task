import React, { useEffect, useState } from 'react'
import { ordersList } from '../api'

export default function Orders() {
  const [items, setItems] = useState([])
  const [err, setErr] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const res = await ordersList()
        setItems(res)
      } catch (e) {
        setErr('Please login to view orders.')
      }
    }
    load()
  }, [])

  if (err) return <div className="container"><div className="card">{err}</div></div>

  return (
    <div className="container">
      <div className="card">
        <h2 style={{marginTop:0}}>Orders</h2>
        {!items.length ? <div>No orders yet.</div> : (
          <table className="table">
            <thead><tr><th>Side</th><th>Symbol</th><th>Qty</th><th>Price (INR)</th><th>Amount (INR)</th><th>Status</th><th className="hide-sm">Time</th></tr></thead>
            <tbody>
              {items.map(o => (
                <tr key={o.id}>
                  <td><span className="badge" style={{background: o.side === 'BUY' ? 'var(--success)' : 'var(--danger)'}}>{o.side}</span></td>
                  <td>{o.symbol}</td>
                  <td>{o.qty}</td>
                  <td>₹ {o.price_inr}</td>
                  <td>₹ {o.amount_inr}</td>
                  <td>{o.status}</td>
                  <td className="hide-sm">{o.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
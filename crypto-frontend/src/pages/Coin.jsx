import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { currencyDetail, history, placeOrder } from '../api'

export default function Coin() {
  const { id } = useParams()
  const [detail, setDetail] = useState(null)
  const [hist, setHist] = useState([])
  const [qty, setQty] = useState('')
  const [side, setSide] = useState('BUY')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  useEffect(() => {
    async function load() {
      try {
        setMsg(''); setErr('')
        const d = await currencyDetail(id)
        setDetail(d)
        try {
          const h = await history(id)
          setHist(Array.isArray(h) ? h : [])
        } catch { setHist([]) }
      } catch (e) {
        setErr('Failed to load coin')
      }
    }
    load()
  }, [id])

  const submit = async (e) => {
    e.preventDefault()
    setMsg(''); setErr('')
    const q = Number(qty)
    if (!q || q <= 0) { setErr('Enter a valid quantity'); return }
    try {
      const symbol = (detail.symbol || id).toUpperCase()
      const res = await placeOrder(side, symbol, q)
      setMsg(`${res.side} ${res.qty} ${res.symbol} @ ₹${res.price_inr}`)
    } catch (e) {
      setErr(e?.response?.data?.detail || 'Order failed')
    }
  }

  return (
    <div className="container">
      <div className="card">
        {!detail ? <div>Loading...</div> : (
          <>
            <h2 style={{marginTop:0}}>{detail.name} ({detail.symbol?.toUpperCase()})</h2>
            <div className="row">
              <div style={{flex:1}}>
                <div className="badge" style={{background:'#1c2742', display:'inline-block'}}>Rank #{detail.rank ?? '—'}</div>
                <h3>₹ {detail.current_price_inr?.toLocaleString?.() || '—'}</h3>
                <p style={{color:'var(--muted)'}}>{detail.description || ''}</p>
              </div>
              <div style={{flex:1}}>
                <form onSubmit={submit} className="row">
                  <select className="select" value={side} onChange={(e)=>setSide(e.target.value)}>
                    <option value="BUY">BUY</option>
                    <option value="SELL">SELL</option>
                  </select>
                  <input className="input" placeholder="Quantity (e.g., 0.01)" value={qty} onChange={(e)=>setQty(e.target.value)} />
                  <button className="button">Place Order</button>
                  {msg && <div className="badge" style={{background:'var(--success)'}}>{msg}</div>}
                  {err && <div className="badge" style={{background:'var(--danger)'}}>{err}</div>}
                </form>
              </div>
            </div>
            <div style={{marginTop:16}}>
              <h3 style={{marginBottom:8}}>Recent Prices (OHLC)</h3>
              <div className="grid">
                {hist.slice(0,8).map((c, idx) => (
                  <div key={idx} className="card" style={{padding:'8px'}}>
                    <div style={{fontSize:12, color:'var(--muted)'}}>{c.ts}</div>
                    <div style={{display:'flex', gap:8, fontSize:14}}>
                      <div>O: ₹{c.open}</div>
                      <div>H: ₹{c.high}</div>
                      <div>L: ₹{c.low}</div>
                      <div>C: ₹{c.close}</div>
                    </div>
                  </div>
                ))}
                {!hist.length && <div>No history available.</div>}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

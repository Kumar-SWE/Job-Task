import React, { useEffect, useState } from 'react'
import { wallet, holdings } from '../api'

export default function WalletPage() {
  const [w, setW] = useState(null)
  const [h, setH] = useState([])
  const [err, setErr] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const [w1, h1] = await Promise.all([wallet(), holdings()])
        setW(w1); setH(h1)
      } catch (e) { setErr('Please login to view wallet.') }
    }
    load()
  }, [])

  if (err) return <div className="container"><div className="card">{err}</div></div>

  return (
    <div className="container">
      <div className="card">
        <h2 style={{marginTop:0}}>Wallet</h2>
        {!w ? 'Loading...' : (
          <div className="row">
            <div className="card" style={{flex:1}}>
              <div style={{color:'var(--muted)'}}>Currency</div>
              <div style={{fontSize:22, fontWeight:700}}>{w.currency_code}</div>
              <div style={{color:'var(--muted)'}}>Balance</div>
              <div style={{fontSize:22, fontWeight:700}}>₹ {Number(w.balance).toLocaleString?.()}</div>
            </div>
            <div className="card" style={{flex:2}}>
              <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                <h3 style={{margin:0}}>Holdings</h3>
              </div>
              {!h?.length ? <div>No holdings yet.</div> : (
                <table className="table">
                  <thead><tr><th>Symbol</th><th>Quantity</th><th>Avg Cost (INR)</th><th className="hide-sm">Updated</th></tr></thead>
                  <tbody>
                    {h.map(x => (
                      <tr key={x.id}>
                        <td>{x.symbol}</td>
                        <td>{x.quantity}</td>
                        <td>₹ {x.avg_cost_inr}</td>
                        <td className="hide-sm">{x.updated_at}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
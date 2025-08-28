import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listCurrencies, prices } from '../api'

export default function Dashboard() {
  const [coins, setCoins] = useState([])
  const [priceMap, setPriceMap] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const cur = await listCurrencies()
        setCoins(cur)
        if (cur.length) {
          const ids = cur.map(c => c.id)
          const p = await prices(ids)
          setPriceMap(p)
        }
      } catch (e) {
        setError('Failed to load market data')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) return <div className="container"><div className="card">Loading...</div></div>
  if (error) return <div className="container"><div className="card">{error}</div></div>

  return (
    <div className="container">
      <div className="card">
        <div className="row" style={{justifyContent:'space-between', alignItems:'center'}}>
          <h2 style={{margin:0}}>Market</h2>
        </div>
        <table className="table">
          <thead>
            <tr><th>Coin</th><th className="hide-sm">Symbol</th><th>INR Price</th><th className="hide-sm">Rank</th></tr>
          </thead>
          <tbody>
            {coins.map(c => {
              const p = priceMap[c.id]?.inr ?? priceMap[c.symbol?.toLowerCase()]?.inr
              return (
                <tr key={c.id}>
                  <td><Link to={`/coin/${c.id}`}>{c.name}</Link></td>
                  <td className="hide-sm">{c.symbol}</td>
                  <td>₹ {p ? p.toLocaleString() : '—'}</td>
                  <td className="hide-sm">{c.rank ?? '—'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
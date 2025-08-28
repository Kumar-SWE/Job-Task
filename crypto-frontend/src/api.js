import axios from 'axios'

const MARKET_BASE_URL = import.meta.env.VITE_MARKET_BASE_URL || 'http://127.0.0.1:8001'
const USER_BASE_URL = import.meta.env.VITE_USER_BASE_URL || 'http://127.0.0.1:8000/api/v1'

export const market = axios.create({ baseURL: `${MARKET_BASE_URL}/api/v1` })
export const userApi = axios.create({ baseURL: USER_BASE_URL })


userApi.defaults.headers.post['Content-Type'] = 'application/json'


userApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})


export async function login(email, password) {

  const res = await userApi.post('auth/login', {
    username: email,   
    password: password,
  })
  return res.data
}

export async function register(email, password, name) {

  const res = await userApi.post('auth/register', {
    username: email,   
    password: password,
    name: name,     
  })
  return res.data
}

export async function me() {
  const res = await userApi.get('auth/me')
  return res.data
}


export async function listCurrencies() {
  const res = await market.get('currencies')
  return res.data
}

export async function prices(ids) {
  const res = await market.get('prices', { params: { ids: ids.join(','), fiat: 'inr' } })
  const data = res.data.__root__ || res.data
  return data
}

export async function currencyDetail(id) {
  const res = await market.get(`currencies/${id}`)
  return res.data
}

export async function history(id) {
  const res = await market.get(`history/${id}`)
  return res.data
}


export async function wallet() {
  const res = await userApi.get('wallet')
  return res.data
}

export async function holdings() {
  const res = await userApi.get('holdings')
  return res.data
}

export async function ordersList() {
  const res = await userApi.get('orders')
  return res.data
}

export async function placeOrder(side, symbol, qty) {
  const res = await userApi.post('orders', { side, symbol, qty })
  return res.data
}

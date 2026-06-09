import Taro from '@tarojs/taro'
import { API_BASE_URL } from '../constants/config'
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from '../utils/storage'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, any>
}

// 后端统一响应结构
interface ApiResponse<T> {
  code: number
  message: string
  data: T
  timestamp: number
}

// 防止刷新风暴：并发 401 时只发起一次刷新，其余请求等同一个 Promise
let refreshing: Promise<boolean> | null = null

// 用裸 Taro.request 调刷新接口，避免经过 request() 造成递归
async function doRefresh(): Promise<boolean> {
  const refreshToken = getRefreshToken()
  if (!refreshToken) return false
  try {
    const res = await Taro.request({
      url: `${API_BASE_URL}/api/v1/user/auth/refresh`,
      method: 'POST',
      data: { refresh_token: refreshToken },
      header: { 'Content-Type': 'application/json' },
    })
    const body = res.data as ApiResponse<{ access_token: string; refresh_token: string }>
    if (res.statusCode === 200 && body.code === 0) {
      setTokens(body.data.access_token, body.data.refresh_token)
      return true
    }
    return false
  } catch {
    return false
  }
}

async function ensureRefreshed(): Promise<boolean> {
  if (!refreshing) {
    refreshing = doRefresh().finally(() => {
      refreshing = null
    })
  }
  return refreshing
}

export async function request<T = any>(options: RequestOptions): Promise<T> {
  const send = async (): Promise<Taro.request.SuccessCallbackResult> => {
    const token = getAccessToken()
    return Taro.request({
      url: `${API_BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    })
  }

  let res: Taro.request.SuccessCallbackResult
  try {
    res = await send()
  } catch {
    Taro.showToast({ title: '网络异常', icon: 'none' })
    throw new Error('network error')
  }

  // 401：尝试刷新后重发一次
  if (res.statusCode === 401) {
    const ok = await ensureRefreshed()
    if (!ok) {
      clearTokens()
      Taro.showToast({ title: '请重新登录', icon: 'none' })
      throw new Error('unauthorized')
    }
    try {
      res = await send()
    } catch {
      Taro.showToast({ title: '网络异常', icon: 'none' })
      throw new Error('network error')
    }
  }

  const body = res.data as ApiResponse<T>
  if (body.code !== 0) {
    Taro.showToast({ title: body.message || '请求失败', icon: 'none' })
    throw new Error(body.message || 'business error')
  }
  return body.data
}

import { createContext, useContext, useState, useCallback, ReactNode } from 'react'
import { setTokens, clearTokens, getAccessToken } from '../utils/storage'
import { login as apiLogin, getMe, wxLoginCode } from '../services/user'

interface AuthState {
  isLoggedIn: boolean
  userId: number | null
  // 首次登录：wx.login → 换 token → 存储 → 拉 /me
  loginWithWechat: () => Promise<void>
  // 启动时恢复登录态：有 token 就拉 /me 验证
  restore: () => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthState | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userId, setUserId] = useState<number | null>(null)

  const loginWithWechat = useCallback(async () => {
    const code = await wxLoginCode()
    const tokens = await apiLogin(code)
    setTokens(tokens.access_token, tokens.refresh_token)
    const me = await getMe()
    setUserId(me.user_id)
    setIsLoggedIn(true)
  }, [])

  const restore = useCallback(async () => {
    if (!getAccessToken()) return
    try {
      const me = await getMe()
      setUserId(me.user_id)
      setIsLoggedIn(true)
    } catch {
      // getMe 内部已处理 401 刷新；走到这里说明刷新也失败，保持未登录
      setIsLoggedIn(false)
      setUserId(null)
    }
  }, [])

  const logout = useCallback(() => {
    clearTokens()
    setIsLoggedIn(false)
    setUserId(null)
  }, [])

  return (
    <AuthContext.Provider value={{ isLoggedIn, userId, loginWithWechat, restore, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth 必须在 AuthProvider 内使用')
  return ctx
}

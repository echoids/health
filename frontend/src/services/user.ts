import Taro from '@tarojs/taro'
import { request } from './request'

interface LoginResult {
  access_token: string
  refresh_token: string
}

interface MeResult {
  user_id: number
}

// 用微信 code 换 token
export async function login(code: string): Promise<LoginResult> {
  return request<LoginResult>({
    url: '/api/v1/user/auth/login',
    method: 'POST',
    data: { code },
  })
}

// 获取当前登录用户信息（带 token，验证登录态）
export async function getMe(): Promise<MeResult> {
  return request<MeResult>({
    url: '/api/v1/user/me',
    method: 'GET',
  })
}

// 调微信 wx.login 拿 code（静默，不需要用户授权）
export async function wxLoginCode(): Promise<string> {
  const res = await Taro.login()
  if (!res.code) throw new Error('wx.login 失败')
  return res.code
}

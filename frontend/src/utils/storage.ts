import Taro from '@tarojs/taro'
import { STORAGE_KEYS } from '../constants/config'

export function getAccessToken(): string {
  return Taro.getStorageSync(STORAGE_KEYS.ACCESS_TOKEN) || ''
}

export function getRefreshToken(): string {
  return Taro.getStorageSync(STORAGE_KEYS.REFRESH_TOKEN) || ''
}

export function setTokens(accessToken: string, refreshToken: string): void {
  Taro.setStorageSync(STORAGE_KEYS.ACCESS_TOKEN, accessToken)
  Taro.setStorageSync(STORAGE_KEYS.REFRESH_TOKEN, refreshToken)
}

export function clearTokens(): void {
  Taro.removeStorageSync(STORAGE_KEYS.ACCESS_TOKEN)
  Taro.removeStorageSync(STORAGE_KEYS.REFRESH_TOKEN)
}

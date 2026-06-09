// 后端 API 基础地址。本地调试时指向本机后端；上线改为线上域名。
// 微信开发者工具需在「详情 → 本地设置」勾选「不校验合法域名」才能用 localhost/IP。
export const API_BASE_URL = 'http://localhost:8000'

// 本地存储 key
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
} as const

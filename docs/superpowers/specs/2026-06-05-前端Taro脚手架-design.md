# 前端 Taro 脚手架 - 设计文档

## 文档信息

- **项目名称**: AI健康生活助手 - 前端 Taro 脚手架
- **文档类型**: 设计文档（spec）
- **创建日期**: 2026-06-05
- **范围**: 仅前端脚手架（含一个后端 refresh 接口补充）。功能页面（建档/记录/周报/问答）留到后续子项目。

## 1. 目标

搭建可在微信开发者工具中运行的 Taro 小程序前端骨架，打通：项目结构 + 微信登录链路 + JWT token 自动刷新 + 网络请求封装。MVP 范围，<1000 用户。

## 2. 技术决策

| 项 | 选择 | 理由 |
|---|---|---|
| 创建方式 | Taro CLI 模板（React + TypeScript） | 配置文件多（project.config.json / babel / tsconfig），CLI 生成不易踩坑 |
| 状态管理 | React Context + useState | MVP 阶段登录态简单，不引第三方库（YAGNI） |
| UI 组件库 | NutUI（@nutui/nutui-react-taro） | 专为 Taro 小程序设计，开箱即用 |
| 页面范围 | 2 个 Tab：首页 + 我的 | 脚手架目标是跑通骨架+登录链路，功能页留到对应子项目 |
| 登录方式 | 首次用户点按钮授权登录，之后 refresh_token 自动刷新 | 微信现状：getUserProfile 需用户点按钮；refresh_token 30 天有效，比每次 wx.login 更标准 |

## 3. 后端改动（先做，前端依赖它）

后端当前只有 `POST /auth/login` 和 `GET /me`，缺少刷新接口。新增：

```
POST /api/v1/user/auth/refresh
  请求: { "refresh_token": "xxx" }
  逻辑: decode_token → 校验 payload.type == "refresh" → 重新签发一对新 token
  返回: success({ access_token, refresh_token })
  失败: refresh_token 无效/过期/类型不符 → BusinessError(40101, "登录已过期")
```

涉及文件：
- `backend/app/modules/user/schemas.py` — 加 `RefreshRequest`
- `backend/app/modules/user/service.py` — 加 `refresh(refresh_token: str) -> dict`
- `backend/app/modules/user/router.py` — 加 `POST /auth/refresh` 路由
- `backend/tests/test_user_login.py` — 加测试（刷新成功 / refresh_token 被拒 / access_token 当 refresh 用被拒）

复用现有 `decode_token`、`create_access_token`、`create_refresh_token`。

## 4. 前端目录结构

```
frontend/
├── config/                  # Taro 构建配置（CLI 生成）
├── src/
│   ├── app.tsx              # 应用入口（包 AuthProvider + 启动时恢复登录态）
│   ├── app.config.ts        # 全局配置（tabBar 2 个 Tab + 页面注册）
│   ├── pages/
│   │   ├── index/           # 首页（占位 + 登录态展示）
│   │   └── profile/         # 我的（登录按钮 + 用户信息）
│   ├── services/
│   │   ├── request.ts       # 网络请求封装（核心）
│   │   └── user.ts          # 用户 API（login / refresh / getMe）
│   ├── store/
│   │   └── auth.tsx         # AuthContext（token + 用户态 + 登录/登出方法）
│   ├── utils/
│   │   └── storage.ts       # Taro.setStorageSync / getStorageSync 封装
│   └── constants/
│       └── config.ts        # API baseURL 等常量
├── package.json
├── tsconfig.json
└── project.config.json      # 小程序配置（填 AppID）
```

每个单元职责单一：
- `request.ts` — 只负责 HTTP 通信、token 注入、统一响应解包、401 刷新
- `auth.tsx` — 只负责登录态（token 存哪、当前用户是谁、login/logout）
- `user.ts` — 只负责拼装用户相关 API 调用
- `storage.ts` — 只负责本地存储读写

## 5. 登录 + token 刷新链路

**首次登录**（用户在「我的」页点登录按钮）：
```
wx.login() 拿 code
  → POST /auth/login { code }
  → 拿到 { access_token, refresh_token }
  → 存 Storage + 写入 AuthContext（已登录态）
  → 可选：wx.getUserProfile 拿头像昵称展示
```

**后续启动**（app.tsx 里恢复登录态）：
```
读 Storage 里的 token
  → 无 token → 未登录态
  → 有 token → 设为已登录态，调 /me 验证
       · /me 成功 → 保持登录态
       · /me 返回 401 → 用 refresh_token 换新 token；刷新成功保持，失败则清空回未登录
```

**请求自动刷新**（request.ts 拦截）：
```
任何业务请求返回 HTTP 401
  → 自动用 refresh_token 调 /auth/refresh
  → 成功 → 用新 token 重发原请求
  → 失败 → 清登录态，提示重新登录
```

## 6. 请求封装（request.ts）

```
request<T>(options): Promise<T>
  - 自动拼 baseURL（来自 constants/config.ts）
  - 自动注入 Authorization: Bearer <access_token>
  - 解包后端统一响应 { code, message, data, timestamp }
       · code === 0 → 返回 data
       · code !== 0 → 抛业务错误（toast 提示 message）
  - HTTP 401 → 触发刷新流程（见第 5 节），刷新后重发原请求
  - 网络错误 → 统一 toast「网络异常」
  - 防止刷新风暴：并发 401 时只刷新一次，其余请求排队等同一个刷新结果
```

## 7. 测试策略

- **后端 refresh 接口**：照常写 pytest 单元测试（3 个：刷新成功 / refresh_token 被拒 / access_token 当 refresh 用被拒）。
- **前端**：脚手架阶段不强制单测，依赖**微信开发者工具**手动验证——登录链路跑通 + /me 能拿到 user_id。前端单测留到有复杂业务逻辑时再引入。

## 8. 范围说明

本设计仅覆盖前端脚手架 + 后端 refresh 接口。明确不在范围内：
- 建档表单、AI 建议、每日记录、周报、问答等功能页（各自独立子项目）
- 前端单元测试框架
- 第三方状态管理库
- 记录/周报/问答 Tab 页

## 9. 验收标准

1. `frontend/` 项目能在微信开发者工具中编译运行。
2. 底部有 2 个 Tab（首页 / 我的）。
3. 「我的」页点登录按钮 → 完成微信登录 → 拿到并存储 token。
4. 登录后调 `/me` 能拿到 user_id 并展示。
5. token 过期时能用 refresh_token 自动换新 token，无需重新登录。
6. 后端 refresh 接口单元测试通过。

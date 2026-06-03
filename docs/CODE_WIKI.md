# AI健康生活助手 - Code Wiki 文档

---

## 1. 项目概述

### 1.1 项目定位

**AI健康生活助手** 是一款轻量级AI健康生活管理工具，帮助普通用户改善饮食、运动、作息和体重管理。

| 属性 | 值 |
|------|-----|
| 产品形态 | 微信小程序 + Web(移动端 + PC) |
| 商业模式 | 免费基础功能 + 订阅会员 + 增值服务 |
| 核心价值 | 用户愿意每天打开、轻量记录、获得AI个性化建议 |

### 1.2 核心闭环

```
建档 → 初始建议 → 每日记录 → 周小结 → 调整改进
```

### 1.3 项目状态

| 阶段 | 状态 |
|------|------|
| 产品需求定义 | ✅ 完成 |
| AI调用规则定义 | ✅ 完成 |
| 技术架构设计 | ✅ 完成 |
| 数据库设计 | ✅ 完成 |
| API接口设计 | ✅ 完成 |
| 开发实施 | ⬜ 待开始 |

---

## 2. 技术架构

### 2.1 系统架构图

```
┌─────────────────┐
│  微信小程序      │
│  (Taro + React) │
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────────────────────────┐
│         Nginx (反向代理 + SSL)       │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│      FastAPI 应用服务器              │
│  ┌─────────────────────────────┐   │
│  │  API 路由层                  │   │
│  ├─────────────────────────────┤   │
│  │  业务模块 (领域驱动)          │   │
│  │  • user    (用户档案)        │   │
│  │  • diet    (饮食记录)        │   │
│  │  • record  (生活方式记录)     │   │
│  │  • ai      (AI服务封装)      │   │
│  │  • report  (周小结)          │   │
│  │  • qa      (AI问答)          │   │
│  ├─────────────────────────────┤   │
│  │  通用层                      │   │
│  │  • 认证中间件                │   │
│  │  • 限流中间件                │   │
│  │  • 日志/监控                 │   │
│  └─────────────────────────────┘   │
└────┬──────────────────┬─────────────┘
     │                  │
     ↓                  ↓
┌──────────┐      ┌──────────┐
│  MySQL   │      │  Redis   │
│  (主存储) │      │ (缓存+队列)│
└──────────┘      └──────────┘
     │
     ↓
┌──────────────────┐
│  DeepSeek API    │
│  (AI服务)        │
└──────────────────┘
```

### 2.2 核心技术栈

| 层级 | 技术选型 | 版本 | 说明 |
|------|---------|------|------|
| 前端 | Taro | 3.6+ | React框架，支持小程序 |
| 前端 | React | 18+ | UI框架 |
| 前端 | TypeScript | 5.0+ | 类型安全 |
| 后端 | Python | 3.11+ | 主语言 |
| 后端 | FastAPI | 0.104+ | Web框架 |
| 后端 | SQLAlchemy | 2.0+ | ORM |
| 后端 | Pydantic | 2.0+ | 数据验证 |
| 数据库 | MySQL | 8.0+ | 主存储 |
| 缓存 | Redis | 7.0+ | 缓存+队列 |
| AI | DeepSeek SDK | 最新 | AI调用 |
| 部署 | Docker | 24+ | 容器化 |
| 部署 | Docker Compose | 2.0+ | 编排 |
| Web服务器 | Nginx | 1.24+ | 反向代理 |

---

## 3. 项目目录结构

```
meishi/
├── backend/                      # 后端服务
│   ├── app/
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置管理
│   │   ├── dependencies.py      # 依赖注入
│   │   │
│   │   ├── modules/             # 业务模块（领域驱动）
│   │   │   ├── user/           # 用户模块
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   ├── diet/           # 饮食记录模块
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   ├── record/         # 生活方式记录模块
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   ├── ai/             # AI服务模块
│   │   │   │   ├── client.py
│   │   │   │   ├── prompts.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   ├── report/         # 周小结模块
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   └── qa/             # AI问答模块
│   │   │       ├── models.py
│   │   │       ├── schemas.py
│   │   │       ├── service.py
│   │   │       └── router.py
│   │   │
│   │   ├── common/             # 通用层
│   │   │   ├── database.py
│   │   │   ├── redis.py
│   │   │   ├── auth.py
│   │   │   ├── limiter.py
│   │   │   ├── logger.py
│   │   │   ├── exceptions.py
│   │   │   └── utils.py
│   │   │
│   │   └── tasks/              # 定时任务
│   │       ├── scheduler.py
│   │       └── weekly_report.py
│   │
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # 前端（Taro小程序）
│   ├── src/
│   │   ├── pages/
│   │   │   ├── index/
│   │   │   ├── profile/
│   │   │   ├── record/
│   │   │   ├── report/
│   │   │   └── qa/
│   │   ├── components/
│   │   ├── services/
│   │   ├── store/
│   │   ├── utils/
│   │   └── app.tsx
│   ├── config/
│   ├── package.json
│   └── project.config.json
│
├── docker/
│   ├── nginx/nginx.conf
│   └── docker-compose.yml
│
└── docs/
    ├── 01-产品需求文档.md
    ├── 02-AI调用规则.md
    ├── iterations/
    └── CODE_WIKI.md             # 本文档
```

---

## 4. 主要模块职责

### 4.1 用户模块 (`modules/user/`)

**职责**: 管理用户身份认证、用户档案和会员状态

| 文件 | 职责 |
|------|------|
| `models.py` | 用户表、用户档案表的数据库模型定义 |
| `schemas.py` | 用户相关的数据验证和序列化模型 |
| `service.py` | 用户业务逻辑（登录、档案创建/更新、会员状态查询） |
| `router.py` | 用户相关API路由定义 |

**核心功能**:
- 微信登录认证
- 用户档案创建与更新
- 会员状态管理
- 用户上下文标签生成

### 4.2 饮食记录模块 (`modules/diet/`)

**职责**: 处理饮食记录的提交、查询和AI反馈

| 文件 | 职责 |
|------|------|
| `models.py` | 饮食记录表模型定义 |
| `schemas.py` | 饮食记录的数据验证和序列化模型 |
| `service.py` | 饮食记录业务逻辑（提交、查询、AI反馈生成） |
| `router.py` | 饮食记录相关API路由定义 |

**核心功能**:
- 饮食记录提交（文字/图片）
- AI即时反馈生成
- 饮食记录查询与管理

### 4.3 生活方式记录模块 (`modules/record/`)

**职责**: 管理体重、饮水、运动、睡眠等生活方式记录

| 文件 | 职责 |
|------|------|
| `models.py` | 生活方式记录表、每日完成度表模型定义 |
| `schemas.py` | 生活方式记录的数据验证和序列化模型 |
| `service.py` | 生活方式记录业务逻辑 |
| `router.py` | 生活方式记录相关API路由定义 |

**核心功能**:
- 体重记录
- 饮水记录
- 运动记录
- 睡眠记录
- 每日完成度确认

### 4.4 AI服务模块 (`modules/ai/`)

**职责**: AI服务封装，处理AI调用和结果生成

| 文件 | 职责 |
|------|------|
| `client.py` | DeepSeek API客户端封装 |
| `prompts.py` | Prompt模板定义 |
| `service.py` | AI服务业务逻辑 |
| `router.py` | AI相关API路由定义 |

**核心功能**:
- 初始建议卡片生成（流式输出）
- 饮食反馈生成
- AI调用成本控制
- 安全规则拦截

### 4.5 周小结模块 (`modules/report/`)

**职责**: 周小结的生成、查询和用户反馈收集

| 文件 | 职责 |
|------|------|
| `models.py` | AI生成内容表、每周感受反馈表模型定义 |
| `schemas.py` | 周小结相关的数据验证和序列化模型 |
| `service.py` | 周小结业务逻辑（模板生成、AI生成） |
| `router.py` | 周小结相关API路由定义 |

**核心功能**:
- 免费版周小结模板生成
- 会员版AI周小结生成
- 每周感受反馈收集
- 定时任务触发

### 4.6 AI问答模块 (`modules/qa/`)

**职责**: 处理用户的AI问答请求

| 文件 | 职责 |
|------|------|
| `models.py` | QA记录表模型定义 |
| `schemas.py` | QA相关的数据验证和序列化模型 |
| `service.py` | QA业务逻辑（提问、历史查询、限频） |
| `router.py` | QA相关API路由定义 |

**核心功能**:
- 单轮问答处理
- 问答历史查询
- 问答次数限制

### 4.7 通用层 (`common/`)

**职责**: 提供通用基础设施和工具

| 文件 | 职责 |
|------|------|
| `database.py` | 数据库连接和会话管理 |
| `redis.py` | Redis客户端封装 |
| `auth.py` | JWT认证中间件 |
| `limiter.py` | 限流中间件 |
| `logger.py` | 日志配置 |
| `exceptions.py` | 自定义异常定义 |
| `utils.py` | 通用工具函数 |

---

## 5. 数据库设计

### 5.1 核心表结构

| 表名 | 核心字段 | 用途 |
|------|----------|------|
| `users` | id, openid, nickname, is_member, member_expire_at | 用户基础信息 |
| `user_profiles` | id, user_id, gender, birth_year, height, weight, main_goal, dietary_preferences(JSON), lifestyle_answers(JSON) | 用户健康档案 |
| `diet_records` | id, user_id, record_date, meal_type, content_type, text_content, image_url, ai_feedback(JSON) | 饮食记录 |
| `lifestyle_records` | id, user_id, record_date, record_type, value, notes | 生活方式记录（体重、饮水、运动、睡眠） |
| `daily_completion` | id, user_id, record_date, completion_status | 每日完成度 |
| `ai_generated_content` | id, user_id, content_type, content(JSON), week_start_date | AI生成内容持久化 |
| `weekly_feedback` | id, user_id, week_start_date, energy_level, sleep_quality, digestion_status | 每周感受反馈 |
| `qa_records` | id, user_id, question, answer, context_snapshot(JSON) | AI问答记录 |
| `api_call_logs` | id, user_id, endpoint, input_tokens, output_tokens, cost, response_time | API调用日志（成本核算） |

### 5.2 Redis缓存键设计

| 缓存键 | 用途 | 过期策略 |
|--------|------|----------|
| `user:profile:{user_id}` | 用户档案缓存 | 1小时 |
| `ai:initial_advice:{user_id}` | 初始建议缓存 | 持久 |
| `ai:weekly_report:{user_id}:{week_start_date}` | 周小结缓存 | 持久 |
| `qa:dedup:{user_id}:{question_hash}` | 问答去重 | 5分钟 |
| `limit:diet_feedback:{user_id}:{date}` | 饮食反馈次数限制 | 1天 |
| `limit:qa:{user_id}:{date}` | 问答次数限制 | 1天 |
| `queue:weekly_report` | 周小结任务队列 | - |

---

## 6. API接口设计

### 6.1 基础规范

- **Base URL**: `https://api.yourdomain.com/v1`
- **认证方式**: JWT Token（微信登录后颁发）
- **统一响应格式**: 
  ```json
  { "code": 0, "message": "success", "data": {}, "timestamp": 123 }
  ```

### 6.2 接口清单

| 模块 | 方法 | 路径 | 功能 |
|------|------|------|------|
| 用户 | POST | `/api/v1/user/auth/login` | 微信登录 |
| 用户 | GET | `/api/v1/user/profile` | 获取用户档案 |
| 用户 | POST | `/api/v1/user/profile` | 创建/更新档案 |
| 用户 | GET | `/api/v1/user/member/status` | 获取会员状态 |
| 饮食 | POST | `/api/v1/diet/records` | 提交饮食记录（含AI反馈） |
| 饮食 | GET | `/api/v1/diet/records` | 查询饮食记录（分页） |
| 饮食 | GET | `/api/v1/diet/records/:id` | 获取单条记录 |
| 饮食 | DELETE | `/api/v1/diet/records/:id` | 删除记录 |
| 记录 | POST | `/api/v1/record/weight` | 记录体重 |
| 记录 | POST | `/api/v1/record/water` | 记录饮水 |
| 记录 | POST | `/api/v1/record/exercise` | 记录运动 |
| 记录 | POST | `/api/v1/record/sleep` | 记录睡眠 |
| 记录 | GET | `/api/v1/record/history` | 查询历史 |
| 记录 | POST | `/api/v1/record/completion` | 提交每日完成度 |
| AI | GET | `/api/v1/ai/initial-advice` | 获取初始建议卡片 |
| AI | POST | `/api/v1/ai/initial-advice/regenerate` | 重新生成（会员） |
| 报告 | GET | `/api/v1/report/weekly` | 获取周小结列表 |
| 报告 | GET | `/api/v1/report/weekly/:week_start` | 获取指定周小结 |
| 报告 | POST | `/api/v1/report/weekly/feedback` | 提交每周感受反馈 |
| QA | POST | `/api/v1/qa/ask` | 提问 |
| QA | GET | `/api/v1/qa/history` | 问答历史 |
| QA | GET | `/api/v1/qa/quota` | 查询剩余次数 |

---

## 7. AI调用架构

### 7.1 四个触点实现模式

| 触点 | 触发时机 | 调用方式 | 超时 | 失败处理 |
|------|----------|----------|------|----------|
| 饮食反馈 | 用户提交饮食记录后 | 同步非流式 | 3秒 | 降级返回"已记录" |
| 初始建议 | 建档完成后 | 同步流式 | 60秒 | 缓存已生成部分+重试入口 |
| 周小结 | 每周日20:00 | 异步队列 | 30秒 | 降级为免费版模板 |
| AI问答 | 用户主动提问 | 同步非流式 | 8秒 | 返回"AI暂时忙" |

### 7.2 成本控制策略

1. **结果持久化**: 初始建议、周小结存数据库，复看不重新调用
2. **频次限制**: 饮食反馈免费3次/天，问答免费3次/天
3. **Prompt Cache**: DeepSeek原生支持，系统提示词缓存命中率>90%
4. **请求去重**: 同一用户5分钟内相同问题返回缓存

### 7.3 安全规则

**全局禁用词**:
- 评判类：超标 / 过量 / 不健康 / 危险 / 警告 / 异常 / 失败 / 退步
- 医疗类：疾病 / 诊断 / 治疗 / 治愈 / 药物 / 处方
- 绝对类：应该 / 必须 / 不可以 / 一定要

**预设拦截规则**:
| 触发关键词 | 返回内容 |
|------------|----------|
| 自残 / 轻生 / 不想活 | 心理援助热线 010-82951332 + 关怀文案 |
| 处方药名 / 用药剂量 | 引导咨询医生或药师 |
| 怀孕 + 用药 / 流产 | 引导就医 |
| 减肥药 / 泻药 / 催吐 | 健康提醒 + 引导专业帮助 |

---

## 8. 部署方案

### 8.1 Docker Compose架构

```yaml
services:
  nginx:    # 反向代理 + SSL
  backend:  # FastAPI应用（Python 3.11）
  mysql:    # MySQL 8.0 + 数据持久化
  redis:    # Redis 7.0 + 数据持久化
```

### 8.2 服务器配置

| 环境 | 配置 | 月成本 |
|------|------|--------|
| 开发 | 本地Docker | 免费 |
| 测试 | 2核2G ECS | ¥100 |
| 生产 | 2核4G ECS | ¥200-300 |

### 8.3 扩展路径

```
阶段1（MVP，<1000用户）: 单体应用，单台服务器
阶段2（1万用户）:         Nginx负载均衡，2-3台应用服务器
阶段3（10万用户）:        微服务拆分，消息队列
```

---

## 9. 安全设计

- **认证**: 微信登录 → JWT Token（7天）+ Refresh Token（30天）
- **限流**: IP级别100次/分钟，用户级别1000次/小时
- **API安全**: HTTPS强制，CORS限制小程序域名，ORM防SQL注入
- **AI安全**: 关键词预拦截 + 禁用词检测 + 内容安全API接入

---

## 10. 监控指标

- API响应时间（P50/P95/P99）
- AI调用成功率及响应时间（按触点）
- 每用户每日AI调用次数（异常检测）
- AI输出格式错误率
- 数据库连接池状态
- Redis内存使用率

---

## 11. 启动方式

### 11.1 开发环境

```bash
# 进入项目目录
cd meishi

# 启动后端服务（Docker方式）
cd backend
docker-compose up -d

# 或者本地运行
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 启动前端
cd frontend
npm install
npm run dev:h5  # H5开发
npm run dev:weapp  # 小程序开发
```

### 11.2 生产环境

```bash
# 构建Docker镜像
cd meishi
docker-compose build

# 启动服务
docker-compose up -d
```

---

## 12. 文档阅读指南

| 文档 | 阅读时间 | 用途 |
|------|----------|------|
| [README.md](README.md) | 5分钟 | 项目定位和状态概览 |
| [01-产品需求文档.md](01-产品需求文档.md) | 15分钟 | 产品功能定义和用户旅程 |
| [02-AI调用规则.md](02-AI调用规则.md) | 15分钟 | AI触点规则、安全边界、成本控制 |
| [iterations/](iterations/) | 按需 | 关键决策的来龙去脉 |
| [CODE_WIKI.md](CODE_WIKI.md) | 本文档 | 技术架构和实现指南 |

---

**版本**: v1.0  
**最后更新**: 2026-06-01  
**适用项目**: AI健康生活助手
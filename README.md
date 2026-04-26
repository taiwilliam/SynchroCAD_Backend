# SynchroCAD Backend

> 一套用於管理工業零件（CAD 圖檔、3D 模型）的後端服務，採用分層架構設計，並完整部署於 AWS 雲端環境。本專案為全端能力展示作品，涵蓋 RESTful API 設計、雲端架構規劃、容器化部署與 CI/CD 自動化流程。

---

## 技術棧

| 分類 | 技術 |
|---|---|
| 語言 | Python 3.11 |
| 框架 | Flask |
| ORM | Flask-SQLAlchemy |
| 資料庫遷移 | Flask-Migrate（Alembic） |
| 資料庫 | PostgreSQL 15 |
| 雲端儲存 | AWS S3（boto3） |
| 跨域處理 | Flask-CORS |
| API 文件 | Flasgger（Swagger UI） |
| Web Server | Nginx（Reverse Proxy） |
| 容器化 | Docker、Docker Compose |
| CI/CD | GitHub Actions |
| 雲端平台 | AWS EC2、AWS S3、AWS IAM |

---

## AWS 雲端架構

```
┌─────────────────────────────────────────────────────────┐
│                        Internet                         │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────┐     ┌────────────────────────────┐
│   AWS S3 (Frontend)  │     │      AWS EC2 (Backend)     │
│                      │     │                            │
│  Static Website      │     │  ┌──────────────────────┐  │
│  s3-website hosting  │     │  │  Nginx (Port 80)     │  │
│                      │     │  │  Reverse Proxy       │  │
│  Angular SPA         │────▶│ └──────────┬───────────┘  │
│                      │     │             │              │
└──────────────────────┘     │  ┌──────────▼───────────┐  │
                             │  │  Flask               │  │
                             │  │  REST API Server     │  │
┌──────────────────────┐     │  └──────────┬───────────┘  │
│  AWS S3 (File Store) │     │             │              │
│                      │◀────│  ┌──────────▼───────────┐ │
│  DXF/  → CAD 圖檔    │     │  │  PostgreSQL DB       │  │
│  GLB/  → 3D 模型     │     │  └──────────────────────┘  │
│                      │     │                            │
└──────────────────────┘     └────────────────────────────┘
```

### 各服務職責

- **S3（前端）** — 靜態網站 hosting，SPA 前端部署於此，對外公開
- **S3（檔案）** — 儲存零件的 DXF 及 GLB 檔案，IAM 控管存取權限，只允許後端寫入
- **EC2（後端）** — 運行 Docker Compose，包含 Nginx、Flask、PostgreSQL 三個容器
- **IAM** — 建立最小權限原則的 User Policy，後端只具備 `PutObject / GetObject / DeleteObject` 權限

---

## 後端架構設計

採用四層分離架構，確保各層職責單一、易於維護與擴充：

```
Request
   │
   ▼
Router          路由定義、HTTP method 對應
   │
   ▼
Controller      請求驗證、回應格式化
   │
   ▼
Service         商業邏輯處理
   │
   ▼
Repository      資料庫存取（SQLAlchemy ORM）
   │
   ▼
PostgreSQL
```

---

## S3 檔案上傳設計

上傳流程採**後端代理**模式：

```
前端
  │  POST /api/parts/:id/upload
  │  multipart/form-data: { folder, field, file }
  ▼
EC2 Flask Backend
  │  boto3 upload_fileobj()
  │  自動偵測 ContentType（mimetypes）
  │  大檔自動分片（multipart threshold 8MB）
  ▼
AWS S3
  │  DXF/{filename}  或  GLB/{filename}
  ▼
DB 存 key，API 序列化時動態轉為完整 URL
```

---

## API 設計

Base URL：`/api`

| Method | Endpoint | 說明 |
|---|---|---|
| GET | `/api/parts` | 取得所有零件列表 |
| GET | `/api/parts/:id` | 取得單一零件 |
| POST | `/api/parts` | 新增零件 |
| PUT | `/api/parts/:id` | 更新零件資料 |
| DELETE | `/api/parts/:id` | 刪除零件 |
| POST | `/api/parts/:id/upload` | 上傳 CAD / GLB 檔案至 S3 |
| GET | `/apidocs` | Swagger API 文件介面 |

---

## CI/CD 自動化部署

使用 **GitHub Actions** 在 push 到 `master` 時自動觸發部署：

```
git push origin master
        │
        ▼
GitHub Actions (ubuntu-latest)
        │
        ▼
SSH 連線至 EC2
        │
        ├── git pull --ff-only origin master
        ├── docker compose up -d --build
        ├── flask db upgrade（自動執行 DB 遷移）
        └── curl 健康檢查（失敗即中止）
```

EC2 主機資訊與 SSH 私鑰統一存放於 GitHub Secrets，不進版控。

---

## 本地開發

**前置需求：** Docker Desktop

```bash
# 啟動所有服務（Flask + PostgreSQL + Nginx）
docker compose up --build

# 執行資料庫遷移
docker compose exec backend flask db upgrade

# 匯入測試資料
docker compose exec backend flask seed

# API 文件
open http://localhost/apidocs
```

環境變數設定（複製 `.env.example` 並填入實際值）：

```bash
cp .env.example .env
```

---

## 專案亮點

- **雲端架構規劃**：前端、後端、檔案儲存三層分離，各自獨立擴充，符合 AWS 最佳實踐
- **最小權限原則**：IAM Policy 只開放必要的 S3 操作
- **分層架構**：Router / Controller / Service / Repository 四層分離，職責分離
- **Extension 模式**：S3 client 以 Flask extension 管理，啟動時建立一次後 thread-safe 重複使用
- **大檔支援**：boto3 TransferConfig 設定 multipart 上傳，適應大型 CAD 檔案
- **API 文件**：Swagger UI 自動生成，降低前後端溝通成本
- **自動化部署**：GitHub Actions + Docker Compose 實現 push-to-deploy 流程

# SynchroCAD Backend

## 專案簡介
本專案為 Flask + PostgreSQL + Nginx 的後端應用，支援本地與 Docker 部署。

## 目錄結構
- `app/`：Flask 應用程式碼
- `requirements.txt`：Python 依賴
- `Dockerfile`：Flask 容器建構
- `Dockerfile.nginx`：Nginx 容器建構
- `docker-compose.yml`：整合服務
- `nginx.conf`：Nginx 設定

## 啟動方式
### 本地開發
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app wsgi.py run --host=0.0.0.0 --port=5001
```

### Docker 開發
```sh
docker compose up --build
```

## 環境變數
- `DATABASE_URL`：PostgreSQL 連線字串

## 資料庫遷移
請參考 Flask-Migrate 說明。

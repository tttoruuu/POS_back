#!/bin/bash

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# データベースのマイグレーション
alembic upgrade head

# Gunicornでアプリケーションを起動
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT 
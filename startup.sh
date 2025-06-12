#!/bin/bash

# 仮想環境の作成と有効化
python -m venv venv
source antenv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# $PORTがセットされていなければ8000を使う
PORT=${PORT:-8000}

# Gunicornでアプリケーションを起動
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT 
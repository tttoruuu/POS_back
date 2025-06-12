from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# データベース接続URL
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# SQLAlchemyエンジンの作成

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": os.path.join(os.path.dirname(__file__), "BaltimoreCyberTrustRoot.crt.pem")
        }
    }
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# データベースセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# マイグレーション（テーブル作成）を実行
# 以下のコマンドを実行してください：
# ```sh
# alembic upgrade head
# ```
# もしエラーが出た場合は、その内容を教えてください。
# 成功すれば、データベースに必要なテーブルが作成されます！
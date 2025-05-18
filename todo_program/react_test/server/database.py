from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print("資料庫連線字串:", DATABASE_URL)  # 解開註解這行

# 測試連線
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("資料庫連接成功！")
except Exception as e:
    print(f"資料庫連線失敗：{str(e)}")

if DATABASE_URL is None:
    raise ValueError("找不到 DATABASE_URL，請確認 .env 檔存在並且格式正確")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import create_engine
import pandas as pd

try:
    # 連線字串（可改成 os.getenv("DATABASE_URL")）
    engine = create_engine("postgresql://postgres:Postgre@localhost:5432/todolist")
    
    # 指定你要查詢的資料表
    table_name = "Todo_data"  # ← 這邊請換成你實際的表格名稱
    
    # 使用 pandas 執行 SQL 查詢
    df = pd.read_sql(f"SELECT * FROM {table_name};", engine)
    
    print("✅ 資料讀取成功：")
    print(df)
    
except Exception as e:
    import traceback
    print("❌ 發生錯誤：")
    print(traceback.format_exc())



# venv\Scripts\activate
# uvicorn main:app --reload
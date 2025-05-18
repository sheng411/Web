from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class Todo(Base):
    __tablename__ = "todo_data"  # 對應到你的實際 table 名稱

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)  # VARCHAR(100)，nullable 視需求可設 True/False
    time = Column(DateTime, default=datetime.now, nullable=True)
    completed = Column(Boolean, default=False)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/todos", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    try:
        print("收到獲取待辦事項請求")
        todos = crud.get_todos(db)
        print(f"返回 {len(todos)} 個待辦事項：{todos}")
        return todos
    except Exception as e:
        print(f"處理請求時發生錯誤：{str(e)}")
        raise

@app.post("/api/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return {"message": "Deleted"}

@app.put("/api/todos/{todo_id}", response_model=schemas.Todo)
def update_todo_status(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)


# venv\Scripts\activate
# uvicorn main:app --reload
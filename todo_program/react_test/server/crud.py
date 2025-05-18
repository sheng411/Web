from sqlalchemy.orm import Session
import models, schemas

def get_todos(db: Session):
    try:
        todos = db.query(models.Todo).all()
        #print(f"查詢結果：{todos}")
        return todos
    except Exception as e:
        print(f"查詢資料時發生錯誤：{str(e)}")
        raise

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    db.commit()

def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        for key, value in todo_update.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo
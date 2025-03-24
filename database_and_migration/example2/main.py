from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, Users
from pydantic import BaseModel

app = FastAPI()

class UserModal(BaseModel):
    id: int
    name: str
    email: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def get_users(db: Session= Depends(get_db)):
    return db.query(Users).all()

@app.post("/users/")
def create_users(user: UserModal, db: Session = Depends(get_db)):
    new_user=Users( id = user.id, name = user.name, email = user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
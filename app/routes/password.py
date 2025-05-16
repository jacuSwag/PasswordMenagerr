from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.password import PasswordEntry
from schemas.password import PasswordCreate, PasswordOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/passwords", response_model=PasswordOut)
def create_password(entry: PasswordCreate, db: Session = Depends(get_db)):
    db_entry = PasswordEntry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/passwords", response_model=list[PasswordOut])
def get_passwords(db: Session = Depends(get_db)):
    return db.query(PasswordEntry).all()

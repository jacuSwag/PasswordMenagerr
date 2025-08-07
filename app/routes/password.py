from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.password import PasswordEntry
from schemas.password import PasswordCreate, PasswordOut
from security import encrypt_text, decrypt_text  # <-- NOWE

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/passwords", response_model=PasswordOut)
def create_password(entry: PasswordCreate, db: Session = Depends(get_db)):
    # 1) szyfrujemy plaintext
    encrypted = encrypt_text(entry.password)
    db_entry = PasswordEntry(service=entry.service, login=entry.login, password=encrypted)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # 2) na odpowiedzi devowo zwracamy odszyfrowane
    return PasswordOut(
        id=db_entry.id,
        service=db_entry.service,
        login=db_entry.login,
        password=decrypt_text(db_entry.password),
    )

@router.get("/passwords", response_model=list[PasswordOut])
def get_passwords(db: Session = Depends(get_db)):
    items = db.query(PasswordEntry).all()
    # odszyfruj do odpowiedzi (dev)
    result = []
    for it in items:
        try:
            plain = decrypt_text(it.password)
        except Exception:
            plain = "***ERROR***"
        result.append(PasswordOut(
            id=it.id,
            service=it.service,
            login=it.login,
            password=plain
        ))
    return result

@router.delete("/passwords/{password_id}")
def delete_password(password_id: int, db: Session = Depends(get_db)):
    db_password = db.query(PasswordEntry).filter(PasswordEntry.id == password_id).first()
    if db_password is None:
        raise HTTPException(status_code=404, detail="Password not found")
    db.delete(db_password)
    db.commit()
    return {"message": "Password deleted"}

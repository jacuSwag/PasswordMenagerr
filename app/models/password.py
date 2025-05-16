from sqlalchemy import Column, Integer, String
from database import Base

class PasswordEntry(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True)
    login = Column(String)
    password = Column(String)

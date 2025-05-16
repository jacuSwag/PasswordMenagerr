from fastapi import FastAPI
from database import engine, Base
from routes import password

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔒 Obsługa CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # lub ["*"] dla otwartej wersji
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tworzenie tabel w bazie
Base.metadata.create_all(bind=engine)

# Rejestracja routera
app.include_router(password.router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import password, auth

app = FastAPI()

# 🔒 Obsługa CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Otwarte dla zewnętrznych frontendów
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tworzenie tabel w bazie
Base.metadata.create_all(bind=engine)

# Rejestracja routerów
app.include_router(auth.router)
app.include_router(password.router)


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from db import get_db,DATABASE_URL, engine
from sqlalchemy import create_engine
import os
from models import Base
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)
#to create database

Base.metadata.create_all(engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/signup-page")
def signup_page():
    return FileResponse(os.path.join(STATIC_DIR, "signup.html"))

@app.get("/login-page")
def login_page():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
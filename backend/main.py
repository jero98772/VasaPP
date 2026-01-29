from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from apps.auth import router as auth_router
from apps.chats import router as chats_router

# Configure CORS to allow React Native app to connect
app = FastAPI(title="VasaPP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(auth_router)
app.include_router(chats_router)

@app.get("/")
def root():
    return {"status": "ok"}

# app/auth.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login")
def login(username: str, password: str):
    return {
        "message": "logged in",
        "user": username
    }

@router.post("/register")
def register(username: str, password: str):
    return {
        "message": "user registered",
        "user": username
    }

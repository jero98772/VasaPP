# app/chats.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

@router.get("/")
def get_chats():
    return [
        {"id": 1, "name": "General"},
        {"id": 2, "name": "Private"},
    ]

@router.post("/")
def create_chat(name: str):
    return {
        "message": "chat created",
        "name": name
    }

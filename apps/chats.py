# app/chats.py
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def chat(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
    })

@router.get("/list", response_class=HTMLResponse)
def chatlist(request: Request):
    return templates.TemplateResponse("chatlist.html", {
        "request": request,
    })


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


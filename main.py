from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory user store


class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email


users: List[User] = []
next_id = 1


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    print("{0} {1}".format(email, password))
    return "printed"
    # return RedirectResponse(url="/users", status_code=303)


@app.get("/register", response_class=HTMLResponse)
async def get_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def handle_register_form(request: Request, name: str = Form(...), email: str = Form(...)):
    global next_id
    user = User(id=next_id, name=name, email=email)
    users.append(user)
    next_id += 1
    return RedirectResponse(url="/users", status_code=303)


@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return RedirectResponse(url="/users", status_code=303)
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})


@app.post("/edit/{user_id}")
async def edit_user(user_id: int, name: str = Form(...), email: str = Form(...)):
    user = next((u for u in users if u.id == user_id), None)
    if user:
        user.name = name
        user.email = email
    return RedirectResponse(url="/users", status_code=303)


@app.post("/delete/{user_id}")
async def delete_user(user_id: int):
    global users
    users = [u for u in users if u.id != user_id]
    return RedirectResponse(url="/users", status_code=303)

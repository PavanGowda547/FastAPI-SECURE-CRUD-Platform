from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from seed import auth, crud
from seed.database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username)

    if not user or not auth.verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": {}, "error": "Invalid username or password"}
        )

    token = auth.create_access_token({"sub": user.username})

    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return response


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = crud.get_user_by_username(db, username)

    if existing:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username already exists"}
        )

    if len(username) < 3 or len(username) > 20:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username must be 3-20 characters"}
        )

    if len(password) < 8:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Password must be at least 8 characters"}
        )

    hashed = auth.hash_password(password)
    crud.create_user(db, username, hashed)

    return RedirectResponse("/login", status_code=303)


@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import auth, crud, models

router = APIRouter(prefix="/admin")

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(auth.require_admin)
):
    users = db.query(models.User).all()
    notes = crud.get_all_notes(db)
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "users": users,
            "notes": notes,
            "admin": admin
        }
    )


@router.get("/users")
def view_users(
    db: Session = Depends(get_db),
    admin=Depends(auth.require_admin)
):
    users = db.query(models.User).all()
    return JSONResponse([
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ])


@router.post("/users/{user_id}/update")
def update_user(
    user_id: int,
    role: str = Form(...),
    db: Session = Depends(get_db),
    admin=Depends(auth.require_admin)
):
    user = crud.update_user_role(db, user_id, role)
    if not user:
        return {"error": "User not found"}
    return RedirectResponse("/admin/dashboard", status_code=303)


@router.post("/users/{user_id}/delete")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(auth.require_admin)
):
    user = crud.delete_user(db, user_id)
    if not user:
        return {"error": "User not found"}
    return RedirectResponse("/admin/dashboard", status_code=303)


@router.get("/notes")
def view_notes(
    db: Session = Depends(get_db),
    admin=Depends(auth.require_admin)
):
    notes = crud.get_all_notes(db)
    return JSONResponse([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "owner_id": n.owner_id
        }
        for n in notes
    ])


@router.post("/notes/{note_id}/delete")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    admin=Depends(auth.require_admin)
):
    note = crud.delete_note(db, note_id)
    if not note:
        return {"error": "Note not found"}
    return RedirectResponse("/admin/dashboard", status_code=303)
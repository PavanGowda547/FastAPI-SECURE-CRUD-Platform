from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from seed.database import get_db
from seed import auth, crud, schemas

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(
    request: Request,
    q: str = None,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user)
):
    notes = crud.get_notes(db, user.id, q)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "notes": notes,
            "user": user,
            "query": q
        }
    )


@router.post("/notes")
def create_note(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user)
):
    crud.create_note(
        db,
        schemas.NoteCreate(title=title, content=content),
        user.id
    )
    return RedirectResponse("/dashboard", status_code=303)


@router.get("/notes/{note_id}/edit")
def edit_note_page(
    note_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user)
):
    note = crud.get_note(db, note_id)

    if not note or note.owner_id != user.id:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    return templates.TemplateResponse(
        "edit_note.html",
        {"request": request, "note": note}
    )


@router.post("/notes/{note_id}/update")
def update_note(
    note_id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user)
):
    note = crud.get_note(db, note_id)

    if not note or note.owner_id != user.id:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    crud.update_note(db, note_id, title, content)
    return RedirectResponse("/dashboard", status_code=303)


@router.post("/notes/{note_id}/delete")
def delete_note(
    note_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user)
):
    note = crud.get_note(db, note_id)

    if not note or note.owner_id != user.id:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    crud.delete_note(db, note_id)
    return RedirectResponse("/dashboard", status_code=303)
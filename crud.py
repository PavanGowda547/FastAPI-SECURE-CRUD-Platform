from sqlalchemy.orm import Session
import models, schemas


def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.User(
        username=username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()


def update_user_role(db: Session, user_id: int, role: str):
    user = get_user(db, user_id)
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


# NOTES

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session, user_id: int, search: str = None):
    query = db.query(models.Note).filter(
        models.Note.owner_id == user_id
    )
    if search:
        query = query.filter(models.Note.title.contains(search))
    return query.all()


def get_all_notes(db: Session):
    return db.query(models.Note).all()


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(
        models.Note.id == note_id
    ).first()


def update_note(db: Session, note_id: int, title: str, content: str):
    note = get_note(db, note_id)
    if note:
        note.title = title
        note.content = content
        db.commit()
        db.refresh(note)
    return note


def delete_note(db: Session, note_id: int):
    note = get_note(db, note_id)
    if note:
        db.delete(note)
        db.commit()
    return note
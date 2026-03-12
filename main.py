from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import Base, engine, session
import models, auth, os

from routers import auth_router, note_router, admin_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return RedirectResponse("/login")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=404
    )


app.include_router(auth_router.router)
app.include_router(note_router.router)
app.include_router(admin_router.router)


# Auto-create admin
db = session()

admin = db.query(models.User).filter(models.User.username == "admin").first()

if not admin:
    admin_password = os.getenv("ADMIN_PASSWORD", "changeme123")
    admin_user = models.User(
        username="admin",
        hashed_password=auth.hash_password(admin_password),
        role="admin"
    )
    db.add(admin_user)
    db.commit()

db.close()
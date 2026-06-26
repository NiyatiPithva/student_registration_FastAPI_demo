from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal
import models

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Home Page
# -----------------------------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -----------------------------
# Show All Students
# -----------------------------
@app.get("/students/")
def get_all_students(
    request: Request,
    db: Session = Depends(get_db)
):
    students = db.query(models.Student).all()

    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={
            "students": students
        }
    )


# -----------------------------
# Register Page
# -----------------------------
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


# -----------------------------
# Register Student
# -----------------------------
@app.post("/students/")
def create_student(
    name: str = Form(...),
    email: str = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):

    student = models.Student(
        name=name,
        email=email,
        course=course
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return RedirectResponse(
        url="/students/",
        status_code=303
    )


# -----------------------------
# Search Page
# -----------------------------
@app.get("/search")
def search_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={}
    )


# -----------------------------
# Search Student
# -----------------------------
@app.get("/students/search")
def search_student(
    request: Request,
    id: int,
    db: Session = Depends(get_db)
):

    student = db.query(models.Student).filter(
        models.Student.id == id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "student": student
        }
    )


# -----------------------------
# Edit Page
# -----------------------------
@app.get("/students/edit/{id}")
def edit_student(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    student = db.query(models.Student).filter(
        models.Student.id == id
    ).first()

    if student is None:
        return RedirectResponse(
            url="/students/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "student": student
        }
    )


# -----------------------------
# Update Student
# -----------------------------
@app.post("/students/update/{id}")
def update_student(
    id: int,
    name: str = Form(...),
    email: str = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):

    student = db.query(models.Student).filter(
        models.Student.id == id
    ).first()

    if student:
        student.name = name
        student.email = email
        student.course = course

        db.commit()
        db.refresh(student)

    return RedirectResponse(
        url="/students/",
        status_code=303
    )


# -----------------------------
# Delete Student
# -----------------------------
@app.post("/students/delete/{id}")
def delete_student(
    id: int,
    db: Session = Depends(get_db)
):

    student = db.query(models.Student).filter(
        models.Student.id == id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return RedirectResponse(
        url="/students/",
        status_code=303
    )


# -----------------------------
# JSON API (Optional)
# -----------------------------
@app.get("/students/{id}")
def get_student(
    id: int,
    db: Session = Depends(get_db)
):
    return db.query(models.Student).filter(
        models.Student.id == id
    ).first()
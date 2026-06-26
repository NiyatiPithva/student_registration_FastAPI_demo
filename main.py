from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
# Dependency Injection
def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
# create student
@app.post("/students/")
def create_studnets(student : schemas.StudentSchema, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    print("-->>",new_student)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# Get All Students
@app.get("/students/")
def get_all_studnets(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# Get Student by ID
@app.get("/students/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == id).first()


# delete student
@app.delete("/students/{id}")
def delete_student(id: int,db: Session = Depends(get_db)):
    studnet = db.query(models.Student).filter(models.Student.id == id).first()
    print("student deleted..",studnet)
    if studnet:
        db.delete(studnet)
        db.commit()
        return {"deleted student" : studnet}
    return "student not found"

# update
@app.put("/students/{id}")
def update_student(id: int, student: schemas.StudentSchema,db: Session = Depends(get_db)):
    updatedStudent = db.query(models.Student).filter(models.Student.id == id).first()

    if updatedStudent:
        updatedStudent.name = student.name
        updatedStudent.course = student.course
        updatedStudent.email = student.email
        db.commit()
        db.refresh(updatedStudent)
        return updatedStudent
    else:
        return "No student found"
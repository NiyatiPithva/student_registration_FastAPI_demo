from pydantic import BaseModel

class StudentSchema(BaseModel):
    name : str
    email : str
    course : str

    class config:
        orm_mode : True
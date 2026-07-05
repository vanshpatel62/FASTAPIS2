from fastapi import FastAPI,status,HTTPException,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union


app=FastAPI()

Students=[]

class Student(BaseModel):        #Request Model
    id:int
    name:str
    age:int
    password:str


class student_Responce(BaseModel):  #Responce Model
    id:int
    name:str
    age:int



@app.post("/student")
def student_add(stu:Student):
    Students.append(stu)
    return   {"Message":"Student Created",
            "Data":stu}


@app.get("/student",response_model=list[student_Responce])
def student():
    return Students

# @app.get("/student/{stu_id}")
# def find_student(stu_id:int,response_model=student_Responce):
#     for index,x in enumerate(Students):
#         if x.id==stu_id:
#             return Students[index]
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail="Student Not Found"
#         )
#     return {"Error":"Somthing Wrong"}


class User_Not_Found(Exception):
    def __init__(self,id:int):
        self.id=id

@app.exception_handler(User_Not_Found)
def User_not_Found_Handler(request:Request,exc:User_Not_Found):
    return JSONResponse(
        status_code=404,
        content={
            "Status":"Error",
            "Message":f"Student {exc.id} not found"
        }
    )


@app.get("/student/{stu_id}")
def find_student(stu_id:int,response_model=list[student_Responce]):
    for index,x in enumerate(Students):
        if x.id==stu_id:
            return Students[index]
    else:
        raise User_Not_Found(stu_id)
     
    return {"Error":"Somthing Wrong"}
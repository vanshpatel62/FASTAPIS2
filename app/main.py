from fastapi import FastAPI,HTTPException,Depends,Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from app import services,schemas
from app.database import get_db,engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Union
from app.database import engine
from app.models import Base

# change name
# change folder name 
# hvj
# wdsd

app=FastAPI()

# Base.metadata.create_all(bind=engine)



@app.get("/cust",response_model=list[schemas.customer_data])
def get_cust(db:Session=Depends(get_db)):
    return services.get_customre(db)


@app.get("/products",response_model=list[schemas.produsts_data])
def get_produsts(db:Session=Depends(get_db)):
    return services.get_product(db)


@app.get("/orders",response_model=list[schemas.orders_data])
def get_orders(db:Session=Depends(get_db)):
    return services.get_order(db)


@app.get("/")
def home():
    return {"Welcome to FastApi"}


@app.get("/hello")
def hello():
    return {"hello World"}


# About 
@app.get("/About")
def about():
    return {"This is about page"}

# User list
@app.get("/users")
def users_list():
    return {"users":["Mohit","Rohit","Amit"]}

# user page
@app.get("/user/{user_id}")
def user(user_id:int):
    return {"user id" ,user_id}

@app.get("/us")
def get_user(name:str|None = "sir"): # pyright: ignore[reportArgumentType]
    return (f"Welcome {name}")

# @app.get("/products")
# def products(limit : int | None = 10):
#     return (f"sort list products {limit}")

@app.get("/items")
def items(name:str|None=None,price :int|None=0): # type: ignore
    return {
        "Product Name" :name,
        "price ":price
    }

class user_reg(BaseModel):
    name:str
    age:int

@app.post("/registor")
def register(user_reg:dict):
    return{
        "User Creted Sucessfully",
        "User Data",user_reg["name"],user_reg["age"]
    }

Todos_List=[]
# Todo_Id_List=[]
# Todo_Com_List=[]

class Todo_Model(BaseModel):
    id:int
    title:str
    complated:bool

# @app.post("/todos")
# def todos(todo:Todo_Model):
#     Todos_List.append(Todo_Model["title"])
#     Todo_Id_List.append(Todo_Model["id"])
#     Todo_Com_List.append(Todo_Model["complated"])
#     return {"Message" : "Add task in todo list",
#             # "Data",
#             "id":Todo_Id_List[0],
#             "Title":Todos_List[0],
#             "cmplated":Todo_Com_List[0]
#             }

@app.post("/todos/add")   
def create_todos(todo:Todo_Model):
    Todos_List.append(todo)
    return {"Message" : "Add task in todo list",
            "data":todo}


@app.get("/todos/read")
def read_todos():
    return Todos_List

@app.get("/todos/read/{todo_id}")
def read_todos_with_id(todo_id:int=None): # type: ignore
    for x in Todos_List:
        if x.id==todo_id:
            return {"ID ":x.id,
                    "Title":x.title,
                    "complated":x.complated
                    }
    
    return {"Error":"Todo Not Found"}

@app.put("/todos/update/{todo_id}")
def update_todo(todo_id:int=None,updated_todo:Todo_Model |None=None): # type: ignore
    for index,x in enumerate(Todos_List):
        if x.id==todo_id:
            Todos_List[index]=updated_todo
            return {"Message":"Todo Updated sucessfully",
                    "Data":updated_todo}
        
    return {"Error":"TOdoNot Found"}

@app.delete("/todos/delete/{todo_id}")
def delete_tofo(todo_id:int):
    for index,x in enumerate(Todos_List):
        if x.id==todo_id:
            d_data=Todos_List[index]
            Todos_List.pop(index)
            return {"Message":"Todo delete sucessfully",
                    "Deleted Data":d_data}
    return {"Error":"Todo not found"}






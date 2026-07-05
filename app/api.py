from fastapi import FastAPI
from pydantic import BaseModel


app=FastAPI()

users=[]

class User_Model(BaseModel):
    name:str
    age:int

class User_res(BaseModel):
    name:str

@app.post("/user")
def add_user(user:User_Model):
    users.append(user)
    return {"Message":"User Created",
            "Data":user}


@app.get("/user",response_model=list[User_res])
def see_user():
    return users

@app.put("/user/{user_id}")
def update_user(user_id:int,user:User_Model,notify:bool=False):
    if user_id<len(users):
        users[user_id]=user
        return {"Message":"User Updated sucessfully",
                        "notify":notify,
                        "Data":user}

    # if user_id<=len(users):
    #     for index,x in enumerate(users):
    #         if x.id==user_id:
    #             users[index]=up_data
    #             return {"Message":"User Updated sucessfully",
    #                     "notify":notify,
    #                     "Data":up_data}
    return {"Error":"User Not Found"}
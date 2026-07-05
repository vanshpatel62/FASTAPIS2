from fastapi import FastAPI,HTTPException,Request,Depends,Header
from fastapi.responses import Response
from pydantic import BaseModel

app=FastAPI()

def common_logic():
    return{
        "Message":"Welcome,Good Morning"
    }

# def time():
    # return {}

# kajal,meena

@app.get("/home")
def home(Data=Depends(common_logic)):
    return Data


def varifiuser(tokan:str=Header(None),Data=Depends(common_logic)):
    if tokan!="121212222":
        raise HTTPException(
            status_code=401,
            detail="Unautorise User"
        )
    return Data
    
    


@app.get("/lock")
def lock(user=Depends(varifiuser)):
    return {
        "Message":"User Is Varified",
        "user":user
    }
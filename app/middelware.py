from fastapi import FastAPI,HTTPException,Header,Request,Depends
from fastapi.responses import Response
from pydantic import BaseModel
import time

app=FastAPI()

# @app.middleware("http")
# async def  My_Middelwary(request:Request,call_next):
#     print("Request Recived")

#     response=await call_next(request)

#     print("Responce Sent")
#     return response


@app.middleware("http")
async def login(req:Request,call_next):
    start=time.time()
    print()

    res=await call_next(req)

    process_time=time.time()-start

    print(f"Process time {process_time}")

    print(f"path :{req.url.path} | Time {process_time}")

    return res
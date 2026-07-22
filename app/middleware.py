import time
import logging
from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from app.utils.jwt_handler import verify_access_token


logger=logging.getLogger(__name__)

# async def log_requests(request:Request,call_next):
#     start_time=time.time()

#     logger.info("Requect middleware")
#     logger.info(f"Methode : {request.method}")
#     logger.info(f"url : {request.url}")

#     response=await call_next(request)

#     process_time=time.time()-start_time

#     logger.info(f"Status : {response.status_code}")
#     logger.info(f"Time   : {process_time:.4f} seconds")
#     logger.info("Request Finished")

#     return response

# async def delete_middleware(request:Request,call_next):
#     if request.method=="DELETE" and request.url.path.startswith=="/user/delete_user":

#         auth=request.headers.get("Authorization")

#         if auth is None:
#             return JSONResponse(
#                 status_code=401,
#                 content={
#                     "details":"Authorization Header Missing"
#                 }
#             )
        
#         if not auth.startswith("bearer "):
#             return JSONResponse(
#                 status_code=401,
#                 content={
#                     "details":"Invalid Token Format"
#                 }
#             )
        
#         token=auth.split(" ")[1]

#         payload=verify_access_token(token)

#         if payload is None:
#             return JSONResponse(
#                 status_code=401,
#                 content={
#                     "detail": "Invalid or Expired Token"
#                 }
#             )
        
#         if payload["role"] != "admin":
#             return JSONResponse(
#                 status_code=403,
#                 content={
#                     "detail": "Only Admin Can Delete Users"
#                 }
#             )
        
#         responce=await call_next(request)
#         return responce
    

# white_list=["192.168.29.149","127.0.0.1"]
white_list=["127.0.0.1"]


async def ip_whitelist(request:Request,call_next):
    assert request.client is not None

    print(request.client.host)
    client_ip=request.client.host
    user_agent = request.headers.get("User-Agent", "")


    if (client_ip not in white_list) :
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "Your IP address is not allowed."
                }
            )
    # if :
    #     return JSONResponse(
    #         status_code=403,
    #         content={
    #             "detail": "Only Google Chrome browser is allowed."
    #         }
    #     )
    
    responce=await call_next(request)

    return responce

async def browser_check(request: Request, call_next):

    user_agent = request.headers.get("User-Agent", "")
    print(request.headers.get("User-Agent"))
    # Allow only Chrome

    is_google_chrome = (
        "Chrome" in user_agent and
        "Edg" not in user_agent and
        "OPR" not in user_agent and
        "Firefox" not in user_agent
    )
    if not is_google_chrome:
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Only Google Chrome browser is allowed."
            }
        )
    
    response = await call_next(request)
    return response
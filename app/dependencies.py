from fastapi import Depends
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import Models
from app.utils.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login"
)


# def get_current_user(
#     token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
#     print("Received Token:", token)
    
#     payload = verify_access_token(token)

#     print("Payload:", payload)


#     if payload is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or Expired Token"
#         )

#     user_id = payload.get("user_id")

#     user = (
#         db.query(Models.User)
#         .filter(Models.User.user_id == user_id)
#         .first()
#     )

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )
    
#     return payload

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("Received Token:", token)

    payload = verify_access_token(token)
    
    print("Payload:", payload)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

    user_id = payload.get("user_id")

    user = db.query(Models.User).filter(
        Models.User.user_id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return payload

# def get_admin_user()
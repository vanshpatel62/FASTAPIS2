from fastapi import APIRouter,Depends,HTTPException,UploadFile,Form,File
from sqlalchemy.orm import Session

from app import Schemas,Models,Services
from app.database import get_db
import logging
logger=logging.getLogger(__name__)

router=APIRouter(prefix="/document",tags=["Document"])

@router.get("/doc",response_model=list[Schemas.document])
def get_document(db:Session=Depends(get_db)):

    try:
        logger.info("document gat api calling")

        document=Services.get_document(db)
        return document
    except Exception as e:
        logger.exception("          Database error while fetching documents")
        logger.error(f"         Database Error : {e}")
        return {"Message":"Error"}
    
@router.post("/register")
def register(
    user_id: int = Form(...),
    mail: str = Form(...),
    document: UploadFile | None = File(None),
    db: Session = Depends(get_db)):

    data = Schemas.set_registration(user_id=user_id,email=mail)

    return Services.document.set_document(
        db=db,
        data=data,
        document=document
    )
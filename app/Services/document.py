from fastapi import Depends,HTTPException,UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.Models import Document
from app import Schemas
import os
import uuid
from datetime import datetime
from app.utils.encryption import encrypt,decrypt
from app.utils.lookup import encrypt_hash

import logging
logger=logging.getLogger(__name__)

UPLOAD_DIR = "uploads/documents"

def get_document(db:Session):
    logger.info("       Fetching all documents from the database ...")
    documents=db.query(Document).all()

    for document in documents:
        document.email = decrypt(document.email) 

    logger.info("           Successfully fetched %d Documents", len(documents))

    return documents

def set_document(db:Session,data:Schemas.set_registration,document: UploadFile | None):

    # document_ins=data.model_dump()


    # original_email = document_ins["email"]

    # # 1. Encrypt email for secure storage
    # document_ins["email"] = encrypt(original_email)

    # # 2. Generate a random unique lookup ID
    # document_ins["email_lookup"] = str(uuid.uuid4())

    # # 3. Generate deterministic HMAC for searching
    # document_ins["email_lookup"] = encrypt_hash(original_email)

    # # 4. Check duplicate using email_search

    # existing_document = (
    #     db.query(Document)
    #     .filter(
    #         Document.email_lookup == document_ins["email_lookup"]
    #     )
    #     .first()
    # )

    # if existing_document:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Email already exists"
    #     )



    document_ins=data.model_dump()
    original_email = document_ins["email"]
    document_ins['email']=encrypt(original_email)
    document_ins["email_lookup"] = str(uuid.uuid4())
    document_ins['email_lookup']=encrypt_hash(original_email)

    existing_document = (
        db.query(Document).filter(Document.email_lookup == document_ins['email_lookup']).first())

    if existing_document:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )




    document_ins['doc_type']=None
    document_ins['doc_path']=None
    document_ins['save_time']=None

    # if document is not None:
    #     user_folder = os.path.join(UPLOAD_DIR,str(document_ins['user_id']))

    #     original_filename=document.filename

    #     if original_filename is None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Uploaded file must have a filename"
    #         )
    
    # os.makedirs(user_folder,exist_ok=True)

    # # original_filename = document.filename

    # extension = os.path.splitext(original_filename)[1].lower()

    # unique_filename = (f"{uuid.uuid4()}{extension}")

    # file_path = os.path.join(user_folder,unique_filename)
    # with open (file_path,"wb") as file:
    #     content=document.file.read()
    #     file.write(content)

    
    #     document_ins['doc_path'] = os.path.join(
    #         "uploads",
    #         "documents",
    #         str(document_ins['user_id']),
    #         unique_filename
    #     )

    #     document_ins['doc_type'] = extension.replace(".","")

    if document is not None:

        original_filename = document.filename

        if original_filename is None:
            raise HTTPException(
                status_code=400,
                detail="File name is missing"
            )

        extension = os.path.splitext(original_filename)[1].lower()

        # unique_filename = f"{uuid.uuid4()}{extension}"

        user_folder = os.path.join(
            UPLOAD_DIR,
            str(document_ins["user_id"]))

        os.makedirs(
            user_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            user_folder,
            original_filename
        )

        # Save uploaded file
        with open(file_path, "wb") as file:
            content = document.file.read()
            file.write(content)

        document_ins["doc_path"] = os.path.join(
            "uploads",
            "documents",
            str(document_ins["user_id"]),
            original_filename
        )

        document_ins["doc_type"] = extension.replace(
            ".",
            ""
        )

        document_ins['save_time']=datetime.now()
    
    customer_ins = Document(**document_ins)

    db.add(customer_ins)
    db.commit()
    db.refresh(customer_ins)

    return customer_ins
import bcrypt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.database.connection import db
from app.database.schema import User
from app.models import user
from app.common.response import response

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(user: user.UserRegister, session: Session = Depends(db.session)):
    check = session.query(exists().where(User.email == user.email)).scalar()

    if check:
        raise HTTPException(409, "Email is already exists")

    if user.password != user.password_confirm:
        raise HTTPException(400, "Password and Password Confirm must be same")

    user.password = bcrypt.hashpw(str(user.password).encode("utf-8"), bcrypt.gensalt())
    session.add(User(email=user.email, password=user.password, name=user.name))
    session.commit()
    del user.password_confirm

    return response(201, "Created", user)

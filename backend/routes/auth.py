# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from models.users import User
# from schemas.user import UserCreate
# from auth.utils import hash_password, verify_password, create_access_token

# router = APIRouter(prefix="/auth", tags=["Auth"])


# @router.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.username == user.username).first()

#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")

#     new_user = User(
#         username=user.username,
#         password=hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User registered"}


# @router.post("/login")
# def login(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()

#     if not db_user or not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"user_id": db_user.id})

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.users import User
from schemas.user import UserCreate

from auth.utils import (
    hash_password,
    verify_password,
    create_access_token
)

# =========================================
# Router
# =========================================
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# =========================================
# Register User
# =========================================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "success",
        "message": "User registered successfully"
    }


# =========================================
# Login User
# =========================================
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({
        "user_id": db_user.id
    })

    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer"
    }
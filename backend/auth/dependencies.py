import logging
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from auth.utils import SECRET_KEY, ALGORITHM

logger = logging.getLogger(__name__)


def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        logger.error("No Authorization header found")
        logger.error(f"All headers: {dict(request.headers)}")
        raise HTTPException(status_code=401, detail="Not authenticated")

    logger.info(f"Auth header received: {auth_header[:50]}...")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.error(f"Invalid header format: {auth_header[:50]}...")
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = parts[1]
    logger.info(f"Token extracted: {token[:30]}...")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        logger.info(f"Token decoded successfully, user_id: {user_id}")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User found: {user.username}")
    return user

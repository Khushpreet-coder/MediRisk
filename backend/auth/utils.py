
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

# ✅ LOAD ENV VARIABLES
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # default safe
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ✅ PASSWORD HASHING CONTEXT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔐 HASH PASSWORD
def hash_password(password: str):
    return pwd_context.hash(password)


# 🔍 VERIFY PASSWORD
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# 🎟️ CREATE JWT TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(100), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)

#     reports = relationship("Report", back_populates="user", cascade="all, delete")

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(100), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)

#     # Relationship with reports
#     reports = relationship("Report", back_populates="user")

from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    
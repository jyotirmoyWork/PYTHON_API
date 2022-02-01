from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship




class Post_Two(Base):
    __tablename__ = "POSTS"

    ID = Column(Integer, primary_key=True, nullable=False)
    TITLE = Column(String, nullable=False)
    CONTENT = Column(String, nullable=False)
    PUBLISHED = Column(Boolean, server_default='True',nullable=False)
    CREATED_AT = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)
    OWNER_ID = Column(Integer, ForeignKey("USERS.ID", ondelete="CASCADE"), nullable=False)

    OWNER = relationship("User")



class User(Base):
    __tablename__ = "USERS"

    ID = Column(Integer, primary_key=True, nullable=False)
    EMAIL = Column(String, nullable=False, unique=True)
    PASSWORD = Column(String, nullable=False)
    CREATED_AT = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)
    PHONE_NO = Column(String)


class Votes(Base):
    __tablename__ = "VOTES"

    USER_ID = Column(Integer, ForeignKey("USERS.ID", ondelete="CASCADE"), primary_key=True)
    POST_ID = Column(Integer, ForeignKey("POSTS.ID", ondelete="CASCADE"), primary_key=True)
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import ARRAY

from DataBase.Models import Base


class User(Base):
    __tablename__ = "users"

    chat_id = Column(Integer, primary_key=True)
    chains = relationship("Chains", back_populates="user")  # Много связок
    posts = relationship("Post")


class Chains(Base):
    __tablename__ = "chains"

    chain_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("users.chat_id"))  # Внешний ключ на User.chat_id
    target_channel = Column(String)
    source_urls = Column(ARRAY(JSON))
    parsing_type = Column(String)
    parsing_time = Column(ARRAY(String))
    additional_text = Column(String)
    active_due_date = Column(DateTime, default=func.now(), nullable=True)
    posts = relationship("Post")

    user = relationship("User", back_populates="chains")  # Отношение к юзеру


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    chain_id = Column(Integer, ForeignKey("chains.chain_id"))
    user_chat_id = Column(Integer, ForeignKey("users.chat_id"))
    post_text = Column(String)
    post_date = Column(DateTime, default=func.now())
    media_files = Column(ARRAY(String))
    is_sent = Column(Boolean, default=False)

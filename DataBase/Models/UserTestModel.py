import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from DataBase.Models import Base


class UserTest(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(Integer(), nullable=False, unique=True)
    username = Column(String(), nullable=True)
    balance = Column(Float(), nullable=False, default=0)

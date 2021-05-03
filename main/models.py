from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from transitions import Machine


from .database import Base

from .machine import UserMachineMixin
class User(Base, UserMachineMixin):

    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_state = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
class Item(Base):

    __tablename__ = "items"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

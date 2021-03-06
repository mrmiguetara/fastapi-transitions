from typing import List, Optional


from pydantic import BaseModel



class ItemBase(BaseModel):

    title: str

    description: Optional[str] = None




class ItemCreate(ItemBase):

    pass



class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):

    email: str




class UserCreate(UserBase):

    password: str
    user_state: str



class User(UserBase):
    id: int
    is_active: bool
    user_state: str
    items: List[Item] = []

    class Config:
        orm_mode = True

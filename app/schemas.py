from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# --- COMMENTS ---

class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    content: str
    reply_to: Optional[int] = None

class CommentOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    timestamp: datetime
    reply_to: Optional[int] = None
    replies: Optional[List['CommentOut']] = []
    class Config:
        orm_mode = True

CommentOut.update_forward_refs()

# --- LIKES & SAVES ---

class LikeCreate(BaseModel):
    user_id: int

class SaveCreate(BaseModel):
    user_id: int

# --- CATEGORY ---

class CategoryCreate(BaseModel):
    title: str

class CategoryOut(BaseModel):
    id: int
    title: str
    class Config:
        orm_mode = True

class PostCategoryAssign(BaseModel):
    post_id: int
    category_ids: List[int]

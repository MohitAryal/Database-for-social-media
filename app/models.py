from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, DateTime, Table, UniqueConstraint
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# Association table for Post <-> Category (Many-to-Many)
post_category = Table(
    "post_category",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)

class User(AsyncAttrs, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String())
    is_verified = Column(Integer, default=0)

    posts = relationship("Post", back_populates="author", cascade="all, delete")
    comments = relationship("Comment", back_populates="author", cascade="all, delete")
    post_likes = relationship("PostLike", back_populates="user", cascade="all, delete")
    post_saves = relationship("PostSave", back_populates="user", cascade="all, delete")
    comment_likes = relationship("CommentLike", back_populates="user", cascade="all, delete")

class Post(AsyncAttrs, Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete")
    saves = relationship("PostSave", back_populates="post", cascade="all, delete")
    categories = relationship("Category", secondary=post_category, back_populates="posts", lazy="selectin")

class Comment(AsyncAttrs, Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reply_to = Column(Integer, ForeignKey("comments.id"), nullable=True)

    post = relationship("Post", back_populates="comments", lazy="selectin")
    author = relationship("User", back_populates="comments", lazy="selectin")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete", lazy="selectin")
    parent = relationship("Comment", remote_side=[id], back_populates="replies", lazy="selectin")
    likes = relationship("CommentLike", back_populates="comment", cascade="all, delete", lazy="selectin")

class CommentLike(AsyncAttrs, Base):
    __tablename__ = "comment_likes"
    __table_args__ = (UniqueConstraint("comment_id", "user_id", name="unique_comment_like"),)

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    comment = relationship("Comment", back_populates="likes")
    user = relationship("User", back_populates="comment_likes")

class PostLike(AsyncAttrs, Base):
    __tablename__ = "post_likes"
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_post_like"),)

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="post_likes")

class PostSave(AsyncAttrs, Base):
    __tablename__ = "post_saves"
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_post_save"),)

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="saves")
    user = relationship("User", back_populates="post_saves")

class Category(AsyncAttrs, Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(15), unique=True)

    posts = relationship("Post", secondary=post_category, back_populates="categories", lazy="selectin")

import os
import sys
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    UserId = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    followers = relationship("Follower", foreign_keys='Follower.followed_id', cascade="all, delete-orphan")
    following = relationship("Follower", foreign_keys='Follower.follower_id', cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = 'posts'

    PostId = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.UserId', ondelete='CASCADE'), nullable=False)
    image_url = Column(String, nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = 'comments'

    CommentId = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.PostId', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.UserId', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Follower(Base):
    __tablename__ = 'followers'
    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)

    follower_id = Column(Integer, ForeignKey('users.UserId', ondelete='CASCADE'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.UserId', ondelete='CASCADE'), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

class Like(Base):
    __tablename__ = 'likes'
    __table_args__ = (UniqueConstraint('PostID', 'UserID', name='_post_user_uc'),)

    LikeId = Column(Integer, primary_key=True)
    PostID = Column(Integer, ForeignKey('posts.PostId', ondelete='CASCADE'), nullable=False)
    UserID = Column(Integer, ForeignKey('users.UserId', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e

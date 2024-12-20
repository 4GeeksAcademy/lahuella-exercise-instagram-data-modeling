import os
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    followers = relationship("Follower", foreign_keys="[lambda: Follower.followed_id]")
    following = relationship("Follower", foreign_keys="[lambda: Follower.follower_id]")

class Post(Base):
    __tablename__ = 'posts'

    PostId = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    image_url = Column(String, nullable=False)
    caption = Column(Text, nullable=True)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'

    CommentId = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.PostId'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    content = Column(Text, nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Follower(Base):
    __tablename__ = 'followers'

    follower_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

class Like(Base):
    __tablename__ = 'likes'

    LikeId = Column(Integer, primary_key=True)
    PostID = Column(Integer, ForeignKey('posts.PostId'), nullable=False)
    UserID = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")



## Draw from SQLAlchemy base
try:
    engine = create_engine('sqlite:///:memory:')  # Usa tu URL de base de datos
    Base.metadata.create_all(engine)
    render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
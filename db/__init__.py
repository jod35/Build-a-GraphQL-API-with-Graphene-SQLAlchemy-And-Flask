from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship,sessionmaker,scoped_session
import os


BASE_DIR=os.path.dirname(os.path.realpath(__file__))

connection_str= "sqlite:///" + os.path.join(BASE_DIR,'posts.db')


Base=declarative_base()



engine=create_engine(connection_str,echo=True)


session=scoped_session(
    sessionmaker(bind=engine)
)

Base.query = session.query_property()


"""
table users:
id - primary key
username : str
email


table posts:
id - primary key
title:str
content:text
user_id -> users.id

"""


class User(Base):
    __tablename__="users"
    id=Column(Integer(),primary_key=True)
    username=Column(String(45),nullable=False)
    email=Column(String(80),nullable=False)
    posts=relationship("Post",backref="author")


    def __repr__(self):
        return f"<User {self.username}>"


class Post(Base):
    __tablename__="posts"
    id=Column(Integer(),primary_key=True)
    title=Column(String(),nullable=False)
    content=Column(Text(),nullable=False)
    user_id=Column(Integer(),ForeignKey("users.id"))

    def __repr__(self):
        return f"<User {self.title}>"



from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey, Table, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er
import enum

db = SQLAlchemy()

likes = Table("likes", db.Model.metadata,
Column("user.id", Integer, ForeignKey("user.id"), primary_key=True),
Column("post.id", Integer, ForeignKey("post.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    #Relaciones
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
    liked_posts: Mapped[list["Post"]] = relationship("Post", secondary=likes, back_populates="linking_users")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
#Modelo Post
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(350), unique=True, nullable=True)
    #Relaciones
    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    linking_users: Mapped[list["User"]] = relationship("User", secondary=likes, back_populates="liked_posts")


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    post_id: Mapped[str] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)
    #Relaciones
    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class TypeEnum(enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    type: Mapped[enum.Enum] = mapped_column(Enum(TypeEnum), nullable=False)
    post_id: Mapped[str] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)
    #Relaciones
    post: Mapped["Post"] = relationship("Post", back_populates="comments")



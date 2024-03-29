from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    user = relationship("User")  # fetches details of user


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Like(Base):
    __tablename__ = "like"

    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("post.id", ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime


Base = declarative_base()

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    img = Column(String)
    publish_dt = Column(DateTime, nullable=False)
    writer_id = Column(Integer, ForeignKey("writer.id"))
    writer = relationship("Writer")
    comments = relationship("Comment")
    tags = relationship("Tag", secondary=tag_post)


class Writer(Base):
    __tablename__ = "writer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    posts = relationship(Post)


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    posts = relationship(Post, secondary=tag_post)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    posts = relationship(Post)
    writers = relationship(Writer)
    post_id = Column(Integer, ForeignKey(Post.id))
    writer_id = Column(Integer, ForeignKey(Writer.id))

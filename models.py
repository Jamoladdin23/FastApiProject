from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine

Base.metadata.create_all(bind=engine)

class BookModel(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    published_year = Column(Integer)
    price = Column(Integer, default=99)

    author = relationship("AuthorModel", back_populates="books")


class AuthorModel(Base):

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

    author = relationship("BookModel", back_populates="authors")

# this for create users
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

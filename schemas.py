from pydantic import BaseModel


class BaseBook(BaseModel):
    title: str
    description: str | None = None
    published_year: int
    price: int
    authhor_id: int


class CreateBook(BaseBook):
    name: str
    price: int
    author_id: int


class Book(BaseBook):
    id: int

    class Config:
        orm_mode = True  # chto bi v orm mojno bilo rabotat s nim


class BaseAuthor(BaseModel):
    first_name: str
    last_name: str


class CreateAuthor(BaseAuthor):
    id: int


class Author(BaseAuthor):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

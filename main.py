from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated

from sqlalchemy.orm import Session
from starlette import status

from .import models, schemas
from app.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



def get_db():  # this func can write s pomowyu conext managera
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_hash_password(password: str):
    return "fakehashed" + password
class UserInDB(models.User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    db = SessionLocal()
    user = get_user(db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db = SessionLocal()
    user_dict = db.query(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user



@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int):
    db = SessionLocal()
    author = db.query(models.AuthorModel).filter(models.AuthorModel.id == author_id).first()
    db.close()
    if author in None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.CreateAuthor):
    db = SessionLocal()
    author_model = models.AuthorModel(**author.dict())
    db.add(author_model)
    db.commit()
    db.refresh(author_model)
    db.close()
    return author_model


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.CreateAuthor):
    db = SessionLocal()
    author_model = db.query(models.AuthorModel).filter(models.AuthorModel.id == author_id).first()
    if author_model is None:
        db.close()
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict().items():
        setattr(author_model, key, value)
    db.commit()
    db.close()
    return author_model


@app.delete("/authors/{author_id}")
def delete_author(author_id: int):
    db = SessionLocal()
    author_model = db.query(models.AuthorModel).filter(models.AuthorModel.id == author_id).first()
    if author_model is None:
        db.close()
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author_model)
    db.commit()
    db.close()
    return {"message": "Author deleted successfully"}


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int):
    db = SessionLocal()
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    db.close()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.CreateBook):
    db = SessionLocal()
    book_model = models.BookModel(**book.dict())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    db.close()
    return book_model


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.CreateBook):
    db = SessionLocal()
    book_model = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if book_model is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(book_model, key, value)
    db.commit()
    db.close()
    return book_model


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()
    book_model = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if book_model is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book_model)
    db.commit()
    db.close()
    return {"message": "Book deleted successfully"}

from sqlalchemy.orm import Session

from .models import BookModel, AuthorModel, User# tak kak budem work s etim model need to import
from .schemas import CreateBook, CreateAuthor, UserCreate

def book_list(db: Session):
    return db.query(BookModel).all()

def book_create(db: Session, book: CreateBook):
    db_book = BookModel(**book.model_dump())# delaem dump wob danni ne bili obj a bili slovnikom
    db.add(db_book)# dodayem v bd..
    db.commit()# commitim, posilaem wob vipolnilisand get result, id for db book
    db.refresh(db_book)
    return db_book

def book_retrieve(db: Session, book_id: int):
    return db.query(BookModel).filter(BookModel.id == book_id).first()


def author_list(db: Session):
    return db.query(AuthorModel).all()

def author_create(db: Session, author: CreateAuthor):
    db_author = AuthorModel(**author.model_dump())# delaem dump wob danni ne bili obj a bili slovnikom
    db.add(db_author)# dodayem v bd..
    db.commit()# commitim, posilaem wob vipolnilisand get result, id for db book
    db.refresh(db_author)
    return db_author

def author_retrieve(db: Session, author_id: int):
    return db.query(AuthorModel).filter(AuthorModel.id == author_id).first()



def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


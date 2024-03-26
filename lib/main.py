from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine("sqlite:///book.db")
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    isbn = Column(Integer())
    publication_date = Column(String())
    description = Column(String())
    publisher = Column(String())
    language = Column(String())
    pages_count = Column(Integer())
    rating = Column(Integer())

    genre_id = Column(Integer(), ForeignKey('genres.id'))
    genre = relationship("Genre", back_populates="books")

    author_id = Column(Integer(), ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f'Book(id={self.id},' + \
               f'title={self.title},' + \
               f'author={self.author},' + \
               f'isbn={self.isbn},' + \
               f'publication_date={self.publication_date},' + \
               f'description={self.description},' + \
               f'publisher={self.publisher},' + \
               f'language={self.language},' + \
               f'pages_count={self.pages_count},' + \
               f'rating={self.rating})'

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    best_seller = Column(String())
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f'Author(id={self.id},' + \
               f'name={self.name},' + \
               f'best_seller={self.best_seller})'

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return f'Genre(id={self.id},' + \
               f'name={self.name})'

Base.metadata.create_all(engine)

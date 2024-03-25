import click
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from main import Base, Book, Author, Genre

# Define the SQLite database URL
DB_URL = "sqlite:///book.db"

# Create the SQLAlchemy engine and session
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables if they don't exist
Base.metadata.create_all(engine)


@click.group()
def cli():
    """
    Command-line interface for managing books.
    """
    pass


@cli.command()
@click.argument("title")
@click.argument("author")
@click.argument("genre")
def add(title, author, genre):
    """
    Add a new book to the database.
    """
    # Check if the author already exists
    author_exists = session.query(exists().where(Author.name == author)).scalar()

    if not author_exists:
        # Create a new author if not found in the database
        new_author = Author(name=author)
        session.add(new_author)
        session.commit()

    # Check if the genre exists
    genre_obj = session.query(Genre).filter_by(name=genre).first()

    if not genre_obj:
        click.echo(f"Genre '{genre}' not found.")
        return

    # Add the book to the database
    new_book = Book(title=title, author_name=author, genre=genre_obj)
    session.add(new_book)
    session.commit()
    click.echo(f"Added book: {title} by {author} in {genre}")


@cli.command()
@click.argument("title")
def delete(title):
    """
    Delete a book from the database.
    """
    book = session.query(Book).filter_by(title=title).first()

    if book:
        session.delete(book)
        session.commit()
        click.echo(f"Deleted book: {title}")
    else:
        click.echo(f"Book '{title}' not found.")


@cli.command()
@click.argument("search_term", nargs=-1)
def search(search_term):
    """
    Search for books by title or author.
    """
    search_query = ' '.join(search_term)

    found_books = (
        session.query(Book)
        .join(Author)
        .filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Author.name.ilike(f"%{search_query}%"))
        )
        .all()
    )

    if found_books:
        click.echo(f"Books related to '{search_query}':")
        for book in found_books:
            click.echo(f"- {book.title} by {book.author_name}")
    else:
        click.echo(f"No books found related to '{search_query}'")


if __name__ == "__main__":
    cli()

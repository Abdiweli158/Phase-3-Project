import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Book, Author, Genre

engine = create_engine("sqlite:///book.db")
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("title")
@click.argument("author")
@click.argument("genre")
def add(title, author, genre):
    """
    Add a new book.
    """
    author_obj = session.query(Author).filter_by(name=author).first()
    genre_obj = session.query(Genre).filter_by(name=genre).first()

    if not author_obj:
        # Create a new author if not found in the database
        new_author = Author(name=author)
        session.add(new_author)
        session.commit()
        author_obj = new_author

    if not genre_obj:
        click.echo(f"Genre '{genre}' not found.")
        return

    new_book = Book(title=title, author=author_obj, genre=genre_obj)
    session.add(new_book)
    session.commit()
    click.echo(f"Added book: {title} by {author} in {genre}")


@cli.command()
@click.argument("title")
def delete(title):
    """
    Delete a book.
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
            click.echo(f"- {book.title} by {book.author.name}")
    else:
        click.echo(f"No books found related to '{search_query}'")

if __name__ == "__main__":
    cli()

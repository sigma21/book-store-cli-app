import typer
import database
from rich.console import Console
from rich.table import Table
from rich import print
from typing import Optional

console = Console()

app = typer.Typer()

@app.command("start")
def start():
    typer.secho(f"Welcome to Library CLI!\n\nYou can execute command '--help' to see the possible commands", fg=typer.colors.GREEN)
    database.connect()

@app.command("sign_up")
def sign_up(username: str):
    typer.echo(f"Nice that you are signing up!")
    usernames = database.get_usernames()
    while username in usernames:
        typer.secho(f"This username already exists!", fg=typer.colors.RED)
        username = input("Please enter another username: ")
    database.add_user(username)
    typer.secho(f"Successfully signed up!", fg=typer.colors.GREEN)

@app.command("add_book")
def add_book():
    typer.secho(f"Please enter the required book info to add!", fg=typer.colors.BLUE)
    name = input("Name: ")
    author = input("Author: ")
    page = int(input("# Pages: "))
    genre = input("Genre: ")
    database.add_book(name, author, page, genre)
    typer.secho(f"Successfully added book!", fg=typer.colors.GREEN)

@app.command("search_by_name")
def search_by_name(name: str):
    books = database.search_book_by_name(name)
    display_book_table(books)

@app.command("search_by_author")
def search_by_author(author: str):
    books = database.search_book_by_author(author)
    display_book_table(books)

@app.command("recently_added")
def recently_added(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.get_recent_books()
    else:
        books = database.get_recent_books_by_genre(genre)
    display_book_table(books)
    
@app.command("most_read_books")
def most_read_books(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.most_read_books()
    else:
        books = database.most_read_books_by_genre(genre)
    display_book_table_with_count(books)

@app.command("most_favorite_books")
def most_favorite_books(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.most_favorite()
    else:
        books = database.most_favorite_by_genre(genre)
    display_book_table_with_count(books)

@app.command("most_read_genres")
def most_read_genres():
    genres = database.most_read_genres()
    display_most_read_count(genres, "Genre")

@app.command("most_read_authors")
def most_read_authors():
    authors = database.most_read_authors()
    display_most_read_count(authors, "Author")

@app.command("borrow_book")
def borrow_book(book_id: int, username: str):
    available = database.is_book_available(book_id)
    if available:
        database.borrow_book(username, book_id)
        print(f"\nYou borrowed book {book_id}!\n")
    else:
        print(f"\nSorry, book {book_id} is not available! Try again later.\n")

@app.command("return_book")
def return_book(book_id: int, username: str):
    borrowed = database.is_borrowed(username, book_id)
    if not borrowed:
        print(f"\nSorry, you didn't borrow book {book_id}.\n")
    else:
        database.return_book(username, book_id)
        print(f"\nYou returned book {book_id}!\n")

@app.command("mark_read")
def mark_read(book_id: int, username: str):
    database.mark_status(username, book_id, 'read')
    print("\nYou marked book", str(book_id), "as read!\n")

@app.command("mark_reading")
def mark_reading(book_id: int, username: str):
    database.mark_status(username, book_id, 'reading')
    print("\nYou marked book", str(book_id), "as reading!\n")

@app.command("mark_will_read")
def mark_will_read(book_id: int, username: str):
    database.mark_status(username, book_id, 'will_read')
    print("\nYou marked book", str(book_id), "as will read!\n")

@app.command("fav_book")
def fav_book(book_id: int, username: str):
    database.add_fav(username, book_id)
    print("\nYou added book", str(book_id), "to your favorites!\n")

@app.command("my_books")
def my_books(username: str):
    read_books = database.get_books_with_status(username, "read")
    typer.echo(f"BOOKS YOU READ")
    display_book_table(read_books)
    reading_books = database.get_books_with_status(username, "reading")
    typer.echo(f"BOOKS YOU ARE READING")
    display_book_table(reading_books)
    will_read_books = database.get_books_with_status(username, "will_read")
    typer.echo(f"BOOKS YOU WILL READ")
    display_book_table(will_read_books)
    fav_books = database.get_fav_books(username)
    typer.echo(f"YOUR FAVORITE BOOKS")
    display_book_table(fav_books)

@app.command("statistics")
def statistics(username: str):
    books, authors, genres, total_pages = database.get_statistics(username)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Statistic", style="dim", min_width=10, justify=True)
    table.add_column("Number", style="dim", min_width=10, justify=True)

    table.add_row('Books you read', str(books))
    table.add_row('Authors you read', str(authors))
    table.add_row('Genres you read', str(genres))
    table.add_row('Total pages you read', str(total_pages))

    console.print(table)

def display_book_table(books):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("# Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)

    for idx, book in enumerate(books, start=1):
        availability = False
        if book[5] <= book[6]:
            availability = True
        table.add_row(str(idx), str(book[0]), book[1], book[2], str(book[3]), book[4], str(availability))

    console.print(table)

def display_book_table_with_count(books):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)

    for idx, book in enumerate(books, start=1):
        table.add_row(str(idx), str(book[0][0]), book[0][1], book[0][2], book[0][4], str(book[1]))

    console.print(table)

def display_most_read_count(most_read, type):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column(type, style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)

    for idx, item in enumerate(most_read, start=1):
        table.add_row(str(idx), item[0], str(item[1]))

    console.print(table)

if __name__ == "__main__":
    app()

import typer
from database import connect, get_users, add_user, get_books, add_book, search_book
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()

@app.command("start")
def start():
    typer.echo(f"Welcome to Library CLI!")
    typer.echo(f"You can execute command 'help' to see the possible commands")
    connect()

@app.command("help")
def help():
    typer.echo(f"Here are the possible commands:")
    for command in app.registered_commands:
        print("-", command.name)

@app.command("signup")
def signup():
    typer.echo(f"Nice that you are signing up!")
    username = input("Please enter your username: ")
    users = get_users()
    while username in users:
        print("This username already exists!")
        username = input("Please enter another username: ")
    add_user(username)
    print("Successfully signed up!")

@app.command("signin")
def signin():
    typer.echo(f"Let's sign in!")
    name = input("Please enter your username: ")
    users = get_users()
    if name in users:
        print("This username doesn't exist. Please sign up!")
        return

@app.command("addbook")
def addbook():
    typer.echo(f"Please enter the required book info to add!")
    name = input("Book name: ")
    author = input("Author: ")
    page = input("Number of the pages: ")
    genre = input("Genre of the book: ")
    add_book(name, author, page, genre)
    typer.echo(f"Book successfully added!")

@app.command("books")
def books():
    books = get_books()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)

    for idx, book in enumerate(books, start=1):
        table.add_row(str(idx), str(book[0]), book[1], book[2], str(book[3]), book[4])

    console.print(table)

@app.command("searchbook")
def searchbook():
    name = input("Please enter the name of the book you want to search: ")
    books = search_book(name)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)

    for idx, book in enumerate(books, start=1):
        table.add_row(str(idx), str(book[0]), book[1], book[2], str(book[3]), book[4])

    console.print(table)
    
if __name__ == "__main__":
    app()

from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from urllib.parse import unquote

from typing import List


import uvicorn
import sqlite3


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

templates = Jinja2Templates(directory="templates/")


app.mount("/static", StaticFiles(directory="static"), name="static")

# Connect user.db
user = sqlite3.connect('users.db')
user_cursor = user.cursor()

user_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

user.commit()


# Random book
def random_book():
    conn = sqlite3.connect("lib_book.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books ORDER BY RANDOM() LIMIT 1")

    book_id = cursor.fetchone()[0]

    conn.close()

    return book_id


# Search book
def search_book(name: str) -> List[str]:
    conn = sqlite3.connect('lib_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE name_book LIKE ?",
                   ('%' + name + '%',))

    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    conn = sqlite3.connect('lib_book.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    img_books = cursor.fetchmany(99)

    random_b = random_book()  # <-- book id

    conn.close()

    # get username
    session = request.session
    username = session.get("username")

    return templates.TemplateResponse("index.html", {"request": request, "img_books": img_books, "random_book": random_b, "username": username})


@app.get("/b/{item_id}", response_class=HTMLResponse)
async def book_info(request: Request, item_id: int):
    conn = sqlite3.connect('lib_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (item_id,))

    book = cursor.fetchall()

    random_b = random_book()  # <-- book id

    # get username
    session = request.session
    username = session.get("username")

    return templates.TemplateResponse("book_info.html", {"request": request, "item_id": item_id, "book": book, "random_book": random_b, "username": username})


@app.get("/search", response_class=HTMLResponse)
async def search_b(request: Request, name: str = None):
    try:
        random_b = random_book()  # <-- book id

        params = dict(request.query_params)
        name = unquote(params.get('name', ''))
        items = search_book(name.capitalize())

        books = []
        for item in items:
            conn = sqlite3.connect('lib_book.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (str(item),))
            book = cursor.fetchone()
            books.append(book)

        # get username
        session = request.session
        username = session.get("username")

        return templates.TemplateResponse("search.html", {"request": request, "random_book": random_b, "books": books, "username": username})

    except AssertionError as e:
        # get username
        session = request.session
        username = session.get("username")

        return templates.TemplateResponse("search.html", {"request": request, "random_book": random_b, "e": e, "username": username})


# Login
@app.get("/enter_page", response_class=HTMLResponse)
async def enter_page(request: Request):
    return templates.TemplateResponse("enter_page.html", {"request": request})


@app.post("/login")
async def login(response: Response, request: Request, username: str = Form(...), password: str = Form(...)):
    user_cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user_acc = user_cursor.fetchone()
    if user_acc:
        response.set_cookie(key="username", value=username)
        session = request.session
        session["username"] = username
        return RedirectResponse(url="/", status_code=302)
    else:
        return {"message": "Invalid username or password"}


# Register
@app.get("/register_page", response_class=HTMLResponse)
async def enter(request: Request):
    return templates.TemplateResponse("register_page.html", {"request": request})


@app.post("/create/", response_class=HTMLResponse)
async def create(request: Request, username: str = Form(...), password: str = Form(...)):
    user_cursor.execute("SELECT * FROM users WHERE username= ?", (username,))
    existing_user = user_cursor.fetchone()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    user_cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    user.commit()

    return RedirectResponse(url="/", status_code=302)

# Logout


@app.get("/logout", response_class=RedirectResponse)
async def logout(request: Request):
    session = request.session
    if "username" in session:
        del session["username"]
    return RedirectResponse(url="/", status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

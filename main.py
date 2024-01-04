from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from urllib.parse import unquote

from typing import List

import uvicorn
import sqlite3


app = FastAPI()
templates = Jinja2Templates(directory="templates/")


app.mount("/static", StaticFiles(directory="static"), name="static")


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

    return templates.TemplateResponse("index.html", {"request": request, "img_books": img_books, "random_book": random_b})


@app.get("/b/{item_id}", response_class=HTMLResponse)
async def book_info(request: Request, item_id: int):
    conn = sqlite3.connect('lib_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (item_id,))

    book = cursor.fetchall()

    random_b = random_book()  # <-- book id

    return templates.TemplateResponse("book_info.html", {"request": request, "item_id": item_id, "book": book, "random_book": random_b})


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

        return templates.TemplateResponse("search.html", {"request": request, "random_book": random_b, "books": books})

    except AssertionError as e:
        return templates.TemplateResponse("search.html", {"request": request, "random_book": random_b, "e": e})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

import requests
import sqlite3

from bs4 import BeautifulSoup

# Get books link


def scrape_book():
    link = f"https://flibusta.is/stat/b"
    counter = 0
    clear_list = []
    while True:
        r = requests.get(link)

        soup = BeautifulSoup(r.text, "lxml", multi_valued_attributes=None)

        get_main = soup.find("div", {"id": "main-wrapper"})
        find_list = get_main.find("ul")
        get_list = find_list.find_all("li")

        for name in get_list:
            try:
                result = name.find_all("a")
                link_book = f"https://flibusta.is{result[1].get('href')}"
                clear_list.append(link_book)

            except:
                continue

        counter += 1

        link = f"https://flibusta.is/stat/b?page={counter}"

        if counter == 100:
            break

    return clear_list

# scrape data about book


def scrape_data_book(book_list):
    conn = sqlite3.connect("lib_book.db")
    cursor = conn.execute('''
            CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_book TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre_book TEXT NOT NULL,
                    download_link TEXT NOT NULL,
                    discription TEXT NOT NULL,
                    img TEXT NOT NULL
    )''')

    cursor.execute("DROP TABLE IF EXISTS users")

    x = 0
    for book in book_list:
        try:
            r = requests.get(book)
            soup = BeautifulSoup(r.text, "lxml", multi_valued_attributes=None)

            into_main = soup.find("div", {"id": "main-wrapper"})

            # Get name
            name_book = into_main.find("h1", {"class": "title"})

            # Get author
            autho_book = into_main.find_all("a")
            authors = autho_book[34].text

            # Get genre
            genre_book = into_main.find("p", {"class": "genre"})
            genre_text = genre_book.find("a").text

            # Get download link
            download_link = f"{book}/fb2"

            # Get date
            # I can't do it
            # Maybe soon

            # Get discription
            get_p = into_main.find_all("p")
            get_discription = get_p[1].text

            # Get img src
            get_img = into_main.find_all("img")

            get_src = f"https://flibusta.is{get_img[1].get('src')}"

            # Insert into db
            conn.execute(
                "INSERT INTO books (name_book, author, genre_book, download_link, discription, img) VALUES (?, ?, ?, ?, ?, ?)", [name_book.text, authors, genre_text, download_link, get_discription, get_src])

            conn.commit()

            x += 1
            print(f"Add {x}")

        except IndexError as err:
            print(f"Skip | {err}")
            continue

        except KeyboardInterrupt:
            break

    conn.close()


def main():
    scrape_data_book(scrape_book())


if __name__ == "__main__":
    main()

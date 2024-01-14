import sqlite3


# Connect lib_book.db
conn = sqlite3.Connection('lib_book.db')
cursor_lib = conn.cursor()


def sort_genre():
    cursor_lib.execute("SELECT genre_book FROM books")
    genres = cursor_lib.fetchall()

    genre_list = []
    for genre in genres:
        for g in genre:
            genre_list.append(g)

    # delete duplicate
    sorted_list = []
    seen = set()
    for gen in genre_list:
        if gen not in seen:
            sorted_list.append(gen)
            seen.add(gen)

    # Create genre.db
    # c = sqlite3.Connection('genre.db')
    # cursor_genre = c.cursor()
    #
    # cursor_genre.execute(
    #     '''CREATE TABLE IF NOT EXISTS genre (id INTEGER PRIMARY KEY AUTOINCREMENT, genres TEXT NOT NULL)''')
    #
    # x = 0
    # for g_book in sorted_list:
    #     cursor_genre.execute(
    #         "INSERT INTO genre (genres) VALUES (?)", (g_book,))
    #     c.commit()
    #     x += 1
    #     print(f"{x}")
    #
    # c.close()

    return sorted_list


def main():
    sort_genre()


if __name__ == "__main__":
    main()
    conn.close()

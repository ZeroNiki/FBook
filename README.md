# FBook WebApp (RU)
- Fastapi
- sqlite3
- requests
- bs4

Приложение с книгами взятами из сайта Flibusta

! Ещё не полностью готов

## Установка и запуск (GNU/Linux)

1:
```sh
git clone https://github.com/ZeroNiki/FBook.git
cd FBook
```

2:
```sh
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

3:
Скачайте файл базы данных из моего [Google Drive](https://drive.google.com/file/d/1Mdt1kpnSiwIwWgcC1uE77B37oyliEblM/view?usp=sharing)
и вставьте в корень репозитория. Либо просто запустить файл `db/scrape.py` (займёт время)

4:
Запуск
```sh
python3 main.py
```

Перейдите по ссылке: http://127.0.0.1:8000



# FBook  WebApp (EN)
- Fastapi
- sqlite3
- requests
- bs4

WebApp with book taken from the site Flibusta

! Not completely ready yet

## Downlaod and run (GNU/Linux) step by step

1:
```sh
git clone https://github.com/ZeroNiki/FBook.git
cd FBook
```

2:
```sh
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

3:
Download db file from my [Google Drive](https://drive.google.com/file/d/1Mdt1kpnSiwIwWgcC1uE77B37oyliEblM/view?usp=sharing)
and move to repository root. Or just start file `db/scrape.py` (take some time)

4:
Launch
```sh
python3 main.py
```

follow the link: http://127.0.0.1:8000

from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import requests
import sqlite3 as sq


class Code:
    def __init__(self):
        self.query = ''
        self.lang = ''
        self.con = sq.connect('BD2.sl3', timeout=5)
        self.cur = self.con.cursor()
        self.create_table()
        self.pages = []

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS FINAL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            obivlenie TEXT,
            cena TEXT,
            opisanie TEXT,
            location TEXT,
            page_number INTEGER
            )''')
        self.con.commit()


    def cod_project(self):
        # self.query = input(Fore.BLACK + Back.GREEN + 'Что ищем на сайте:' + Style.RESET_ALL + ' ')
        # self.lang = input(Fore.BLACK + Back.GREEN + 'Выберете язык (ru или ua):' + Style.RESET_ALL + ' ')

        self.query = 'машина'
        self.lang = 'ru'

        if self.lang not in ('ru', 'ua'):
            print(Fore.BLACK + Back.GREEN + 'Я вас не понимаю' + Style.RESET_ALL)
            return

        try:
            html = requests.get(f'https://obyava.ua/{self.lang}/s-{self.query}?page=1')
            soup = BeautifulSoup(html.text, 'lxml')
        except requests.exceptions.RequestException:
            print(Fore.BLACK + Back.RED + 'Не удалось получить данные с сайта' + Style.RESET_ALL)
            return

        for i in soup.find_all('a', class_='pagination__item'):
            try:
                self.pages.append(int(i.getText()))
            except ValueError:
                pass
        print(f'Количество страниц: {max(self.pages)}')

        for page_num in range(1, max(self.pages) + 1):
            try:
                html = requests.get(f'https://obyava.ua/{self.lang}/s-{self.query}?page={page_num}')
                soup = BeautifulSoup(html.text, 'lxml')
            except requests.exceptions.RequestException:
                print(Fore.BLACK + Back.RED + f'Не удалось получить данные со страницы {page_num}' + Style.RESET_ALL)
                continue

            for a, b, c, d in zip(
                    soup.select('.single-item__title'),
                    soup.select('.single-item__price'),
                    soup.select('.single-item__description'),
                    soup.select('.single-item__location')
            ):
                obivlenie = a.text.strip().replace('[', '').replace(']', '')
                cena = b.text.strip().replace('[', '').replace(']', '').replace(',', '').replace('торг', '')
                opisanie = c.text.strip()
                location = d.text.strip().replace('[', '').replace(']', '')

                print(Back.LIGHTWHITE_EX + Fore.YELLOW)
                print(obivlenie, cena, opisanie, location)

                self.cur.execute(
                    f'INSERT INTO FINAL (obivlenie, cena, opisanie, location,page_number) VALUES (?, ?, ?, ?,?)',
                    (obivlenie, cena, opisanie, location,page_num)
                )
                self.con.commit()


if __name__ == '__main__':
    object_class = Code()
    object_class.cod_project()

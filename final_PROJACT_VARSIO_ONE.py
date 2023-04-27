from bs4 import BeautifulSoup
from colorama import *
import lxml,requests ,sqlite3 as sq
# импортируем библиотеки нужные для программы

# создаем класс в котором будет выполняться код
class Code:
    def __init__(self):  # иницилизируем то что нужно
        #инициализируем переменные
        self.zapros = ''
        self.obivlenie = ''
        self.cena = ''
        self.opisanie = ''
        self.location = ''


    def cod_project(self):
        # создаем БД
        with sq.connect("BD.sl3",timeout=5) as con:
            cur = con.cursor()
            #создаем курсор для манипуляции с БД
            # создаем таблицу
            cur.execute('''CREATE TABLE IF NOT EXISTS FINAL(  
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            obivlenie TEXT, 
            cena TEXT,
            opisanie TEXT,
            location TEXT
            )''')

        self.zapros = input(Fore.BLACK + Back.GREEN + 'Что ищем на сайте:' + Style.RESET_ALL + ' ')
        # запрашиваем что будем искать

        html = requests.get(f'https://obyava.ua/ua/s-{self.zapros}')
        #парсим html код
        soup = BeautifulSoup(html.text, 'lxml')
        # обрабатывает html код


        # создаем цикл с помошью которого мы парсим принтуем записываем в БД то что запарсили
        for a, b, c, d in zip(soup.select('.single-item__title'),soup.select('.single-item__price'),soup.select('.single-item__description'),soup.select('.single-item__location')):
            obivlenie = str(a).replace('<a class="single-item__title" href=','').replace('"','').replace('<','').replace('>','').replace('/a,','').replace('[','').replace(']','').replace('a class=single-item__title single-item__title--short href=','').replace('/a','').strip()
            cena = str(b).replace('<div class="single-item__price">','').replace('[','').replace(']','').replace('</span>','').replace('</div>','').replace(',','').replace('<span class="price-negotiable">','').replace('торг','').strip()
            opisanie = str(c).replace('<div class="single-item__description">', '').replace('</div>', '')
            location = str(d).replace(' <div class="single-item__location">','').replace('<svg class="single-item__geo-icon">','').replace('</svg>','').replace('</use>','').replace('</div>','').replace('<use xlink:href=','').replace('"','').replace('<div class=single-item__location>','').replace('xmlns:xlink=http://www.w3.org/1999/xlink>','')

            #переназначаем переменные
            self.obivlenie = obivlenie
            self.cena = cena
            self.opisanie = opisanie
            self.location = location


            print(Back.LIGHTWHITE_EX + Fore.YELLOW )
            #принтуем переменные
            print(obivlenie,cena,opisanie,location)

            #записываем данные в БД
            cur.execute(f'''INSERT INTO FINAL (obivlenie,cena,opisanie,location) VALUES (\"%s\",\"%s\",\"%s\",\"%s\");''' %(obivlenie,cena,obivlenie,location))
            con.commit()


if __name__ == "__main__":  # запускаем код
    c = Code()
    c.cod_project()
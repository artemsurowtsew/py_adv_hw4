# # Завдання 1
# # Зробіть таблицю для підрахунку особистих витрат із такими полями: id, призначення, сума, час.
import sqlite3 
connect = sqlite3.connect('db.sqlite3')

cursor = connect.cursor()

def create_costs_table():
    query = '''
    CREATE TABLE Сosts (
        id INT(10),
        appointment VARCHAR(55),
        amount INT(17),
        data DATETIME(10)
        );
    '''
    cursor.execute(query)

# # Завдання 2
# # Створіть консольний інтерфейс (CLI) на Python для додавання нових записів до бази даних. 

import argparse
from faker import Faker
fake = Faker("uk_UA")
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query connection success")
    except:
        print("Сonnection was unsuccess")
# # Завдання 3
# # Змініть таблицю так, щоби можна було додати не лише витрати, а й прибутки.

# def alter_cost_table():
#     query2 = '''
#     ALTER TABLE Сosts ADD COLUMN income INT(25)

#     '''
#     cursor.execute(query2)



# # Завдання 4
# # Створіть агрегатні функції для підрахунку загальної кількості  витрат i прибуткiв за місяць. 
# # Забезпечте відповідний інтерфейс користувача.

# def select_income():
#     query_income = '''
#     SELECT SUM(income) FROM Costs;
# '''
#     cursor.execute(query_income)

# select_income()

# def select_amount():
#     query_amount = '''
#     SELECT SUM(amount) FROM Costs;
# '''
#     cursor.execute(query_amount)

# select_amount()

# Завдання 5
# Create an Exchange Rates To USD db using API Monobank (api.monobank.ua). 
# Do requests via request lib, parse results, write it into db. (3 examples required)
# Example:
# Table - Exchange Rate To USD:

# id (INT PRIMARY KEY) - 1, 2, 3, ...
# currency_name (TEXT) - UAH
# currency_value (REAL) - 39.5
# current_date (DATETIME) - 10/22/2022 7:00 PM

import sys
import requests
import sqlite3
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6 import uic


urls = {
    "monobank": "https://api.monobank.ua/bank/currency",
}

DATABASE_NAME = "exchange_rates_to_usd.db"

def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExchangeRateToUSD (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_name TEXT NOT NULL,
            currency_value REAL NOT NULL,
            current_date TEXT NOT NULL
        )
    """)
    conn.commit()

def insert_exchange_rate(conn, currency_name, currency_value, current_date):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ExchangeRateToUSD (currency_name, currency_value, current_date)
            VALUES (?, ?, ?)
        """, (currency_name, currency_value, current_date))
        conn.commit()
        print(f"Вставлено в БД: {currency_name} - {currency_value} ({current_date})")
    except sqlite3.Error as e:
        print(f"Помилка вставки в БД: {e}")
        conn.rollback()

def parse_monobank():
    rates = {}
    db_conn = None 

    try:
        response = requests.get(urls["monobank"])
        response.raise_for_status()
        data = response.json()


        allowed_currencies_uah = {840: "USD", 978: "EUR"}
        for item in data:
            if item["currencyCodeA"] in allowed_currencies_uah and item["currencyCodeB"] == 980:  # 980 - UAH
                currency = allowed_currencies_uah[item["currencyCodeA"]]
                buy_rate = str(item.get("rateBuy", "N/A"))
                sell_rate = str(item.get("rateSell", "N/A"))
                rates[currency] = {"buy": buy_rate, "sell": sell_rate}

        db_conn = connect_db()
        create_table(db_conn)
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        monobank_rates_lookup = {}
        for item in data:
            key = (item.get("currencyCodeA"), item.get("currencyCodeB"))
            monobank_rates_lookup[key] = {
                "rateBuy": item.get("rateBuy"),
                "rateSell": item.get("rateSell")
            }

        usd_uah_pair = monobank_rates_lookup.get((840, 980))
        if usd_uah_pair and usd_uah_pair.get("rateSell") is not None:
            uah_per_usd = float(usd_uah_pair["rateSell"])
            insert_exchange_rate(db_conn, "UAH", uah_per_usd, current_timestamp)
        else:
            print("Не знайдено курс UAH до USD для збереження в БД.")


        eur_usd_pair = monobank_rates_lookup.get((978, 840))
        if eur_usd_pair and eur_usd_pair.get("rateSell") is not None:
            usd_per_eur = float(eur_usd_pair["rateSell"])
            insert_exchange_rate(db_conn, "EUR", usd_per_eur, current_timestamp)
        else:
            eur_uah_pair = monobank_rates_lookup.get((978, 980))
            usd_uah_pair_for_calc = monobank_rates_lookup.get((840, 980))
            if (eur_uah_pair and eur_uah_pair.get("rateSell") is not None and
                usd_uah_pair_for_calc and usd_uah_pair_for_calc.get("rateBuy") is not None and
                float(usd_uah_pair_for_calc["rateBuy"]) != 0):
                try:
                    calculated_usd_per_eur = float(eur_uah_pair["rateSell"]) / float(usd_uah_pair_for_calc["rateBuy"])
                    insert_exchange_rate(db_conn, "EUR", calculated_usd_per_eur, current_timestamp)
                    print("Розраховано EUR до USD курс через UAH для збереження в БД.")
                except (ValueError, ZeroDivisionError):
                    print("Помилка розрахунку EUR до USD через UAH.")
            else:
                print("Не знайдено курс EUR до USD для збереження в БД (або для розрахунку через UAH).")


    except requests.exceptions.RequestException as e:
        print(f"Помилка отримання даних з Monobank API: {e}")
    except Exception as e:
        print(f"Виникла неочікувана помилка: {e}")
    finally:
        if db_conn:
            db_conn.close()
    
    return rates 

def get_exchange_rates():
    rates = {}
    rates['monobank'] = parse_monobank()

    return rates

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi('window.ui', self)
        except Exception as e:
            print(f"Помилка завантаження UI файлу: {e}. Переконайтеся, що 'window.ui' існує.")
            sys.exit(1)

        self.table = self.tableWidget

        self.table.setRowCount(2) # За замовчуванням Monobank повертає USD, EUR до UAH
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(['Source', 'Currency', 'Buy Rate', 'Sell Rate'])

        self.pushButton.clicked.connect(self.load_data)

    def load_data(self):
        self.table.setRowCount(0) # Очищаємо таблицю перед завантаженням

        exchange_rates = get_exchange_rates()

        data = []
        for source, rates in exchange_rates.items():
            for currency, rate in rates.items():
                buy_rate = rate['buy']
                sell_rate = rate['sell']
                data.append((source, currency, buy_rate, sell_rate))

        self.table.setRowCount(len(data))

        for row, (source, currency, buy_rate, sell_rate) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(source))
            self.table.setItem(row, 1, QTableWidgetItem(currency))
            self.table.setItem(row, 2, QTableWidgetItem(buy_rate))
            self.table.setItem(row, 3, QTableWidgetItem(sell_rate))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
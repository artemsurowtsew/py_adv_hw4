import json 
# Завдання 1
# Створіть прості словники та конвертуйте їх у JSON.
#  Збережіть JSON у файлі та спробуйте завантажити дані з файлу.
dict1 = {"name" : "Andrew", "surname": "Kotenko", "Age" : "34"}
json_string = json.dumps(dict1, indent=4)
file_name = "output.json"
with open(file_name, 'w', encoding='utf-8') as f:
 print(f"Дані успішно збережено в файл {file_name}")

#  Завдання 2
# Створіть XML-файл із вкладеними елементами та скористайтеся мовою пошуку XPATH.
# Спробуйте здійснити пошук вмісту за створеним документом XML, 
# ускладнюючи свої запити та додаючи нові елементи, якщо буде потрібно.
from xml import etree

# 1. Створення XML-файлу
xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<library>
    <book id="bk001" available="true">
        <title lang="en">The Great Adventure</title>
        <author>John Doe</author>
        <genre>Fantasy</genre>
        <price currency="USD">25.99</price>
        <pages>320</pages>
        <reviews>
            <review rating="5">Excellent read!</review>
            <review rating="4">Enjoyed it very much.</review>
        </reviews>
    </book>
    <book id="bk002" available="false">
        <title lang="ua">Історія України</title>
        <author>Іван Франко</author>
        <genre>History</genre>
        <price currency="UAH">450.00</price>
        <pages>600</pages>
        <reviews>
            <review rating="5">Дуже інформативно.</review>
        </reviews>
    </book>
    <magazine id="mg001" type="monthly">
        <title>Tech World</title>
        <issue>10</issue>
        <year>2023</year>
    </magazine>
</library>
"""

with open("library.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

print("XML-файл 'library.xml' створено.")

tree = etree.parse("library.xml")

print("\nXPath Запити")

titles = tree.xpath("//book/title")
print("\n1. Назви всіх книг:")
for title in titles:
    print(f"- {title.text}")

authors = tree.xpath("//author")
print("\n2. Всі автори:")
for author in authors:
    print(f"- {author.text}")

price_bk001 = tree.xpath("//book[@id='bk001']/price/text()")
print(f"\n3. Ціна книги з ID 'bk001': {price_bk001[0]}")

available_titles = tree.xpath("//book[@available='true']/title/text()")
print("\n4. Назви всіх доступних книг:")
for title in available_titles:
    print(f"- {title}")

english_books = tree.xpath("//book/title[@lang='en']/parent::book")
print("\n5. Деталі книг англійською мовою:")
for book in english_books:
    print(f"- ID: {book.get('id')}, Title: {book.find('title').text}, Author: {book.find('author').text}")

rating_5_reviews = tree.xpath("//review[@rating='5']/text()")
print("\n6. Відгуки з рейтингом 5:")
for review in rating_5_reviews:
    print(f"- {review}")

long_books = tree.xpath("//book[pages > 400]/title/text()")
print("\n7. Назви книг, що мають більше 400 сторінок:")
for title in long_books:
    print(f"- {title}")

magazine_titles = tree.xpath("//magazine/title/text()")
print(f"\n8. Назви всіх журналів: {magazine_titles[0]}")

usd_prices = tree.xpath("//price[@currency='USD']/text()")
print(f"\n9. Ціни книг у USD: {usd_prices}")

elements_with_id = tree.xpath("//*[@id]")
print("\n10. Елементи, що мають атрибут 'id':")
for elem in elements_with_id:
    print(f"- {elem.tag} (ID: {elem.get('id')})")

# Завдання 3
# Попрацюйте зі створенням власних діалектів, довільно вибираючи правила для CSV-файлів.
# Зареєструйте створені діалекти та попрацюйте, використовуючи їх зі створенням/читанням файлом.
import csv
import io 


class MyCommaDialect(csv.Dialect):
    """Діалект CSV з комою як роздільником та подвійними лапками для цитування."""
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL

class MySemicolonDialect(csv.Dialect):
    """Діалект CSV з крапкою з комою як роздільником та без цитування."""
    delimiter = ';'
    quotechar = '' 
    doublequote = False
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE

csv.register_dialect('my_comma_dialect', MyCommaDialect)
csv.register_dialect('my_semicolon_dialect', MySemicolonDialect)

print("Діалекти CSV 'my_comma_dialect' та 'my_semicolon_dialect' зареєстровано.")

# Дані для запису
data = [
    ['Name', 'Age', 'City', 'Notes'],
    ['Alice', 30, 'New York', 'Likes "pizza", has a dog'],
    ['Bob', 24, 'London', 'Works in IT; enjoys hiking'],
    ['Charlie', 35, 'Paris', 'Speaks French, loves art']
]

file_comma = 'data_comma.csv'
with open(file_comma, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, dialect='my_comma_dialect')
    writer.writerows(data)
print(f"\nДані записано у '{file_comma}' з використанням 'my_comma_dialect'.")

file_semicolon = 'data_semicolon.csv'
with open(file_semicolon, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, dialect='my_semicolon_dialect')
    writer.writerows(data)
print(f"Дані записано у '{file_semicolon}' з використанням 'my_semicolon_dialect'.")

print(f"\nЧитання з '{file_comma}' (my_comma_dialect):")
with open(file_comma, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, dialect='my_comma_dialect')
    for row in reader:
        print(row)

print(f"\nЧитання з '{file_semicolon}' (my_semicolon_dialect):")
with open(file_semicolon, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, dialect='my_semicolon_dialect')
    for row in reader:
        print(row)

print("\nДемонстрація роботи з рядковим потоком (my_comma_dialect):")
output_stream = io.StringIO()
writer = csv.writer(output_stream, dialect='my_comma_dialect')
writer.writerows(data)
csv_string = output_stream.getvalue()
print(csv_string)

input_stream = io.StringIO(csv_string)
reader = csv.reader(input_stream, dialect='my_comma_dialect')
read_data = list(reader)
print("Прочитані дані з рядкового потоку:", read_data)

#Завдання 4
import sqlite3
import json

DATABASE_NAME = 'materials.db'

def create_materials_table():
    """Створює таблицю 'матеріали'."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            additional_properties TEXT -- JSON-рядок для зберігання масиву кортежів
        );
    ''')
    conn.commit()
    conn.close()
    print(f"Таблиця 'materials' створена у {DATABASE_NAME}.")

def insert_material(material_id, weight, height, properties):
    """Вставляє новий матеріал у таблицю."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    json_properties = json.dumps(properties)
    
    cursor.execute('''
        INSERT INTO materials (id, weight, height, additional_properties)
        VALUES (?, ?, ?, ?);
    ''', (material_id, weight, height, json_properties))
    conn.commit()
    conn.close()
    print(f"Матеріал id={material_id} успішно додано.")

def get_material(material_id):
    """Отримує матеріал з таблиці та десеріалізує властивості."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM materials WHERE id = ?;', (material_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        material_id, weight, height, json_properties = row
        properties = json.loads(json_properties)
        return {"id": material_id, "weight": weight, "height": height, "additional_properties": properties}
    return None

create_materials_table()

material1_props = [("color", "red"), ("density", 2.7)]
insert_material(1, 10.5, 50.2, material1_props)

material2_props = [("flexibility", "high"), ("strength", "low"), ("texture", "smooth")]
insert_material(2, 20.1, 100.0, material2_props)

material3_props = []
insert_material(3, 15.0, 75.5, material3_props)

material4_props = [("thermal_conductivity", 0.5)]
insert_material(4, 12.8, 60.1, material4_props)

print("\nОтримання матеріалу з ID 1:")
mat = get_material(1)
if mat:
    print(mat)

print("\nОтримання матеріалу з ID 2:")
mat = get_material(2)
if mat:
    print(mat)

print("\nОтримання матеріалу з ID 3:")
mat = get_material(3)
if mat:
    print(mat)

# Перевірка вмісту таблиці
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
print("\nВсі записи в таблиці 'materials':")
cursor.execute('SELECT * FROM materials;')
for row in cursor.fetchall():
    print(row)
conn.close()

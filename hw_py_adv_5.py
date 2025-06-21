# Завдання 1
# Створіть функцію для обчислення факторіала числа. 
# Запустіть декілька завдань, використовуючи Thread, 
# і заміряйте швидкість їхнього виконання, а потім заміряйте швидкість обчислення, 
# використовуючи той же набір завдань на ThreadPoolExecutor. 
# Як приклади використовуйте останні значення, від мінімальних і до максимально можливих, 
# щоб побачити приріст або втрату продуктивності.
import threading

import time
def fibo():
    n=35  
    if n<=1:
        print(f"n= {n}, програма завершила свою роботу")
        return n
    else:
        a=0
        b=1
        for _ in range (2,n + 1):
           a,b=b,a+b
           time.sleep(0.2)
           print(b)
        return b


def print_text():
    text='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
    when an unknown printer took a galley of '''
    for i in range(22):
        time.sleep(0.3)
        print(text[i])

start_time1 = time.perf_counter()
thread1 = threading.Thread(target=fibo)
# thread2 = threading.Thread(target=print_text)

thread1.start()
# thread2.start()

thread1.join()
# thread2.join()
end_time1 = time.perf_counter()
print("ThreadPoolExecutor")
from concurrent.futures import ThreadPoolExecutor
def fibo_threadpool(n): 
        if n<=1:
            print(f"n= {n}, програма завершила свою роботу")
            return n
        else:
            a=0
            b=1
        for _ in range (2,n + 1):
                a,b=b,a+b
                time.sleep(0.2)
                print(b)
        return b

print("Демонстрація ThreadPoolExecutor з функцією Фібоначчі")

start_time = time.perf_counter()


with ThreadPoolExecutor(max_workers=3) as executor:

        future1 = executor.submit(fibo_threadpool, 10)
        future2 = executor.submit(fibo_threadpool, 20)
        future3 = executor.submit(fibo_threadpool, 15)

        try:
            result1 = future1.result()
            print(f"Результат Фібоначчі(10): {result1}")

            result2 = future2.result()
            print(f"Результат Фібоначчі(20): {result2}")

            result3 = future3.result()
            print(f"Результат Фібоначчі(15): {result3}")

        except Exception as e:
            print(f"Під час виконання завдання виникла помилка: {e}")

end_time = time.perf_counter()
print(f"\n Всі завдання завершено за {end_time1 - start_time1:.4f} секунд (threading)")
print(f"\n Всі завдання завершено за {end_time - start_time:.4f} секунд (ThreadPool)")

# Завдання 2
# Створіть три функції, одна з яких читає файл на диску із заданим ім'ям та перевіряє наявність рядка «Wow!».
#  Якщо файлу немає, то засипає на 5 секунд, а потім знову продовжує пошук по файлу. 
#  Якщо файл є, то відкриває його і шукає рядок «Wow!». 
#  За наявності цього рядка закриває файл і генерує подію, 
#  а інша функція чекає на цю подію і у разі її виникнення виконує видалення цього файлу.
#   Якщо рядки «Wow!» не було знайдено у файлі, 
# то засипати на 5 секунд. Створіть файл руками та перевірте виконання програми.
import threading
import time
import os

file_found_event = threading.Event()

FILE_NAME = "my_test_file.txt"
SEARCH_STRING = "Wow!"

def read_and_check_file():

    print(f"Потік читання: Пошук файлу '{FILE_NAME}'...")
    while True:
        if not os.path.exists(FILE_NAME):
            print(f"Потік читання: Файл '{FILE_NAME}' не знайдено. Засипаю на 5 секунд...")
            time.sleep(5)
            continue

        print(f"Потік читання: Файл '{FILE_NAME}' знайдено. Відкриваю для пошуку рядка...")
        found = False
        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if SEARCH_STRING in line:
                        print(f"Потік читання: Рядок '{SEARCH_STRING}' знайдено у файлі '{FILE_NAME}' на рядку {line_num}.")
                        found = True
                        break
            if found:
                print("Потік читання: Генерую подію")
                file_found_event.set() 
                break 
            else:
                print(f"Потік читання: Рядок '{SEARCH_STRING}' не знайдено у файлі '{FILE_NAME}'. Засинаю на 5 секунд...")
                time.sleep(5)
        except IOError as e:
            print(f"Потік читання: Помилка при читанні файлу '{FILE_NAME}': {e}. Засинаю на 5 секунд...")
            time.sleep(5)
        except Exception as e:
            print(f"Потік читання: Несподівана помилка: {e}. Засинаю на 5 секунд...")
            time.sleep(5)

def delete_file_on_event():

    print("Потік видалення: Очікую подію 'файл знайдено'...")
    file_found_event.wait() 
    
    print("Потік видалення: Подія отримана! Видаляю файл...")
    try:
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
            print(f"Потік видалення: Файл '{FILE_NAME}' успішно видалено.")
        else:
            print(f"Потік видалення: Файл '{FILE_NAME}' вже не існує.")
    except OSError as e:
        print(f"Потік видалення: Помилка при видаленні файлу '{FILE_NAME}': {e}")
    except Exception as e:
        print(f"Потік видалення: Несподівана помилка при видаленні: {e}")

def main():
    """Основна функція для запуску потоків."""
    print("Запускаю програму...")

    reader_thread = threading.Thread(target=read_and_check_file)
    reader_thread.start()


    deleter_thread = threading.Thread(target=delete_file_on_event)
    deleter_thread.start()


    reader_thread.join()
    deleter_thread.join()

    print("Програма завершила роботу.")

main()

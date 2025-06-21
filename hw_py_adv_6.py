# Завдання 1
# Створіть співпрограму, 
# яка отримує контент із зазначених посилань 
# і логує хід виконання в database, використовуючи стандартну бібліотеку requests,
# а потім проробіть те саме з бібліотекою aiohttp. 
# Кроки, які мають бути залоговані: початок запиту до адреси X,
# відповідь для адреси X отримано зі статусом 200. Перевірте хід виконання програми на >3 ресурсах 
# і перегляньте послідовність запису логів в обох варіантах і порівняйте результати. 
# Для двох видів завдань використовуйте різні файли для логування, щоби порівняти отриманий результат. 

import requests
import time
import datetime


LOG_FILE_SYNC = "sync_log.txt"

def log_to_db(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(LOG_FILE_SYNC, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def fetch_content_sync(url):
    log_to_db(f"Початок запиту до адреси: {url}")
    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code
        log_to_db(f"Відповідь для адреси: {url} отримано зі статусом {status_code}")
        return f"OK: {url} (Status: {status_code})"
    except requests.exceptions.RequestException as e:
        log_to_db(f"Помилка при запиті до адреси: {url} - {e}")
        return f"Error: {url} - {e}"

if __name__ == "__main__":
    with open(LOG_FILE_SYNC, "w") as f:
        f.write("")

    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/comments/1",
        "https://jsonplaceholder.typicode.com/users/1",
        "https://www.google.com"
    ]

    print(f"Запуск синхронного fetcher'а. Логи зберігаються у '{LOG_FILE_SYNC}'")
    start_time = time.perf_counter()

    for url in urls:
        result = fetch_content_sync(url)
        print(result)

    end_time = time.perf_counter()
    print(f"\nСинхронний fetcher завершив роботу за {end_time - start_time:.4f} секунд.")
    log_to_db(f"Синхронний fetcher завершив роботу за {end_time - start_time:.4f} секунд.")
# Завдання 2
# Розробіть сокет-сервер на основі бібліотеки asyncio.
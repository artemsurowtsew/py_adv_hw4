# дз 4 5 6 8
# Завдання 6
# Використовуючи сервіс https://jsonplaceholder.typicode.com/, 
# спробуйте побудувати різні типи запитів та обробити відповіді. 
# Необхідно попрактикуватися з urllib та бібліотекою requests. Рекомендується спочатку спробувати виконати запити,
# використовуючи urllib, а потім спробувати реалізувати те саме, використовуючи requests.
import requests

def get_posts_requests():
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        posts = response.json()
        print("--- requests GET All Posts ---")
        for post in posts[:5]:
            print(f"ID: {post['id']}, Title: {post['title']}")
        print(f"Total posts: {len(posts)}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Connection error occurred: {err}")
    except requests.exceptions.Timeout as err:
        print(f"Timeout error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

get_posts_requests()


# Завдання 8
# Створіть HTTP-клієнта, який прийматиме URL ресурсу, 
# тип методу та словник як передавальні дані (опціональний). 
# Виконувати запит з отриманим методом на отриманий ресурс,
#  передаючи дані відповідним методом, 
# та друкувати на консоль статус-код, заголовки та тіло відповіді.
import requests
import json

def http_client(url: str, method: str, data: dict = None):
    """
    Універсальний HTTP-клієнт для виконання запитів.

    Аргументи:
    url (str): URL-адреса ресурсу.
    method (str): HTTP-метод запиту (GET, POST, PUT, DELETE, PATCH).
    data (dict, optional): Словник з даними для відправки.
                            Для GET-запитів - це параметри URL.
                            Для POST/PUT/PATCH - це JSON-тіло запиту.
    """
    method = method.upper() 

    print(f"\n--- Виконання {method} запиту до {url} ---")

    try:
        response = None
        if method == 'GET':
            response = requests.get(url, params=data)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'PATCH':
            response = requests.patch(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, json=data) 
        else:
            print(f"Помилка: Непідтримуваний HTTP-метод '{method}'")
            return

        if response:
            print(f"\n--- Статус-код: {response.status_code} ---")
            print("\n--- Заголовки відповіді ---")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")

            print("\n--- Тіло відповіді ---")
            try:
                response_body = response.json()
                print(json.dumps(response_body, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(response.text)
            print("\n" + "="*60)

    except requests.exceptions.ConnectionError as e:
        print(f"Помилка підключення: Не вдалося підключитися до {url}. Перевірте URL або ваше інтернет-з'єднання. Помилка: {e}")
    except requests.exceptions.Timeout:
        print(f"Таймаут запиту: Запит до {url} перевищив час очікування.")
    except requests.exceptions.RequestException as e:
        print(f"Виникла несподівана помилка при виконанні запиту: {e}")

if __name__ == "__main__":
    http_client("https://jsonplaceholder.typicode.com/posts", "GET")

    http_client("https://jsonplaceholder.typicode.com/posts", "GET", data={"userId": 1})

    http_client("https://jsonplaceholder.typicode.com/posts/1", "GET")

    new_post_data = {
        "title": "Мій новий пост",
        "body": "Це тестовий пост, створений за допомогою мого HTTP-клієнта.",
        "userId": 101
    }
    http_client("https://jsonplaceholder.typicode.com/posts", "POST", data=new_post_data)

    updated_post_data = {
        "id": 1, 
        "title": "Оновлений заголовок",
        "body": "Оновлене тіло посту через PUT-запит.",
        "userId": 1
    }
    http_client("https://jsonplaceholder.typicode.com/posts/1", "PUT", data=updated_post_data)

    patch_data = {
        "title": "Тільки заголовок змінено PATCH-запитом"
    }
    http_client("https://jsonplaceholder.typicode.com/posts/2", "PATCH", data=patch_data)

    http_client("https://jsonplaceholder.typicode.com/posts/1", "DELETE")

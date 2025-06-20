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
    n=25  
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
    alt='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
    when an unknown printer took a galley of '''
    for i in range(22):
        time.sleep(0.3)
        print(alt[i])

start_time1 = time.perf_counter()
thread1 = threading.Thread(target=fibo)
thread2 = threading.Thread(target=print_text)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
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
time.sleep(5)

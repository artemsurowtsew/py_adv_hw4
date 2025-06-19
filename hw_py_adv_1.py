# Завдання 2
# Напишіть декоратор, який буде заміряти час виконання для наданої функції.
N_FIB_COUNT = 25
import time
from functools import lru_cache

def time_decorator(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args, **kwargs) 
        end = time.time()
        execution_time = end - start
        print(f"Функція '{func.__name__}' виконана за {execution_time:.6f} секунд.")
        return result 
    return wrapper 


@time_decorator
def my_function():
    time.sleep(1)
    print("Hello from my_function!")


my_function()
# Завдання 3

# Напишіть програму яка буде виводити 25 перших чисел Фібоначі, використовуючи для цього три наведені в тексті 
# заняття функції — без кешу, з кешем довільної довжини,

#  з кешем з модулю functools з максимальною кількістю 10 елементів та з кешем з модулю functools з максимальною кількістю 16 елементів.

def fibonacci_recursive(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

number = 10
print(f"Число Фибоначчи для {number}: {fibonacci_recursive(number)}")



@lru_cache
def fibonacci_recursive_lru(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursive_lru(n-1) + fibonacci_recursive_lru(n-2)

number = 10
print(f"Число Фибоначчи для {number}: {fibonacci_recursive_lru(number)} з lru_cache")


@lru_cache(maxsize=10)
def fibonacci_recursive_lru10(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursive_lru10(n-1) + fibonacci_recursive_lru10(n-2)

number = 10
print(f"Число Фибоначчи для {number}: {fibonacci_recursive_lru10(number)} з lru_cache")


@lru_cache(maxsize=16)
def fibonacci_recursive_lru16(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursive_lru16(n-1) + fibonacci_recursive_lru16(n-2)


print("Варіант 1: Без кешу")
@time_decorator
def run_fibonacci_no_cache_test():
        return [fibonacci_recursive(i) for i in range(N_FIB_COUNT)]
    
fibonacci_recursive = run_fibonacci_no_cache_test()

print("Варіант 2: З кешем LRU")
@time_decorator
def run_fibonacci_lru_cache():
    return[fibonacci_recursive_lru(i) for i in range(N_FIB_COUNT)]

fibonacci_recursive_lru = run_fibonacci_lru_cache()

print("Варіант 3: З кешем LRU =10")
@time_decorator
def run_fibonacci_lru_cache10():
    return[fibonacci_recursive_lru10(i) for i in range(N_FIB_COUNT)]

fibonacci_recursive_lru10 = run_fibonacci_lru_cache10()

print("Варіант 4: З кешем LRU =16")
@time_decorator
def run_fibonacci_lru_cache16():
    return[fibonacci_recursive_lru16(i) for i in range(N_FIB_COUNT)]

fibonacci_recursive_lru16 = run_fibonacci_lru_cache16()

# Завдання 5
def get_squares_numbers(numbers):
    squares_numbers= []
    for num in numbers:
        if num %2 != 0:
            squares_numbers.append(num ** 2)
    return squares_numbers

my_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
squares_of_odd_numbers_list = get_squares_numbers(my_numbers)


print(f"Оригінальний список чисел: {my_numbers}")
print(f"Список квадратів непарних чисел: {squares_of_odd_numbers_list}")


another_list = [0, -1, 2, -3, 4, -5, 6, 7]
squares_from_another_list = get_squares_numbers(another_list)
print(f"\nОригінальний список чисел: {another_list}")
print(f"Список квадратів непарних чисел: {squares_from_another_list}")


# Завдання 6
# Створіть функцію-генератор чисел Фібоначчі. 
# Застосуйте до неї декоратор, який залишатиме в послідовності лише парні числа.

def fibonacci_generator(limit):

    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

def fibo_decorator(generator_func):
    def wrapper(*args, **kwargs):
        original_generator =generator_func(*args, **kwargs)
        for number in original_generator:
            if number % 2 == 0:
                yield number
    return wrapper

@fibo_decorator
def fibo_even_generator(limit):
    """
    Декорований генератор чисел Фібоначчі, що видає лише парні числа.
    """
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

print("Парні числа Фібоначчі до 100:")
for num in fibo_even_generator(100):
    print(num)

print("Парні числа Фібоначчі до 1000:")
for num in fibo_even_generator(1000):
    print(num)


#     Завдання 7
# Створіть звичайну функцію множення двох чисел. 
# Створіть карированну функцію множення двох чисел. Частково застосуйте її до одного аргументу, до двох аргументiв.

# Завдання 7


def multiply_regular(a, b):
    """
    Звичайна функція, яка множить два числа.
    """
    return a * b


def multiply_curried(a):
    """
    Каррірована функція множення.
    Перша функція приймає аргумент 'a' і повертає іншу функцію.
    """
    def inner_multiply(b):
        """
        Внутрішня функція приймає аргумент 'b' і виконує множення.
        """
        return a * b
    return inner_multiply



print("--- Звичайна функція множення ---")
result_regular = multiply_regular(5, 3)
print(f"multiply_regular(5, 3) = {result_regular}") # 15

result_regular_2 = multiply_regular(10, 4)
print(f"multiply_regular(10, 4) = {result_regular_2}") # 40

print("\n--- Каррірована функція множення ---")

multiply_by_2 = multiply_curried(2) 
print(f"Створена функція: multiply_by_2 = multiply_curried(2)")

result_curried_part1_a = multiply_by_2(5)
print(f"multiply_by_2(5) = {result_curried_part1_a}") # 10 (2 * 5)

result_curried_part1_b = multiply_by_2(10)
print(f"multiply_by_2(10) = {result_curried_part1_b}") # 20 (2 * 10)

multiply_by_7 = multiply_curried(7)
print(f"\nСтворена функція: multiply_by_7 = multiply_curried(7)")
result_curried_part1_c = multiply_by_7(3)
print(f"multiply_by_7(3) = {result_curried_part1_c}") # 21 (7 * 3)


# 2. Застосування до обох аргументів (як звичайна функція, але через каррірований виклик)
# Це не є "частковим застосуванням", а послідовним викликом каррірованої функції.
# Технічно, це все ще каррірований виклик, але він відразу завершує обчислення.
print("\n Каррірована функція: застосування до обох аргументів одночасно")
result_curried_full = multiply_curried(5)(3)
print(f"multiply_curried(5)(3) = {result_curried_full}") 

result_curried_full_2 = multiply_curried(8)(6)
print(f"multiply_curried(8)(6) = {result_curried_full_2}") 

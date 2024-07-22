import random
import math
from tkinter import font as tkfont
import tkinter as tk
from tkinter import messagebox
from random import getrandbits

# Функции криптосистемы
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def modular_inverse(a, m):
    m0 = m
    y = 0
    x = 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m

        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    if x < 0:
        x = x + m0

    return x


def l_function(x, n):
    return (x - 1) // n


def generate_keys(p, q):
    n = p * q
    lambda_n = (p - 1) * (q - 1) // gcd(p - 1, q - 1)

    g = random.randint(2, n ** 2)
    while gcd(l_function(pow(g, lambda_n, n ** 2), n), n) != 1:
        g = random.randint(2, n ** 2)

    mu = modular_inverse(l_function(pow(g, lambda_n, n ** 2), n), n)

    return (n, g), (lambda_n, mu)


def encrypt(m, pub_key):
    n, g = pub_key
    r = random.randint(1, n - 1)
    c = pow(g, m, n ** 2) * pow(r, n, n ** 2) % (n ** 2)
    return c


def decrypt(c, priv_key, pub_key):
    lambda_n, mu = priv_key
    n = pub_key[0]
    m = l_function(pow(c, lambda_n, n ** 2), n) * mu % n
    return m

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def gen_p_and_q(message):
    bits = len(bin(message))
    p, q = gen_p_q(bits)
    while p * q <= message:
        p, q = gen_p_q(bits)
    return p, q

def gen_p_q(bits):
    return 41, 17
    while True:
        p = getrandbits(bits)
        if is_prime(p):
            break
    while True:
        q = getrandbits(bits)
        if is_prime(q) and p != q:
            break
    return p, q

# Функции интерфейса

def encode_nums(nums):
    try:
        global public_key, private_key
        max_num = max(nums)
        private_key = list(map(int, entry_priv_key.get().split()))
        public_key = list(map(int, entry_pub_key.get().split()))

        if len(private_key) != 2 or len(public_key) != 2:
            p, q = gen_p_and_q(max_num)
            public_key, private_key = generate_keys(p, q)
        elif public_key[0] < max_num:
            messagebox.showerror("Ошибка", "Открытый ключ n меньше зашифрованного числа. Генерация новых ключей")
            p, q = gen_p_and_q(max_num)
            public_key, private_key = generate_keys(p, q)
        else:
            private_key = tuple(private_key)
            public_key = tuple(public_key)
        #print(p, q)
        entry_pub_key.delete(0, tk.END)
        entry_pub_key.insert(0, ' '.join(map(str, public_key)))
        entry_priv_key.delete(0, tk.END)
        entry_priv_key.insert(0, ' '.join(map(str, private_key)))
        encrypted_nums = [encrypt(num, public_key) for num in nums]
        return encrypted_nums
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректную строку.")
def generate_keys_ui():
    try:
        global public_key, private_key
        nums = list(map(int, entry_numbers.get().split()))
        max_num = max(nums)
        private_key = list(map(int, entry_priv_key.get().split()))
        public_key = list(map(int, entry_pub_key.get().split()))

        if len(private_key) != 2 or len(public_key) != 2:
            p, q = gen_p_and_q(max_num)
            public_key, private_key = generate_keys(p, q)
        elif public_key[0] < max_num:
            messagebox.showerror("Ошибка", "Открытый ключ n меньше зашифрованного числа. Генерация новых ключей")
            p, q = gen_p_and_q(max_num)
            public_key, private_key = generate_keys(p, q)
        else:
            private_key = tuple(private_key)
            public_key = tuple(public_key)
        #print(p, q)
        encrypted_nums = [encrypt(num, public_key) for num in nums]
        entry_encrypted_numbers.delete(0, tk.END)
        entry_encrypted_numbers.insert(0, ' '.join(map(str, encrypted_nums)))
        entry_pub_key.delete(0, tk.END)
        entry_pub_key.insert(0, ' '.join(map(str, public_key)))
        entry_priv_key.delete(0, tk.END)
        entry_priv_key.insert(0, ' '.join(map(str, private_key)))
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа.")

def generate_keys_ui_word():
    try:
        global public_key, private_key
        #words = list(map(str, entry_numbers.get().split()))
        text = str(entry_numbers.get())
        nums = []
        for letter in text:
            nums.append(ord(letter))
        encrypted_nums = encode_nums(nums)
        entry_encrypted_numbers.delete(0, tk.END)
        entry_encrypted_numbers.insert(0, ' '.join(map(str, encrypted_nums)))
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректную строку.")


def decrypt_ui():
    try:
        nums = list(map(int, entry_encrypted_numbers.get().split()))
        private_key = tuple(map(int, entry_priv_key.get().split()))
        public_key = tuple(map(int, entry_pub_key.get().split()))
        if len(private_key) != 2 or len(public_key) != 2:
            messagebox.showerror("Ошибка", "Введите корректные зашифрованные числа и закрытый ключ.")
        else:
            decrypted_nums = [decrypt(num, private_key, public_key) for num in nums]
            entry_decrypted_numbers.delete(0, tk.END)
            entry_decrypted_numbers.insert(0, ' '.join(map(str, decrypted_nums)))
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные зашифрованные числа и закрытый ключ.")

def decrypt_str(nums):
    try:
        private_key = tuple(map(int, entry_priv_key.get().split()))
        public_key = tuple(map(int, entry_pub_key.get().split()))
        if len(private_key) != 2 or len(public_key) != 2:
            messagebox.showerror("Ошибка", "Введите корректные числа и закрытый ключ.")
        else:
            decrypted_nums = [decrypt(num, private_key, public_key) for num in nums]
            text = ''
            for letter_code in decrypted_nums:
                text += chr(letter_code)
            entry_decrypted_numbers.delete(0, tk.END)
            entry_decrypted_numbers.insert(0, text)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа и закрытый ключ.")


def decrypt_ui_text():
    try:
        nums = list(map(int, entry_encrypted_numbers.get().split()))
        decrypt_str(nums)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа и закрытый ключ.")


#addition_numbers
def addition_numbers():
    try:
        # Получаем числа из полей ввода
        num1 = int(entry_addition_number1.get())
        num2 = int(entry_addition_number2.get())

        # Вычисляем произведение
        result = num1 + num2

        # Выводим результат в поле для результата
        entry_addition_result.delete(0, tk.END)
        entry_addition_result.insert(0, str(result))
    except ValueError:
        # Очищаем поле результата, если ввод некорректен
        entry_addition_result.delete(0, tk.END)
        entry_addition_result.insert(0, "Ошибка ввода")

#exponentiation
def binary_exponentiation(a, b):
    result = 1
    base = a
    exponent = b

    while exponent > 0:
        if exponent % 2 == 1:  # Если степень нечетная
            result *= base
        base *= base  # Удваиваем основание
        exponent //= 2  # Делим степень пополам

    return result
def exponentiation():
    try:
        # Получаем числа из полей ввода
        num1 = int(entry_exponentiation_number1.get())
        num2 = int(entry_exponentiation_number2.get())
        n = int(entry_exponentiation_n.get())

        # Вычисляем произведение
        result = binary_exponentiation(num1, num2) % (n ** 2)

        # Выводим результат в поле для результата
        entry_exponentiation_result.delete(0, tk.END)
        entry_exponentiation_result.insert(0, str(result))
    except ValueError:
        # Очищаем поле результата, если ввод некорректен
        entry_exponentiation_result.delete(0, tk.END)
        entry_exponentiation_result.insert(0, "Ошибка ввода")
def multiply_numbers_n():
    try:
        # Получаем числа из полей ввода
        num1 = int(entry_multiply_number1.get())
        num2 = int(entry_multiply_number2.get())
        n = int(entry_n.get())

        # Вычисляем произведение
        result = (num1 * num2) % (n ** 2)
        res2 = (num1 * num2) % n

        # Выводим результат в поле для результата
        entry_multiply_result.delete(0, tk.END)
        entry_multiply_result.insert(0, str(result))
        entry_multiply2_result.delete(0, tk.END)
        entry_multiply2_result.insert(0, str(res2))
    except ValueError:
        # Очищаем поле результата, если ввод некорректен
        entry_multiply_result.delete(0, tk.END)
        entry_multiply_result.insert(0, "Ошибка ввода")


# Интерфейс

root = tk.Tk()
root.title("Шифрование и Дешифрование")
width = 80
r = 0
# Увеличиваем общий шрифт для всех виджетов
input_font = tkfont.Font(family="Helvetica", size=11)
title_font = tkfont.Font(family="Helvetica", size=15, weight="bold")
default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(size=12)  # Увеличиваем размер шрифта до 12

frame = tk.Frame(root)
frame.pack(pady=11, padx=11)

# Теперь все виджеты будут использовать увеличенный размер шрифта
tk.Label(frame, text=" Paillier's cryptographic system", font=title_font).grid(row=r + 0, column=0, sticky="w")
tk.Label(frame, text="").grid(row=r + 0, column=0, sticky="w")
tk.Label(frame, text="Числа для шифрования (через пробел):").grid(row=r + 2, column=0, sticky="w")
entry_numbers = tk.Entry(frame, width=width, font=input_font)
entry_numbers.grid(row=r + 2, column=1, pady=5, )

tk.Button(frame, text="Зашифровать последовательность чисел", command=generate_keys_ui).grid(row=r + 3, column=0, columnspan=2)
tk.Button(frame, text="Зашифровать строку в последовательность чисел", command=generate_keys_ui_word).grid(row=r + 4, column=0, columnspan=2)
#generate_keys_ui_word_to_text
tk.Label(frame, text="Зашифрованные числа:").grid(row=r + 5, column=0, sticky="w")
entry_encrypted_numbers = tk.Entry(frame, width=width, font=input_font)
entry_encrypted_numbers.grid(row=r + 5, column=1, pady=5)

tk.Label(frame, text="Открытый ключ (n, g):").grid(row=r + 6, column=0, sticky="w")
entry_pub_key = tk.Entry(frame, width=width, font=input_font)
entry_pub_key.grid(row=r + 6, column=1, pady=5)

tk.Label(frame, text="Закрытый ключ (lambda, mu):").grid(row=r + 7, column=0, sticky="w")
entry_priv_key = tk.Entry(frame, width=width, font=input_font)
entry_priv_key.grid(row=r + 7, column=1, pady=5)

tk.Button(frame, text="Расшифровать последовательность чисел", command=decrypt_ui).grid(row=r + 8, column=0, columnspan=2)
tk.Button(frame, text="Расшифровать строку из последовательности чисел", command=decrypt_ui_text).grid(row=r + 9, column=0, columnspan=2)
#decrypt_ui_text
tk.Label(frame, text="Расшифрованные числа/строка:").grid(row=r + 10, column=0, sticky="w")
entry_decrypted_numbers = tk.Entry(frame, width=width, font=input_font)
entry_decrypted_numbers.grid(row=r + 10, column=1, pady=5)

tk.Label(frame, text="").grid(row=r + 11, column=0, sticky="w")

# Добавление новых виджетов для умножения чисел

tk.Label(frame, text="Умножение чисел по модулю n^2").grid(row=r + 12, column=0, sticky="w")

tk.Label(frame, text="Введите первое число:").grid(row=r + 13, column=0, sticky="w")
entry_multiply_number1 = tk.Entry(frame, width=width, font=input_font)
entry_multiply_number1.grid(row=r + 13, column=1, pady=5)

tk.Label(frame, text="Введите второе число:").grid(row=r + 14, column=0, sticky="w")
entry_multiply_number2 = tk.Entry(frame, width=width, font=input_font)
entry_multiply_number2.grid(row=r + 14, column=1, pady=5)

tk.Label(frame, text="Введите число n:").grid(row=r + 15, column=0, sticky="w")
entry_n = tk.Entry(frame, width=width, font=input_font)
entry_n.grid(row=r + 15, column=1, pady=5)

tk.Label(frame, text="Результат умножения по модулю n^2:").grid(row=r + 16, column=0, sticky="w")
entry_multiply_result = tk.Entry(frame, width=width, font=input_font)
entry_multiply_result.grid(row=r + 16, column=1, pady=5)
r += 1
tk.Label(frame, text="Результат умножения по модулю n:").grid(row=r + 16, column=0, sticky="w")
entry_multiply2_result = tk.Entry(frame, width=width, font=input_font)
entry_multiply2_result.grid(row=r + 16, column=1, pady=5)

tk.Button(frame, text="Умножить", command=multiply_numbers_n).grid(row=r + 17, column=0, columnspan=2)


tk.Label(frame, text="Сложение чисел").grid(row=r + 18, column=0, sticky="w")

tk.Label(frame, text="Введите первое число:").grid(row=r + 19, column=0, sticky="w")
entry_addition_number1 = tk.Entry(frame, width=width, font=input_font)
entry_addition_number1.grid(row=r + 19, column=1, pady=5)

tk.Label(frame, text="Введите второе число:").grid(row=r + 20, column=0, sticky="w")
entry_addition_number2 = tk.Entry(frame, width=width, font=input_font)
entry_addition_number2.grid(row=r + 20, column=1, pady=5)


tk.Label(frame, text="Результат сложения:").grid(row=r + 21, column=0, sticky="w")
entry_addition_result = tk.Entry(frame, width=width, font=input_font)
entry_addition_result.grid(row=r + 21, column=1, pady=5)

tk.Button(frame, text="Сложить", command=addition_numbers).grid(row=r + 22, column=0, columnspan=2)

#exponentiation

tk.Label(frame, text="Возведение числа m1 в степень m2 по модулю n^2").grid(row=r + 23, column=0, sticky="w")

tk.Label(frame, text="Введите первое число m1:").grid(row=r + 24, column=0, sticky="w")
entry_exponentiation_number1 = tk.Entry(frame, width=width, font=input_font)
entry_exponentiation_number1.grid(row=r + 24, column=1, pady=5)

tk.Label(frame, text="Введите второе число m2:").grid(row=r + 25, column=0, sticky="w")
entry_exponentiation_number2 = tk.Entry(frame, width=width, font=input_font)
entry_exponentiation_number2.grid(row=r + 25, column=1, pady=5)

tk.Label(frame, text="Введите число n:").grid(row=r + 26, column=0, sticky="w")
entry_exponentiation_n = tk.Entry(frame, width=width, font=input_font)
entry_exponentiation_n.grid(row=r + 26, column=1, pady=5)

tk.Label(frame, text="Результат возведения в степень по модулю n^2:").grid(row=r + 27, column=0, sticky="w")
entry_exponentiation_result = tk.Entry(frame, width=width, font=input_font)
entry_exponentiation_result.grid(row=r + 27, column=1, pady=5)

tk.Button(frame, text="Возвести в степень", command=exponentiation).grid(row=r + 28, column=0, columnspan=2)

root.mainloop()




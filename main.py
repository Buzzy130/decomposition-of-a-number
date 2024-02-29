import math
import random
from tkinter import *
from tkinter import messagebox


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def solovay_strassen(n, k=5):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    def jacobi(a, n):
        if a == 0:
            return 0
        if a == 1:
            return 1
        if a % 2 == 0:
            return jacobi(a // 2, n) * ((-1) ** ((n * n - 1) // 8))
        if a >= n:
            return jacobi(a % n, n)
        if a % 4 == 3 and n % 4 == 3:
            return -jacobi(n, a)
        else:
            return jacobi(n, a)

    def check(a, n):
        if pow(a, (n - 1) // 2, n) != jacobi(a, n) % n:
            return False
        return True

    for _ in range(k):
        a = random.randint(2, n - 1)
        if not check(a, n):
            return False
    return True


def lenstra_factorization(n):
    factors = []
    r = 2
    s = 2
    r_star = extended_gcd(r, s)[1] % s
    r_prime = (r_star * n) % s
    i = 0
    max_iterations = 1000

    while i < max_iterations and len(factors) < 2:  # Continue until at least 2 factors are found
        a = (r * r) % n
        b = (r + s) % n
        c = math.gcd(n, abs(r - b))
        if c != 1 and c != n:
            factors.append(c)
            n //= c
        i += 1

    if n > 1:
        factors.append(n)

    return factors


def factorize_non_prime(n):
    factors = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.append(i)
            n //= i
        else:
            i += 1
    if n > 1:
        factors.append(n)
    return factors


def factorize_all(n):
    prime_factors = lenstra_factorization(n)
    all_factors = []

    for factor in prime_factors:
        all_factors.extend(factorize_non_prime(factor))

    return all_factors


def factorize_with_powers(n):
    factors = factorize_all(n)
    factor_powers = {}
    for factor in factors:
        if factor in factor_powers:
            factor_powers[factor] += 1
        else:
            factor_powers[factor] = 1
    return factor_powers







def insert_data_from_file():
    try:
        with open('input.txt', 'r') as file:
            input_data = file.readlines()
            height_tf.insert(0, input_data[0].strip())
    except FileNotFoundError:
        messagebox.showerror('Error', 'File not found')

def calculate_main():
    number = int(height_tf.get())
    result_all_factors = factorize_with_powers(number)

    print("Простые множители числа", number, "методом Ленстры с дополнительным разложением:")
    for factor, power in result_all_factors.items():
        if number == factor and power == 1:
            messagebox.showinfo('hello', f'Число {number} является простым')
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.truncate(0)
                f.write(f'Число {number} является простым')
        else:
            messagebox.showinfo('hello', f'Простые множители числа {number} методом Ленстры с дополнительным разложением: {factor} в степени {power}')
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.truncate(0)
                f.write(f'Простые множители числа {number} методом Ленстры с дополнительным разложением: {factor} в степени {power}')




window = Tk()
window.title('Разложение числа на множетели')
window.geometry('500x300')

frame = Frame(
    window,
    padx=10,
    pady=10
)
frame.pack(expand=True)

height_lb = Label(
    frame,
    text="Введите число"
)
height_lb.grid(row=3, column=1)



height_tf = Entry(
    frame,
)
height_tf.grid(row=3, column=2, pady=5)



cal_btn = Button(
    frame,
    text='Сгенерировать число',
    command=calculate_main
)
cal_btn.grid(row=5, column=2)

cal_btn = Button(
    frame,
    text='Вставить данные из файла',
    command=insert_data_from_file
)
cal_btn.grid(row=6, column=2)

window.mainloop()
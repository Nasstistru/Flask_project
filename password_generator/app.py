from flask import Flask, render_template, request  # Імпорт класу Flask та функцій для рендерингу шаблонів і обробки запитів
from datetime import datetime  # Імпорт модуля для роботи з датами
import random  # Імпорт модуля для генерації випадкових чисел
import string  # Імпорт модуля для роботи з символами та рядками

# Створення екземпляра Flask-додатку
app = Flask(__name__)

# Список популярних паролів, які легко вгадати
popular_passwords = ['123456', 'password', 'qwerty', 'abc123']

# Функція для генерації випадкового пароля
def generate_password(length, use_special):
    chars = string.ascii_letters + string.digits  # Використовуємо букви та цифри як основу для пароля
    if use_special:  # Якщо вибрано опцію спецсимволів
        chars += string.punctuation  # Додаємо спецсимволи до набору символів
    return ''.join(random.choice(chars) for _ in range(length))  # Генеруємо пароль із заданої кількості символів

# Функція для перевірки сили (складності) пароля
def check_password_strength(password):
    length = len(password) >= 8  # Перевірка на достатню довжину пароля (мінімум 8 символів)
    digits = any(char.isdigit() for char in password)  # Перевірка, чи містить пароль хоча б одну цифру
    special = any(char in string.punctuation for char in password)  # Перевірка, чи є спецсимволи

    score = sum([length, digits, special])  # Підрахунок балів за довжину, цифри та спецсимволи
    if score == 3:  # Якщо є всі три умови
        return 'Сильний'  # Пароль сильний
    elif score == 2:  # Якщо є лише дві умови
        return 'Середній'  # Пароль середньої сили
    else:
        return 'Слабкий'  # Якщо умова лише одна, пароль слабкий

# Функція для перевірки, чи є пароль серед популярних
def is_common_password(password):
    return password in popular_passwords  # Повертає True, якщо пароль у списку популярних, інакше False

# Функція для генерації пароля на основі фрази
def generate_phrase_password():
    words = ['apple', 'banana', 'cherry', 'date', 'elephant']  # Список слів для комбінацій
    return '-'.join(random.choice(words) for _ in range(3))  # Створюємо пароль із трьох випадкових слів

# Маршрут для гри в пінг-понг
@app.route('/ping-pong')
def ping_pong():
    return render_template('game.html')  # Відображаємо HTML-шаблон гри

# Маршрут для аналізатора тексту
@app.route('/analizator')
def analizator():
    return render_template('analizator.html')  # Відображаємо HTML-шаблон аналізатора

# Маршрут для сторінки курсу валют
@app.route('/exchange-rates')
def show_exchange_rates():
    return render_template('exchange_rates.html')  # Відображаємо HTML-шаблон курсу валют

# Основний маршрут для генерації пароля
@app.route('/', methods=['GET', 'POST'])
def index():
    password = ''  # Ініціалізація змінної для пароля
    strength = ''  # Ініціалізація змінної для сили пароля
    common_password = False  # Ініціалізація змінної для позначення популярного пароля
    if request.method == 'POST':  # Якщо метод POST
        if 'phrase_password' in request.form:  # Якщо вибрано пароль на основі фрази
            password = generate_phrase_password()  # Генеруємо пароль-фразу
        else:
            length = int(request.form.get('length', 8))  # Отримуємо довжину пароля (8 за замовчуванням)
            use_special = 'special' in request.form  # Чи потрібно додавати спецсимволи
            password = generate_password(length, use_special)  # Генеруємо випадковий пароль

        strength = check_password_strength(password)  # Визначаємо силу пароля
        common_password = is_common_password(password)  # Перевіряємо, чи є пароль серед популярних

    return render_template('index.html', password=password, strength=strength, common_password=common_password)  # Відображаємо HTML-шаблон для головної сторінки

# Маршрут для сторінки калькулятора
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    return render_template('calculator.html')  # Відображаємо HTML-шаблон калькулятора

# Маршрут для розрахунку різниці між датами
@app.route('/date-difference', methods=['GET', 'POST'])
def date_difference():
    if request.method == 'POST':  # Якщо метод POST
        start_date = request.form.get('start_date')  # Отримуємо початкову дату з форми
        end_date = request.form.get('end_date')  # Отримуємо кінцеву дату з форми

        if start_date and end_date:  # Перевірка, що обидві дати задано
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')  # Конвертація початкової дати у формат дати
                end = datetime.strptime(end_date, '%Y-%m-%d')  # Конвертація кінцевої дати у формат дати
                delta = end - start  # Різниця між кінцевою та початковою датами
                years = delta.days // 365  # Визначаємо кількість років
                months = (delta.days % 365) // 30  # Визначаємо кількість місяців
                days = (delta.days % 365) % 30  # Визначаємо кількість днів
                return render_template('date-difference.html', years=years, months=months, days=days)  # Відображаємо шаблон з результатами
            except ValueError:  # Обробка помилки, якщо формат дати некоректний
                return render_template('date-difference.html', error="Invalid date format")  # Відображаємо повідомлення про помилку

    return render_template('date-difference.html', years=None, months=None, days=None)  # Відображаємо шаблон без результатів, якщо метод GET

# Запуск програми у режимі відладки
if __name__ == '__main__':
    app.run(debug=True)

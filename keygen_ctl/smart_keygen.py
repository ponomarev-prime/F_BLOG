import random
import string

def generate_password():
    # Создаем списки символов для каждой категории
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    punctuation = string.punctuation

    # Генерируем случайное количество символов для каждой категории (от 2 до 4)
    upper_count = random.randint(2, 4)
    lower_count = random.randint(2, 4)
    digit_count = random.randint(2, 4)
    punctuation_count = 20 - (upper_count + lower_count + digit_count)  # Общая длина пароля - сумма длин категорий

    # Генерируем символы для каждой категории
    upper_chars = ''.join(random.choice(uppercase_letters) for _ in range(upper_count))
    lower_chars = ''.join(random.choice(lowercase_letters) for _ in range(lower_count))
    digit_chars = ''.join(random.choice(digits) for _ in range(digit_count))
    punctuation_chars = ''.join(random.choice(punctuation) for _ in range(punctuation_count))

    # Собираем пароль
    password = upper_chars + lower_chars + digit_chars + punctuation_chars

    # Перемешиваем символы пароля
    password_list = list(password)
    random.shuffle(password_list)
    shuffled_password = ''.join(password_list)

    return shuffled_password

def insert_dashes(password):
    # Разбиваем пароль на октеты через знак "-"
    octets = [password[i:i+5] for i in range(0, len(password), 5)]
    return '-'.join(octets)

# Пример использования:
generated_password = generate_password()
password_with_dashes = insert_dashes(generated_password)
print(password_with_dashes)

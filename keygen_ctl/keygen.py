import random
import string

def generate_password():
    # Создаем список символов для пароля
    characters = string.ascii_letters + string.digits + string.punctuation

    # Генерируем пароль из 20 символов
    password = ''.join(random.choice(characters) for _ in range(20))

    # Разбиваем пароль на 4 октета через '-'
    password_with_hyphens = '-'.join([password[i:i + 5] for i in range(0, len(password), 5)])

    return password_with_hyphens

# Пример использования:
generated_password = generate_password()
print(generated_password)
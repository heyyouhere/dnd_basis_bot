import random
import string

def generate_unique_codes(prefix="WH", length=9, num_codes=300):
    codes = set()
    while len(codes) < num_codes:
        code = prefix + ''.join(random.choices(string.ascii_uppercase, k=length - len(prefix)))
        codes.add(code)
    return list(codes)

# Генерация 100 уникальных кодов
unique_codes = generate_unique_codes()
unique_codes[:10]  # Выводим первые 10 для примера

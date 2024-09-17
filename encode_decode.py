import random

def decode_kill_counter(encrypted_string):
    if len(encrypted_string) != 9 or (not encrypted_string.startswith('AR') and not encrypted_string.startswith('WH')):
        return (None, None)  # Недопустимый формат строки

    try:
        key = int(encrypted_string[2])
    except ValueError:
        return (None, None)
    
    mapping_table = 'CIYDTFHQXWLGKNPZRVAUEBMJOS'

    def decrypt_digit_pair(encrypted_pair, offset1, offset2):
        try:
            first_char_index = (mapping_table.index(encrypted_pair[0]) - key - offset1 + 26) % 26
            second_char_index = (mapping_table.index(encrypted_pair[1]) - key - offset2 + 26) % 26
        except ValueError:  # Если символ не найден в mapping_table
            return None
        # Проверяем, что оба символа соответствуют одному и тому же числу
        if first_char_index != second_char_index:
            return (None, None)
        return first_char_index

    decrypted_digits = []
    for i in range(3, 9, 2):
        decrypted_digit = decrypt_digit_pair(encrypted_string[i:i+2], 7 if i == 3 else 2 if i == 5 else 3, 3 if i == 3 else 1 if i == 5 else 6)
        if decrypted_digit is None:  # Если дешифровка не удалась
            return (None, None)
        decrypted_digits.append(decrypted_digit)

    # Сборка дешифрованного числа
    decrypted_num = decrypted_digits[0] * 100 + decrypted_digits[1] * 10 + decrypted_digits[2]
    return (decrypted_num, encrypted_string[:2])

def encode_kill_counter(num):
    # По умолчанию шифруем число 80
    prefix = 'AR'
    key = random.randint(0, 9)  # Генерация случайного ключа от 0 до 9

    # Разбиваем число на разряды
    hundreds = num // 100
    tens = (num % 100) // 10
    units = num % 10

    # Таблица сопоставления символов
    mapping_table = 'CIYDTFHQXWLGKNPZRVAUEBMJOS'

    # Шифрование каждого разряда
    encrypted_hundreds = mapping_table[(hundreds + key + 7) % 26] + mapping_table[(hundreds + key + 3) % 26]
    encrypted_tens = mapping_table[(tens + key + 2) % 26] + mapping_table[(tens + key + 1) % 26]
    encrypted_units = mapping_table[(units + key + 3) % 26] + mapping_table[(units + key + 6) % 26]

    # Сборка зашифрованной строки
    code = prefix + str(key) + encrypted_hundreds + encrypted_tens + encrypted_units

    return code

# for _ in range(100):
#     encoded = encode_kill_counter(1)
#     print(encoded)

print(decode_kill_counter('AR8ZFSKZ'))
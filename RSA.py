from copy import copy  # Импортирует функцию для создания копий объектов
from random import randint  # Импортирует функцию для генерации случайных чисел
from math import gcd, trunc, log2, sqrt  # Импортирует математические функции (НОД, округление, логарифм и квадратный корень)

class RSA:
    def __init__(self, conf):
        # Конструктор класса RSA, принимает конфигурацию для настройки ключей

        if (conf['type'] == 'set'):  # Если тип конфигурации 'set', то используем переданные p и q
            self.p = conf['p']
            self.q = conf['q']
        elif (conf['type'] == 'gen'):  # Если тип конфигурации 'gen', то генерируем случайные p и q
            self.p = self.gen_key(conf['min'], conf['max'])  # Генерация первого простого числа p
            self.q = self.gen_key(conf['min'], conf['max'])  # Генерация второго простого числа q

        self.n = self.p * self.q  # Вычисляем модуль n для публичного и приватного ключей
        self.eiler = (self.p - 1) * (self.q - 1)  # Вычисляем функцию Эйлера от n

        if (conf['e'] == 'auto'):  # Если e не задано, генерируем его автоматически
            while True:
                e = randint(3, self.eiler)  # Генерируем случайное число e
                if gcd(e, self.eiler) == 1:  # Проверяем, что e взаимно простое с функцией Эйлера
                    self.e = e  # Если да, сохраняем e
                    break
        else:
            self.e = int(conf['e'])  # Если e задано, то используем его

        self.d = self.evklid(self.e, self.eiler)  # Вычисляем приватный ключ d с помощью алгоритма Евклида
        if (self.d < 0):  # Если d отрицательно, приводим его к положительному виду
            self.d += self.eiler

        self.open_key = {'e': self.e, 'n': self.n}  # Публичный ключ
        self.secret_key = self.d  # Приватный ключ

    def check_easy(self, n):
        n = int(n)
        for a in range(2, n):
            r = self.expo_mod(a, n - 1, n)  # Проверка на простоту с помощью теоремы Ферма
            if r != 1:  # Если результат не равен 1, то число не простое
                return False
        
        return True

    def evklid(self, a, m):
        res = []  # Список для хранения шагов алгоритма Евклида

        i = 0
        while True:
            if (i == 0):
                r = 1  # Начальное значение остатков
                line = {
                    'q': None,  # Целая часть
                    'r': None,  # Остаток
                    'y': None,  # Число для выражения линейного остаточного
                    'x': None,  # Число для вычисления x
                    'm': m,  # Модуль
                    'a': a,  # Число для алгоритма Евклида
                    'y2': 0,  # Начальное значение y2
                    'y1': 1,  # Начальное значение y1
                    'x2': 1,  # Начальное значение x2
                    'x1': 0  # Начальное значение x1
                }
            else:
                q = (res[i - 1]['m'] // res[i - 1]['a'])  # Находим целую часть от деления
                r = (res[i - 1]['m'] % res[i - 1]['a'])  # Остаток от деления
                y = (res[i - 1]['y2'] - q * res[i - 1]['y1'])  # Вычисление y
                x = (res[i - 1]['x2'] - q * res[i - 1]['x1'])  # Вычисление x
                m_n = (res[i - 1]['a'])  # Записываем значение m
                y2 = (res[i - 1]['y1'])  # Обновляем y2
                x2 = (res[i - 1]['x1'])  # Обновляем x2

                line = {
                    'q': q, 'r': r, 'y': y, 'x': x,  # Записываем новые значения
                    'm': m_n, 'a': r, 'y2': y2, 'y1': y, 'x2': x2, 'x1': x
                }

            i += 1  # Увеличиваем индекс для следующего шага
            res.append(copy(line))  # Копируем текущую строку алгоритма

            if (r == 0):  # Если остаток равен нулю, алгоритм завершён
                break

        return res[-1]['y2']  # Возвращаем последний y, это и есть результат Евклида

    def create_blocks(self, content, size):
        while (len(content) % size != 0):  # Пока длина контента не кратна размеру блока, добавляем нули
            content = '0' + content  # Добавляем ведущие нули для выравнивания

        blocks = []  # Список для хранения блоков
        for i in range(0, len(content), size):  # Разбиваем контент на блоки размером size
            block = content[i:i+size]  # Берём блок
            blocks.append(block)  # Добавляем блок в список
        
        return blocks

    def expo_mod(self, a, k, n):
        b = 1  # Начальное значение b
        for i in range(k):  # Повторяем k раз
            b *= a  # Умножаем b на a
            b %= n  # Берём остаток от деления на n

        return b  # Возвращаем результат возведения в степень по модулю

    def gen_key(self, min, max):
        while True:
            num = randint(min, max)  # Генерация случайного числа в диапазоне от min до max
            check = True
            if (num % 2 != 0):  # Если число нечётное
                for dell in range(int(sqrt(num)) + 1, 2, -2):  # Пробуем делить на нечётные числа до sqrt(num)
                    if (num % dell == 0):  # Если нашли делитель, значит число составное
                        check = False
                        break
            
            if check:  # Если число простое, возвращаем его
                return num

    def encrypt(self, filepath):
        size = 4  # Размер блока определяется логарифмом от n

        file = open(filepath, 'rb')  # Открываем файл для чтения в бинарном режиме
        content = file.read()  # Читаем содержимое файла
        file.close()  # Закрываем файл

        bin_content = ''.join(f'{b:08b}' for b in content)  # Преобразуем содержимое в бинарный формат
        blocks = self.create_blocks(bin_content, size)  # Разбиваем на блоки
        print(blocks)
        result = []  # Список для хранения зашифрованных блоков
        for block in blocks:  # Для каждого блока
            block_dec = int(block, 2)  # Преобразуем бинарный блок в десятичное число
            c = self.expo_mod(block_dec, self.e, self.n)  # Шифруем блок с использованием публичного ключа
            c1 = copy(bin(c)[2:])  # Переводим результат в бинарный формат
            while (len(c1) < (size + 1)):  # Добавляем ведущие нули, если необходимо
                c1 = '0' + c1
            result.append(c1)  # Добавляем зашифрованный блок в результат

        print(result)
        result = ''.join(result)  # Собираем все блоки в одну строку

        while (len(result) % 8 != 0):  # Выравниваем длину строки до кратности 8
            result = '0' + result

        res = b''  # Список для хранения байтового результата
        for i in range(0, len(result), 8):  # Разбиваем строку на байты
            byte = result[i:i+8]  # Берём 8 бит
            res += int(byte, 2).to_bytes()  # Преобразуем байт в число и добавляем в результат
            
        file = open((filepath) + '_en', 'wb')  # Открываем новый файл для записи зашифрованных данных
        file.write(res)  # Записываем зашифрованное содержимое
        file.close()

    def decrypt(self, filepath):
        size = 4  # Размер блока определяется логарифмом от n

        file = open(filepath, 'rb')  # Открываем зашифрованный файл
        content = file.read()  # Читаем содержимое файла
        file.close()  # Закрываем файл

        bin_content = ''.join(f'{b:08b}' for b in content)  # Преобразуем содержимое в бинарный формат
        
        while len(bin_content) % (size + 1) != 0:  # Выравниваем длину до кратности размеру блока
            bin_content = bin_content[1:]  # Удаляем лишний бит, если необходимо
        
        blocks = self.create_blocks(bin_content, size + 1)  # Разбиваем на блоки

        result = []  # Список для хранения расшифрованных блоков
        for block in blocks:  # Для каждого блока
            block_dec = int(block, 2)  # Преобразуем блок в десятичное число
            c = self.expo_mod(block_dec, self.d, self.n)  # Расшифровываем блок с использованием приватного ключа
            c1 = copy(bin(c)[2:])  # Переводим результат в бинарный формат
            while (len(c1) < size):  # Добавляем ведущие нули, если необходимо
                c1 = '0' + c1
            result.append(c1)  # Добавляем расшифрованный блок в результат
        
        result = ''.join(result)  # Собираем все блоки в одну строку

        while (len(result) % 8 != 0):  # Убираем лишние нули в конце
            result = result[1:]

        res = b''  # Список для хранения байтового результата
        for i in range(0, len(result), 8):  # Разбиваем строку на байты
            byte = result[i:i+8]  # Берём 8 бит
            res += int(byte, 2).to_bytes()  # Преобразуем байт в число и добавляем в результат
    
        file = open('de_' + ((filepath).replace('_en', '')), 'wb')  # Открываем новый файл для записи расшифрованных данных
        file.write(res)  # Записываем расшифрованное содержимое
        file.close()

# Конфигурация для теста
conf = {
    'type': 'set',  # Тип конфигурации: используем заранее заданные p и q
    'p': 17,  # Первое простое число
    'q': 29,  # Второе простое число
    'e': '3'  # Публичный ключ e
}

a = RSA(conf)  # Создание экземпляра класса RSA с конфигурацией
print(a.__dict__)  # Выводим параметры объекта RSA
a.encrypt('first.txt')  # Шифруем файл first.txt
a.decrypt('first.txt_en')  # Расшифровываем файл first.txt_en

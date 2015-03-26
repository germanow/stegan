"""Реализация стеганографии"""


import lsb

def interface():
	while True:
		print("--Главное меню--")
		print("1)Закодировать сообщение")
		print("2)Декодировать сообщение")
		print("3)Выход")
		choice = input("Введите число:")
		
		if choice == '1':
			print()
			stegan_encode()
		elif choice == '2':
			print()
			stegan_decode()
		elif choice == '3' or choice == 'exit':
			print("Выход...")
			break
		else:
			print("Некорректное значение")

def stegan_encode():
	print("__Кодирование сообщения__")
	print("Для выхода напишите exit")
	while True:
		source = input("Введите имя картинки формата .bmp или укажите путь к ней\n")
		if source == 'exit':
			return 0
		elif source[len(source)-4:] != '.bmp':
			source += '.bmp'
		try:
			with open(source,'rb') as image:
				container = image.read()
		except:
			print("Некорректное имя или путь к файлу")
			continue
		if container[:2].decode() != 'BM':
			print("Формат не поддерживается")
			continue
		start = smeshenie_izobrazheniya(container)
		head_container = container[:start]
		body_container = container[start:]
		message = input("Сообщение:")
		if not message:
			print("Некорректное сообщение")
			continue
		try:
			body_container = lsb.message_encode(body_container, message)
		except ValueError:
			print("Сообщение не умещается")
			continue
		container = head_container + body_container
		print("Выполняется кодирование подождите...")
		with open(source,'wb') as image:
			image.write(container)
		print("Сообщение закодировано")
		input("Для продолжения нажми Enter")
		break
	print()


def stegan_decode():
	print("__Декодирование сообщения__")
	print("Для выхода напишите exit")
	while True:
		source = input("Введите имя картинки формата .bmp или укажите путь к ней\n")
		if source == 'exit':
			return 0
		elif source[len(source)-4:] != '.bmp':
			source += '.bmp'
		try:
			with open(source,'rb') as image:
				container = image.read()
		except:
			print("Некорректное имя или путь к файлу")
			continue
		if container[:2].decode() != 'BM':
			print("Формат не поддерживается")
			continue
		start = smeshenie_izobrazheniya(container)
		body_container = container[start:]
		print("Идёт декодировани подождите...")
		message = lsb.message_decode(body_container)
		print("--"*5)
		print(message)
		print("--"*5)
		input("Для продолжения нажми Enter")
		break
	print()

def smeshenie_izobrazheniya(container):
	#Вычисляет смещения изображения от начала файла
	#Принимает строку байтов
	image_start = container[10:14]
	start = 0
	for (razryad, byte) in enumerate(image_start):
		if razryad == 0:
			start += byte
		else:
			start += byte*(16**(razryad+1))
	return start



interface()

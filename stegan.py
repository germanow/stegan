"""Реализация стеганографии"""


import lsb

def interface():
	while True:
		print("--Главное меню--")
		print("1)Закодировать сообщение")
		print("2)Закодировать сообщение из текстового файла(alpha version)")
		print("3)Декодировать сообщение")
		print("4)Выход")
		choice = input("Введите число:")
		if choice == '1':
			print()
			stegan_encode('notfile')
		if choice == '2':
			print()
			stegan_encode('file')
		elif choice == '3':
			print()
			stegan_decode()
		elif choice == '4' or choice == 'exit':
			print("Выход...")
			break
		else:
			print("Некорректное значение")

def stegan_encode(choice='notfile'):
	print("__Кодирование сообщения__")
	print("Для выхода напишите exit")
	while True:
		img_source = input("Введите имя картинки формата .bmp или укажите путь к ней\n")
		#Проверка правильности img_source
		if img_source == 'exit':
			return 0
		elif len(img_source) <= 4:
				img_source += '.bmp'
		elif img_source[-4] != '.':
			img_source += '.bmp'
		try:
			with open(img_source,'rb') as image:
				container = image.read()
			start = smeshenie_izobrazheniya(container)#Здесь же проверка формата
		except ValueError:
			print('Формат не поддерживается')
			continue
		except FileNotFoundError:
			print("Некорректное имя или путь к файлу")
			continue
		head_container = container[:start]#Заголовочные данные изображения
		body_container = container[start:]
		if choice == 'notfile':
			message = input("Сообщение:")
		elif choice == 'file':
			txt_source = input("Введите имя текстового файла(.txt) или укажите путь к нему\n")
			#Проверка правильности txt_source
			if txt_source == 'exit':
				return 0
			elif len(txt_source) <= 4:
				txt_source += '.txt'
			elif txt_source[-4] != '.':
				txt_source += '.txt'
			elif txt_source[-4:] != '.txt':
				print("Поддерживается только формат .txt")
			try:
				with open(txt_source,'r') as text:
					message = text.read()
			except FileNotFoundError:
				print("Некорректное имя или путь к файлу")
				continue
		try:
			print("Выполняется кодирование подождите...")
			body_container = lsb.message_encode(body_container, message)
		except RuntimeError:
			print("Сообщение не умещается")
			continue
		except ValueError:
			print("Некорректное сообщение")
			continue
		container = head_container + body_container
		try:
			with open(img_source,'wb') as image:
				image.write(container)
		except FileNotFoundError:
			print("Oopss, файл куда-то пропал!")
			continue
		print("Сообщение закодировано")
		input("Для продолжения нажми Enter")
		break
	print()


def stegan_decode():
	print("__Декодирование сообщения__")
	print("Для выхода напишите exit")
	while True:
		source = input("Введите имя картинки формата .bmp или укажите путь к ней\n")
		#Проверка правильности source
		if source == 'exit':
			return 0
		elif len(source) <= 4:
			source += '.bmp'
		elif source[-4] != '.':
			source += '.bmp'
		try:
			with open(source,'rb') as image:
				container = image.read()
			start = smeshenie_izobrazheniya(container)#Здесь же проверка на формат
		except ValueError:
			print('Формат не поддерживается')
			continue
		except FileNotFoundError:
			print("Некорректное имя или путь к файлу")
			continue
		body_container = container[start:]
		print("Идёт декодированиe подождите...")
		message = lsb.message_decode(body_container)
		print("--"*20)
		try:
			print(message)
		except:
			print('Сообщение не найдено')
		print("--"*20)
		input("Для продолжения нажми Enter")
		break
	print()

def smeshenie_izobrazheniya(container):
	#Вычисляет смещения изображения от начала файла
	#Принимает строку байтов
	
	if container[:2].decode() == 'BM':#Для формата .bmp
		image_start = container[10:14]
		start = 0
		for (razryad, byte) in enumerate(image_start):
			if razryad == 0:
				start += byte
			else:
				start += byte*(16**(razryad+1))
		return start
	else:
		raise ValueError('Формат не поддерживается')


interface()
input("Press Enter")

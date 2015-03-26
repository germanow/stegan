"""Модуль для кодирования сообщения(utf-8)  
В последних 2 битах последовательности байтов(имеется виду строка b'...')
Используется только стандартная библиотека
"""


def message_encode(container, text):
	#Функция кодирования сообщеня
	#Принимает строку байтов и строку сообщения
	#Записывает в последние 2 бита сообщение(utf-8)
	#Возвращает строку байтов с закодированым сообщением
	
	def add_to_byte(byte,bits):
		#Добавляет в конец байта 2 бита bits(str)
		
		byte = str(bin(byte))
		#Увеличиваем размер строки до 10
		byte = byte.replace('0b','0b'+'0'*(10-len(byte)))
		byte = byte[:-2]+bits
		return int(eval(byte))
	
	def message_to_list_of_bits(text):
		#Превращает сообщение в список содержащий строки из 2 битов
		
		text = str(text).encode('utf-8')
		message = ''
		for byte in text:
			byte = str(bin(byte))
			byte = byte.replace('0b','0'*(10-len(byte)))
			message+=byte
			
		list = []
		for i in range(0, len(message), 2):
			list.append(message[i]+message[i+1])
			
		#0xff в utf-8 обозначает символ закодированный больше чем 6 байтами
		end_mark = bin(0xff)
		end_mark = end_mark[2:]
		end = []
		for i in range(0,len(end_mark),2):
			end.append(end_mark[i]+end_mark[i+1])
			
		list.extend(end)
		return list
	
	#Начало работы функции
	if not container or not text:
		raise ValueError("Пустые аргументы")
	elif type(container) != bytes:
		raise TypeError("Контейнер должен быть строкой байтов")
	
	container = bytearray(container)
	code = message_to_list_of_bits(text)
	
	if len(container) < len(code):
		raise ValueError("Сообщение не умещается")
		
	for i in range(0,len(code)):
		container[i] = add_to_byte(container[i],code[i])
	return bytes(container)


def message_decode(text_container):
	#Функция декодирования сообщения
	#Принимает строку байтов и извлекает сообщение 
	#из 2 последних битов в байтах
	
	if not text_container:
		raise ValueError("Пустой контейнер")
	elif type(text_container) != bytes:
		raise TypeError("Контейнер должен быть строкой байтов")
	
	container = ''
	for byte in text_container:
		byte = str(bin(byte))
		byte = byte.replace('0b','0b'+'0'*(10-len(byte)))
		container += byte

	message_list = []
	for i in range(0, len(container), 40):
		byte = (container[i+8:i+10] + container[i+18:i+20] +
						container[i+28:i+30] + container[i+38:i+40])
		byte = eval('0b'+byte)
		#Ищем end_mark 0xff
		if byte == 255:break
		message_list.append(byte)
	else:
		return "Сообщение не найдено"
		
	message = bytearray(message_list).decode('utf-8')
	return message

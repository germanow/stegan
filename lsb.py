"""Модуль для кодирования и декодирования сообщения(utf-8) 
В/из последних 2 битах последовательности байтов(имеется виду строка b'...')
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
	
	if (not container) or (not text):
		raise ValueError("Пустые аргументы")
	
	container = bytearray(container)
	code = message_to_list_of_bits(text)
	
	if len(container) < len(code):
		raise RuntimeError("Сообщение не умещается")
		
	for i in range(0,len(code)):
		container[i] = add_to_byte(container[i],code[i])
	return bytes(container)


def message_decode(text_container):#Снова поменять
	#Функция декодирования сообщения
	#Принимает строку байтов и извлекает сообщение 
	#из 2 последних битов в байтах
	
	def recive_byte(container,number):
	#Извлекает байт под номером = number из контейнера
	
		i = number*40
		byte = (container[i+8:i+10] + container[i+18:i+20] +
						container[i+28:i+30] + container[i+38:i+40])
		byte = eval('0b'+byte)
		if byte == 255:#Ищем end_mark
			raise RuntimeError
		return byte
		
	def recive_container(text_container,number):
	#Извлекает контейнер с зашифрованым байтом под номером = number
	#В виде обычной строки с двоичным представлением байтов(длиной 10)

		number = number*4
		container = ''
		for i in range(number,number+4):
			byte = str(bin(text_container[i]))
			byte = byte.replace('0b','0b'+'0'*(10-len(byte)))
			container += byte
		return container
	
	if not text_container:
		raise ValueError("Пустой контейнер")
	i = 0
	container = ''
	message = ''
	while i < (len(text_container)/4):
		try:
			container += recive_container(text_container,i)#Получили часть контейнера
			byte = recive_byte(container,i)#Получили закодированный байт из контейнера
			if 0x00 <= byte <= 0x7f:#Однобайтовый символ
				message += bytearray([byte]).decode()
				i+=1
			elif 0xc0 <= byte <= 0xdf:#Двухбайтовый символ
				message_list = []
				message_list.append(byte)
				i+=1
				container += recive_container(text_container,i)
				byte = recive_byte(container,i)
				message_list.append(byte)
				i+=1
				message += bytearray(message_list).decode()
			elif 0xe0 <= byte <= 0xef:#Трёхбайтовый символ
				message_list = []
				for j in range(i,i+3):
					if j == i:
						byte = recive_byte(container,j)
						message_list.append(byte)
						continue
					container += recive_container(text_container,j)
					byte = recive_byte(container,j)
					message_list.append(byte)
				i+=3
				message += bytearray(message_list).decode()
			elif 0xf0 <= byte <= 0xf7:#Четырёхбайтовый символ
				message_list = []
				for j in range(i,i+4):
					if j == i:
						byte = recive_byte(container,j)
						message_list.append(byte)
						continue
					container += recive_container(text_container,j)
					byte = recive_byte(container,j)
					message_list.append(byte)
				i+=4
				message += bytearray(message_list).decode()
			else:
				return "Сообщение не найдено"
		except RuntimeError:#Нашли end_mark
			break
		except UnicodeDecodeError:
			return "Сообщение не найдено"
	else:
		return "Сообщение не найдено"
	return message

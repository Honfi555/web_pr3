"""Файл для настройки логирования."""
import os
import sys
import atexit
import logging
from logging.handlers import RotatingFileHandler


def create_intermediate_dirs(path: str) -> None:
	"""
	Создаёт всё директории в указанном пути.
	:param path: Путь для создания папок, может оканчиваться на файл.
	"""
	try:
		if not path.endswith(os.sep):
			dir_path = os.path.dirname(path)
		else:
			dir_path = path
		os.makedirs(dir_path, exist_ok=True)
	except Exception as e:
		print(f"Ошибка при создании директорий: {e}")


def configure_logs_on_file(logs_path: str = "logs/app.log") -> None:
	"""
	Настраивает вывод и сохранение логов в файл.
	:param logs_path: Путь к файлу с логами.
	"""

	create_intermediate_dirs(path=logs_path)
	# Настройка RotatingFileHandler для файла логов с максимальным размером 50 МБ и 3 резервными копиями
	log_handler = RotatingFileHandler(
	logs_path,
	maxBytes=50 * 1024 * 1024,  # 50 МБ
	backupCount=3,
	encoding='utf-8'
	)

	# Форматирование логов
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
	log_handler.setFormatter(formatter)

	# Настраиваем логер
	logging.getLogger().setLevel(logging.INFO)
	logging.getLogger().addHandler(log_handler)

	log_file = open(logs_path, 'a', encoding='utf-8')
	sys.stdout = log_file
	sys.stderr = log_file
	atexit.register(log_file.close)


def configure_logs(logs_path: str = "logs/app.log", log_level: int = logging.INFO) -> None:
	"""
	Настраивает вывод и сохранение логов в файл и вывод в консоль.
	:param log_level: Урень логирования, стандартное значение INFO.
	:param logs_path: Путь к файлу с логами.
	"""

	# Получаем корневой логгер
	logger = logging.getLogger()
	logger.setLevel(log_level)

	# Проверяем, есть ли уже обработчики, чтобы избежать добавления дубликатов
	if not logger.handlers:
		create_intermediate_dirs(path=logs_path)
		# Настройка RotatingFileHandler для файла логов с максимальным размером 50 МБ и 3 резервными копиями
		file_handler = RotatingFileHandler(
			logs_path,
			maxBytes=50 * 1024 * 1024,  # 50 МБ
			backupCount=3,
			encoding='utf-8'
		)
		file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
		file_handler.setFormatter(file_formatter)
		logger.addHandler(file_handler)

		# Добавляем обработчик для консоли
		console_handler = logging.StreamHandler(sys.stdout)
		console_handler.setLevel(log_level)
		console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
		console_handler.setFormatter(console_formatter)
		logger.addHandler(console_handler)

		# Перенаправляем stdout и stderr в файл
		try:
			log_file = open(logs_path, 'a', encoding='utf-8')
			sys.stdout = log_file
			sys.stderr = log_file
			atexit.register(log_file.close)
		except Exception as e:
			logger.error("Не удалось перенаправить stdout/stderr: %s", e)


if __name__ == "__main__":
	configure_logs()
	logging.info("Это информационное сообщение")
	logging.warning("Это предупреждающее сообщение")
	logging.error("Это сообщение об ошибке")
	print("Это сообщение через print()")

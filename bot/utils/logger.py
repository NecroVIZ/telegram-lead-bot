import logging
import os
from logging.handlers import RotatingFileHandler

# Создаем папку для логов, если её нет
if not os.path.exists('logs'):
    os.makedirs('logs')

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ротирующий файловый хендлер (максимум 5MB, 3 файла)
    file_handler = RotatingFileHandler(
        'logs/bot.log', 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Консольный хендлер
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
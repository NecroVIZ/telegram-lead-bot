import time
from typing import Dict

# Простой анти-спам: ограничение 3 заявки в час
user_requests: Dict[int, list] = {}

def is_spam(user_id: int) -> bool:
    current_time = time.time()
    hour_ago = current_time - 3600  # 1 час назад
    
    # Очищаем старые запросы
    if user_id in user_requests:
        user_requests[user_id] = [
            req_time for req_time in user_requests[user_id] 
            if req_time > hour_ago
        ]
    else:
        user_requests[user_id] = []
    
    # Проверяем лимит
    if len(user_requests[user_id]) >= 3:
        return True
    
    # Добавляем текущий запрос
    user_requests[user_id].append(current_time)
    return False

def get_remaining_requests(user_id: int) -> int:
    current_time = time.time()
    hour_ago = current_time - 3600
    
    if user_id in user_requests:
        user_requests[user_id] = [
            req_time for req_time in user_requests[user_id] 
            if req_time > hour_ago
        ]
        return 3 - len(user_requests[user_id])
    return 3
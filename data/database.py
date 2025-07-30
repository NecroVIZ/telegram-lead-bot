# data/database.py
import gspread
from google.oauth2.service_account import Credentials
from bot.config import GOOGLE_CREDS_PATH
import datetime
import time
from bot.utils.logger import get_logger

logger = get_logger(__name__)

def get_sheet():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(GOOGLE_CREDS_PATH, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("Заявки").sheet1
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        logger.error("Таблица 'Заявки' не найдена. Проверьте название таблицы.")
        return None
    except Exception as e:
        logger.error(f"Ошибка подключения к Google Sheets: {e}")
        return None

def save_lead(name, phone, message):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            sheet = get_sheet()
            if not sheet:
                return False
                
            # Добавляем заголовки, если таблица пустая
            if len(sheet.get_all_values()) == 0:
                sheet.append_row(["Имя", "Телефон", "Сообщение", "Дата"])
            
            # Добавляем данные
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([name, phone, message, timestamp])
            return True
        except gspread.exceptions.APIError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Экспоненциальная задержка
                logger.warning(f"API ошибка, повторная попытка через {wait_time} секунд...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"API ошибка после {max_retries} попыток: {e}")
                return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка при сохранении в Google Sheets: {e}")
            return False
    return False

def get_stats():
    try:
        sheet = get_sheet()
        if not sheet:
            return {"total_leads": 0, "today_leads": 0, "week_leads": 0}
        
        all_data = sheet.get_all_records()
        total_leads = len(all_data)
        
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        
        today_leads = 0
        week_leads = 0
        
        for row in all_data:  # Исправлено: было "for row in all_"
            if 'Дата' in row:
                try:
                    date_str = row['Дата']
                    # Парсим дату в формате "YYYY-MM-DD HH:MM:SS"
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    if date_obj == today:
                        today_leads += 1
                    if date_obj >= week_ago:
                        week_leads += 1
                except:
                    pass
        
        return {
            "total_leads": total_leads,
            "today_leads": today_leads,
            "week_leads": week_leads
        }
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        return {"total_leads": 0, "today_leads": 0, "week_leads": 0}
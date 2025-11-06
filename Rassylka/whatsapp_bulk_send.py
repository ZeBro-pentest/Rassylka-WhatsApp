#!/usr/bin/env python3
"""
whatsapp_bulk_send_by_number.py
Отправляет персональные сообщения по номерам телефонов через WhatsApp Web.
Данные берутся из CSV (phone,message).
"""

import time
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# =============== НАСТРОЙКИ ===============

CSV_PATH = "contacts.csv"  # путь к CSV с номерами и сообщениями
CHROME_USER_DATA = "Путь_к_гугл-хром_профилю"

# пример для macOS:
# CHROME_USER_DATA = "/Users/IVAN/Library/Application Support/Google/Chrome/Default"

# пример для Windows:
# CHROME_USER_DATA = "C:\\Users\\IVAN\\AppData\\Local\\Google\\Chrome\\User Data"

# пример для Linux:
# CHROME_USER_DATA = "/home/IVAN/.config/google-chrome/Default"

DELAY_BETWEEN_MESSAGES = 3  # секунд между отправками
WAIT_FOR_CHAT = 15  # ожидание загрузки чата (в секундах)

# ========================================

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def wait_for_element(driver, selectors, timeout=15):
    wait = WebDriverWait(driver, timeout)
    last_error = None
    for by, sel in selectors:
        try:
            return wait.until(EC.presence_of_element_located((by, sel)))
        except Exception as e:
            last_error = e
    raise last_error

def send_message_by_number(driver, phone_number, message_text):
    print(f"\n➡️ Отправляем сообщение на номер: {phone_number}")

    encoded_text = urllib.parse.quote(message_text)
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_text}"
    driver.get(url)

    try:
        message_box = WebDriverWait(driver, WAIT_FOR_CHAT).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )
    except:
        print(f"❌ Не удалось открыть чат с {phone_number}")
        return

    time.sleep(1)
    message_box.send_keys(Keys.ENTER)
    print(f"✅ Сообщение отправлено: {message_text}")

def main():
    print("🚀 Запускаем WhatsApp Web...")
    driver = create_driver()
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 60)

    # Проверяем авторизацию
    try:
        wait.until(EC.presence_of_element_located((By.ID, "pane-side")))
        print("✅ WhatsApp Web загружен и авторизация выполнена.")
    except:
        print("⏳ Подожди, пока отсканируешь QR-код в телефоне...")
        wait.until(EC.presence_of_element_located((By.ID, "pane-side")))

    # Загружаем CSV
    contacts = pd.read_csv(CSV_PATH)
    print(f"\n📋 Загружено {len(contacts)} номеров из {CSV_PATH}")

    for _, row in contacts.iterrows():
        phone = str(row["phone"]).strip().replace("+", "")
        message = str(row["message"]).strip()
        send_message_by_number(driver, phone, message)
        time.sleep(DELAY_BETWEEN_MESSAGES)

    print("\n✅ Все сообщения отправлены!")
    # driver.quit()

if __name__ == "__main__":
    main()

# main.py
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Configurar para que funcione sin abrir ventana (headless)
options = Options()
options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = r'https://tramites.munistgo.cl/reservahoralicencia/?__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=DRyytXmkvqsRNHqLnD77wUFvoWgwNPDen18LuIUw8EHQgzunfh8Ng7MZTtm%2FOzPNbkb7FsU8DH33LIdBWNp4KdRC47t2gEkj%2Bqn8YhlbrcvtN9Y0x8c3pTR9l29AXYhYpGuO6h%2FWpVy14zXpo4h9PQ%3D%3D&__VIEWSTATEGENERATOR=341EAED8&__EVENTVALIDATION=dqb2ZBLIMlA5Gj4vvxxIpK%2BYsqL1sVGDaIV%2FNemQNn7IWj1dQ8a%2BnwgXKq%2FRMg2EsrjHfCiL4POTlsOIivKEJkhUWvZkrPLZ4YW5sRgq%2FBCaj4DPai9TSwj8C7dNu2PwMxHb24WHhJr9%2BPx9hDmYSg%3D%3D&txtLogin='
driver.get(url)

rut_input = driver.find_element(By.ID, "txtLogin")
rut_input.clear()
rut_input.send_keys("19394171-0")

boton_ing = driver.find_element(By.ID, 'imgIdentificar')
boton_ing.click()
time.sleep(2)

boton_reserva = driver.find_element(By.ID, 'dgGrilla_btIngresar_0')
boton_reserva.click()
time.sleep(2)

driver.save_screenshot('Resultado.png')
driver.quit()

# Lee variables de entorno para usar con Telegram
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
foto_path = "Resultado.png"
url_api = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

with open(foto_path, "rb") as photo:
    files = {"photo": photo}
    data = {"chat_id": chat_id, "caption": "Aquí está el resultado del scraping"}
    r = requests.post(url_api, files=files, data=data)

print("Envío a Telegram:", r.status_code, r.text)

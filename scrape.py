import time, csv
import os
from bs4 import BeautifulSoup

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



# Configurar Selenium para conectarse a la sesión de Chrome existente
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Se conecta al puerto 9222

# Define la ubicación del ChromeDriver utilizando 'Service'
chrome_driver_path = 'C:/selenium/chromedriver.exe'  # Reemplaza con la ruta real de tu chromedriver
service = Service(chrome_driver_path)
# Inicializa el WebDriver con el servicio y las opciones
driver = webdriver.Chrome(service=service, options=chrome_options)
# Espera a que cargue la página
wait = WebDriverWait(driver, 600)

def output_to_csv(data, filename):
    with open(filename, "w", newline='') as f:  # Cambiado para compatibilidad con Python 3
        writer = csv.writer(f)
        writer.writerows(data)

def locate_chat(name):
    """Buscar el chat con el nombre dado en WhatsApp Web y hacer clic en él."""
    x_arg = '//span[contains(@title, '+ '"' +name + '"'+ ')]'
    print(x_arg)
    person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    print(person_title)
    person_title.click()

def scroll_to_top():
    """Desplazarse hacia la parte superior del chat abierto en WhatsApp Web."""
    chats = driver.find_elements(By.CLASS_NAME, "vW7d1")
    third_chat = chats[2].get_attribute('innerHTML')

    while 'Messages you send' not in third_chat:
        print("Number of chats before scrolling: ", len(chats))
        top = chats[0]
        driver.execute_script("arguments[0].scrollIntoView(true);", top)
        time.sleep(2)
        chats = driver.find_elements(By.CLASS_NAME, "vW7d1")
        third_chat = chats[2].get_attribute('innerHTML')

    return chats

def process_chat(chat):
    """Analizar el HTML del mensaje de chat para extraer los datos."""
    message_type = ""
    chat_text = ""

    check_image = chat.find('div', class_='_3v3PK')
    check_video = chat.find('div', class_='_1opHa video-thumb')
    check_admin = '_3rjxZ' in chat['class']
    check_deleted_msg = chat.find('div', class_='_1fkCN')
    check_document = chat.find('a', class_='_1vKRe')

    check_waiting_message = chat.find('div', class_='_3zb-j ZhF0n _18dOq')
    check_gif = chat.find('span', {'data-icon':'media-gif'})

    if check_video:
        message_type = "video"
    elif check_image:
        message_type = "image"
        chat_text = chat.find('span', class_='selectable-text invisible-space copyable-text').text if chat.find('span', class_='selectable-text invisible-space copyable-text') else ""
    elif check_admin:
        message_type = "admin"
        chat_text = chat.text
    elif check_deleted_msg:
        message_type = "deleted_message"
    elif check_document:
        message_type = "document"
    elif check_waiting_message:
        chat_text = check_waiting_message.text
    elif check_gif:
        message_type = 'gif'
    else:
        message_type = "text"
        chat_text = chat.find('div', class_='copyable-text').text if chat.find('div', class_='copyable-text') else "NA"

    sender_number = chat.find('span', class_="RZ7GO").text if chat.find('span', class_="RZ7GO") else "NA"
    chat_time = chat.find('span', class_='_3EFt_').text if chat.find('span', class_='_3EFt_') else "NA"
    chat_datetime = chat.find('div', class_='copyable-text')['data-pre-plain-text'] if chat.find('div', class_='copyable-text') else "NA"
    sender_name = chat.find('span', class_='_3Ye_R _1wjpf _1OmDL').text if chat.find('span', class_='_3Ye_R _1wjpf _1OmDL') else "NA"

    urls = [a['href'] for a in chat.find_all('a')] if chat.find_all('a') else []

    return [chat_text, message_type, sender_number, chat_time, chat_datetime, sender_name, str(urls)]

def run_scraper():
    locate_chat("Buenos Aires Ciudad")  # Localiza el chat de "Buenos Aires Ciudad"

    group_data = pd.read_csv('group_details.csv', header=None)
    group_id = len(group_data) + 1

    group_data = group_data.values.tolist()

    message_window = driver.find_element(By.ID, 'main')
    data = message_window.get_attribute('innerHTML')

    raw_html_file = open("raw_" + str(group_id) + ".html", "w", encoding='utf-8')
    raw_html_file.write(data)
    raw_html_file.close()

    soup = BeautifulSoup(data, "html.parser")
    chats = soup.find_all('div', class_='vW7d1')
    print("chats...", len(chats))

    group_name = BeautifulSoup(driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div').get_attribute('innerHTML'), 'html.parser').find('span')['title']
    driver.find_element(By.CLASS_NAME, '_1WBXd').click()
    group_created_at = driver.find_element(By.CLASS_NAME, 'Cpiae').get_attribute('innerHTML')
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div[3]/span/div/span/div/header/div/div[1]/button/span').click()

    group_details = [group_name, group_created_at, group_id]
    print(group_details)

    group_data.append(group_details)
    output_to_csv(group_data, 'group_details.csv')

    chat_data = []
    for i in chats:
        parsed_chat = process_chat(i)
        chat_data.append([group_id, group_name, group_created_at] + parsed_chat)

    print("chat_data ready...")
    output_to_csv(chat_data, 'scraped_data/' + str(group_id) +  '.csv')
    print("process complete: ", str(group_id) +  '.csv')

run_scraper()

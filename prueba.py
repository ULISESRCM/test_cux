from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Configuración de WebDriver
url = "https://web.whatsapp.com/"
driver = webdriver.Chrome()

# Abre WhatsApp Web
driver.get(url)

# Espera a que la página se cargue completamente
wait = WebDriverWait(driver, 600)  # Espera hasta 10 minutos si es necesario

# Espera a que aparezca la caja de texto, lo que indica que WhatsApp está cargado
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))

print("WhatsApp Web está listo.")

def locate_chat(name):
    """Buscar el chat con el nombre dado en WhatsApp Web y hacer clic en él."""
    try:
        x_arg = f'//span[contains(@title, "{name}")]'
        print(f"Buscando el chat: {x_arg}")
        # Espera hasta que el chat específico esté visible en la lista de chats
        person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        print(f"Chat encontrado: {person_title.text}")
        person_title.click()  # Clic en el chat para abrirlo
    except Exception as e:
        print(f"Error al localizar el chat {name}: {e}")

# Localizar el chat "Buenos Aires Ciudad"
locate_chat("Buenos Aires Ciudad")

# Esperar unos segundos para que los mensajes se carguen
time.sleep(5)
print("Esperando a que los mensajes se carguen...")

def extract_todays_messages():
    """Extrae los mensajes del chat actualmente abierto que fueron enviados hoy."""
    try:
        # Encontrar el bloque "HOY" en el chat
        today_section = driver.find_element(By.XPATH, '//span[contains(text(), "HOY")]')
        print("Sección 'HOY' encontrada.")

        # Obtener todos los mensajes después de la sección "HOY"
        messages_after_today = today_section.find_elements(By.XPATH, './/following::div[contains(@class, "message-in") or contains(@class, "message-out")]')

        print(f"Se encontraron {len(messages_after_today)} mensajes después de 'HOY'.")

        # Iterar a través de los mensajes encontrados
        for message in messages_after_today:
            try:
                # Extraer el contenido del mensaje
                message_text = message.find_element(By.XPATH, './/span[contains(@class, "selectable-text copyable-text")]')
                message_time = message.find_element(By.XPATH, './/span[@class="_3EFt_"]').text
                
                if message_text:
                    print(f"[{message_time}] {message_text.text}")
            except Exception as e:
                print(f"Error al extraer el mensaje: {e}")
    except Exception as e:
        print(f"Error al extraer mensajes de hoy: {e}")

# Llamar a la función para extraer mensajes de hoy
extract_todays_messages()

# Cierra el navegador (opcional)
# driver.quit()


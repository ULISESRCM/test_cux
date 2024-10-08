import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Configuración de Chrome y Selenium
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/ulises/.config/google-chrome/default")  # Ajusta esta ruta según tu sistema
driver = webdriver.Chrome(options=options)
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(10)  # Espera hasta 10 segundos para cualquier elemento

# Leer el archivo CSV con los disparadores
contact_df = pd.read_csv('CUX-QA.csv')

# Nombre del contacto (el chatbot en este caso)
contact_name = "Buenos Aires Ciudad"

# Buscar el chat del contacto "Buenos Aires Ciudad"
search_bar = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]')
search_bar.clear()
search_bar.send_keys(contact_name)
time.sleep(2)  # Esperar un par de segundos para que cargue la búsqueda

# Seleccionar el contacto
contact_element = driver.find_element(By.XPATH, f'//*[@title="{contact_name}"]')
contact_element.click()
time.sleep(2)  # Esperar a que se abra el chat

# Enviar el primer disparador del archivo CSV
disparador = contact_df.iloc[0]['disparadores']

# Ubicar el cuadro de texto y enviar el disparador
message_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
message_box.send_keys(disparador)
message_box.send_keys(Keys.ENTER)

# Esperar a que el bot responda (ajusta el tiempo si es necesario)
time.sleep(5)

# Capturar el primer <span> que comienza con "La"
try:
    span = driver.find_element(By.XPATH, '//span[starts-with(text(), "La")]')
    bot_response_text = span.text  # Extraer el texto del span

    # Obtener la respuesta esperada del CSV y formatear
    respuesta_esperada = contact_df.iloc[0]['contenido'].replace("*", "").strip()  # Eliminamos los asteriscos

    # Normalizar ambos textos para comparación
    bot_response_text_normalized = bot_response_text.strip()
    respuesta_esperada_normalized = respuesta_esperada

    # Mostrar la longitud de las cadenas
    print("Longitud de la respuesta del bot:", len(bot_response_text_normalized))
    print("Longitud de la respuesta esperada:", len(respuesta_esperada_normalized))

    # Comparar la respuesta del bot con la salida esperada
    print("Respuesta del bot:", bot_response_text_normalized)
    print("Respuesta esperada:", respuesta_esperada_normalized)

    if bot_response_text_normalized == respuesta_esperada_normalized:
        print("Resultado: Aprobado")
    else:
        print("Resultado: Fallido")

except Exception as e:
    print(f"No se encontró el span o ocurrió un error: {e}")

# Cerrar el navegador (opcional)
# driver.quit()  # Descomenta esto si deseas cerrar el navegador automáticamente después

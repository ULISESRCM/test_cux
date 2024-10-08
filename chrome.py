import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración de Chrome y Selenium
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/ulises/.config/google-chrome/default")  # Ajusta esta ruta según tu sistema
driver = webdriver.Chrome(options=options)
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(5)  # Espera hasta 5 segundos para cualquier elemento

# Leer el archivo CSV con los disparadores y el contenido esperado
contact_df = pd.read_csv('CUX-QA.csv')

# Asegurarse de que la columna 'aprobado' sea del tipo str
contact_df['aprobado'] = ''  # Inicializar la columna 'aprobado' como cadena

# Nombre del contacto (el chatbot en este caso)
contact_name = "Buenos Aires Ciudad"

# Buscar el chat del chatbot (usando el nombre del contacto) UNA VEZ
search_bar = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]')
search_bar.clear()
search_bar.send_keys(contact_name)
time.sleep(2)  # Esperar un par de segundos para que cargue la búsqueda

# Seleccionar el chat del contacto
contact_element = driver.find_element(By.XPATH, f'//*[@title="{contact_name}"]')
contact_element.click()

# Iterar sobre las filas del archivo CSV para enviar disparadores y comparar las respuestas
for index, row in contact_df.iterrows():
    titulo_corto = "Identidad de género"
    disparador = row['disparadores']
    respuesta_esperada = row['contenido'].replace("*", "")

    # Obtener las primeras dos letras de la respuesta esperada
    search_text = respuesta_esperada[:3]
    print(search_text)

    # Ubicar el cuadro de texto y enviar el disparador
    message_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    message_box.send_keys(disparador)
    message_box.send_keys(Keys.ENTER)

    # Esperar a que el bot responda (ajusta el tiempo si es necesario)
    time.sleep(5)

    # Capturar el primer <span> que comienza con las dos primeras letras de `respuesta_esperada`
    try:
        # Usar las primeras dos letras en el XPath
        bot_response_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[starts-with(text(), "{search_text}")] | //span[contains(text(), ". {titulo_corto}")]'))
        )
        bot_respuesta = bot_response_element.text.strip()  # Extraer el texto del span
        print(f"texto encontrado: {bot_respuesta}")

    except Exception:
        bot_respuesta = ""  # Asignamos un espacio en blanco si no se encuentra el span

    # Comparar la respuesta del bot con el contenido esperado
    print("----------")
    print(f"Disparador: {disparador}")
    print(f"Respuesta esperada: {respuesta_esperada}")
    print(f"Respuesta del bot: {bot_respuesta}")
    

    if bot_respuesta:  # Si hay respuesta del bot
        if respuesta_esperada in bot_respuesta or bot_respuesta[3:] == titulo_corto:
            contact_df.at[index, 'aprobado'] = 'aprobado'
            print("Resultado: Aprobado")
        else:
            contact_df.at[index, 'aprobado'] = 'desaprobado'
            print("Resultado: Desaprobado")
    else:  # Si no hay respuesta del bot
        contact_df.at[index, 'aprobado'] = 'desaprobado'
        print("Resultado: Desaprobado")

    # Intentar vaciar el chat después de cada disparador
    try:
        # Hacer clic en los tres puntos
        menu_button = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[3]/div/div[3]/div')
        menu_button.click()
        time.sleep(1)  # Esperar a que se despliegue el menú

        # Seleccionar la opción "Vaciar chat"
        clear_chat_option = driver.find_element(By.XPATH, '//div[text()="Vaciar chat"]')
        clear_chat_option.click()
        time.sleep(1)  # Esperar el cuadro de confirmación

        # Confirmar vaciar el chat
        confirm_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div/button[2]'))
        )
        confirm_button.click()
        time.sleep(2)  # Esperar a que el chat se vacíe

    except:
        pass  # No imprimir errores
        # Ubicar el cuadro de texto y enviar el disparador
    message_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
    message_box.send_keys("@clean")
    message_box.send_keys(Keys.ENTER)
    time.sleep(3)

# Guardar los resultados de la prueba en un nuevo archivo CSV
contact_df.to_csv('CUX-QA-resultados.csv', index=False)

# Cerrar el navegador
driver.quit()

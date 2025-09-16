from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def esperar_ajax(navegador):
    espera = WebDriverWait(navegador, 10)
    espera.until(EC.invisibility_of_element_located((By.ID, "ajax-overlay")))

def selecionar_combo_box(navegador, tipo_seletor, seletor, valor):
    esperar_ajax(navegador)
    espera_objeto = WebDriverWait(navegador, 10)
    espera_objeto.until(EC.element_to_be_clickable((tipo_seletor, seletor)))
    objeto = navegador.find_element(tipo_seletor, seletor)
    combo_box = Select((objeto))
    combo_box.select_by_value(valor)

def clicar(navegador, tipo_seletor, seletor):
    esperar_ajax(navegador)
    espera_objeto = WebDriverWait(navegador, 10)
    espera_objeto.until(EC.element_to_be_clickable((tipo_seletor, seletor)))
    objeto = navegador.find_element(tipo_seletor, seletor)
    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'})", objeto)
    objeto.click()

def escrever(navegador, tipo_seletor, seletor, key):
    esperar_ajax(navegador)
    espera_objeto = WebDriverWait(navegador, 10)
    espera_objeto.until(EC.element_to_be_clickable((tipo_seletor, seletor)))
    objeto = navegador.find_element(tipo_seletor, seletor)
    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'})", objeto)
    objeto.send_keys(key)

def pegar_texto(navegador, tipo_seletor, seletor):
    espera_objeto = WebDriverWait(navegador, 3)
    espera_objeto.until(EC.element_to_be_clickable((tipo_seletor, seletor)))
    objeto = navegador.find_element(tipo_seletor, seletor)
    return objeto.text

def limpar_campo(navegador, tipo_seletor, seletor):
    esperar_ajax(navegador)
    espera_objeto = WebDriverWait(navegador, 10)
    espera_objeto.until(EC.element_to_be_clickable((tipo_seletor, seletor)))
    objeto = navegador.find_element(tipo_seletor, seletor)
    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'})", objeto)
    objeto.clear()

def limpar_campo_backspace(navegador, tipo_seletor, seletor):
    esperar_ajax(navegador)
    espera_objeto = WebDriverWait(navegador, 10)
    espera_objeto.until(EC.element_to_be_clickable((tipo_seletor, seletor)))
    objeto = navegador.find_element(tipo_seletor, seletor)
    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'})", objeto)
    objeto.send_keys(Keys.BACKSPACE * 50)

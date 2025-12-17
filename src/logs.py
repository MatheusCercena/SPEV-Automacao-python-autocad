import os, sys
import traceback
from datetime import datetime
import random
import string

def criar_alfanumerico():
    """
    Cria um alfanumérico de 10 valores.
    """
    caracteres = string.ascii_letters + string.digits
    s = ''.join(random.choices(caracteres, k=10))
    return s

def log_spev(mensagem: str, nome_arquivo="spev.log"):
    try:
        pasta_spev = os.path.dirname(sys.executable)
        caminho_log = os.path.join(pasta_spev, nome_arquivo)

        pasta_destino = os.path.dirname(caminho_log)
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto_log = f"[{timestamp}] {mensagem}\n"

        with open(caminho_log, "a", encoding="utf-8") as f:
            f.write(texto_log)

    except Exception as e:
        print(f"[ERRO] Não foi possível gravar no log: {e} {traceback.format_exc()}")

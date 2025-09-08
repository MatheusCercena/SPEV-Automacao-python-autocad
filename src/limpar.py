"""
Módulo para limpeza do ModelSpace do AutoCAD.

Inclui função para remover todas as entidades do espaço de modelo, facilitando o reinício do desenho.
"""
from pyautocad import Autocad
from src.autocad_conn import get_acad
from time import sleep

def limpar_tudo() -> None:
    """Remove todas as entidades do ModelSpace do AutoCAD.

    Deleta todas as linhas e outras entidades do espaço de modelo do AutoCAD.

    Returns:
        None: Função remove elementos do AutoCAD sem retorno.
    """
    acad2 = Autocad(create_if_not_exists=True)
    acad, acad_ModelSpace = get_acad()

    for linha in acad_ModelSpace:
        linha.Delete()
    sleep(1)

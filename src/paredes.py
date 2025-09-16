"""
Módulo para desenho e manipulação de paredes no AutoCAD.

Inclui funções para desenhar paredes laterais, aplicar fillets e integrar paredes aos perfis U do projeto.
"""
"""
Desenha as paredes, através de offsets chamados via COM e fillets por lisp.
"""
import pythoncom
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from math import radians
from time import sleep

def fazer_parede_esq(lcs: list[float], perfil_U_ext: str, perfil_U_int: str, angulo: float) -> str:
    """Desenha a parede esquerda sem dar fillet com os perfis U.

    Args:
        lcs: Lista com coordenadas da linha de centro [x1, y1, x2, y2].
        perfil_U_ext: Handle do perfil U externo.
        perfil_U_int: Handle do perfil U interno.
        angulo: Ângulo de rotação da parede em graus.

    Returns:
        str: Handle da parede esquerda criada.
    """
    acad, acad_ModelSpace = get_acad()
    acad2 = Autocad(create_if_not_exists=True)
    for _ in range(5):
        try:
            pythoncom.PumpWaitingMessages()
            ini = acad.HandleToObject(perfil_U_ext).StartPoint
            fim = acad.HandleToObject(perfil_U_int).StartPoint
            break
        except:
            sleep(0.5)
    linha = acad2.model.AddLine(APoint(ini[0], ini[1]), APoint(fim[0], fim[1]))
    linha.Rotate(APoint(lcs[0], lcs[1]), radians(angulo * 1))
    linha.Layer = 'Paredes'
    return linha.Handle

def fazer_parede_dir(handles_lcs: list[float], perfil_U_ext: str, perfil_U_int: str, angulo: float) -> str:
    """Desenha a parede direita sem dar fillet com os perfis U.

    Args:
        handles_lcs: Lista com coordenadas da linha de centro [x1, y1, x2, y2].
        perfil_U_ext: Handle do perfil U externo.
        perfil_U_int: Handle do perfil U interno.
        angulo: Ângulo de rotação da parede em graus.

    Returns:
        str: Handle da parede direita criada.
    """
    acad, acad_ModelSpace = get_acad()
    acad2 = Autocad(create_if_not_exists=True)

    for _ in range(5):
        try:
            pythoncom.PumpWaitingMessages()
            ini = acad.HandleToObject(perfil_U_ext).EndPoint
            fim = acad.HandleToObject(perfil_U_int).EndPoint
            break
        except:
            sleep(0.5)
    linha = acad2.model.AddLine(APoint(ini[0], ini[1]), APoint(fim[0], fim[1]))
    linha.Rotate(APoint(handles_lcs[2], handles_lcs[3]), radians(angulo * -1))
    linha.Layer = 'Paredes'
    return linha.Handle

def fillet_paredes(handle_perfil_U_ext: str, handle_perfil_U_int: str, handle_parede: str) -> None:
    """Aplica fillets nos perfis U com a parede.

    Args:
        handle_perfil_U_ext: Handle do perfil U externo.
        handle_perfil_U_int: Handle do perfil U interno.
        handle_parede: Handle da parede.

    Returns:
        None: Função executa comandos no AutoCAD sem retorno.
    """
    acad, acad_ModelSpace = get_acad()
    acad2 = Autocad(create_if_not_exists=True)

    acad.SendCommand(f'(c:custom_fillet "{handle_perfil_U_ext}" "{handle_parede}")\n')
    acad.SendCommand(f'(c:custom_fillet "{handle_parede}" "{handle_perfil_U_int}")\n')

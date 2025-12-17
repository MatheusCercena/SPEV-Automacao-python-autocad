import os
from time import sleep
from src.autocad_conn import get_acad
from pyautocad import Autocad, APoint

def carregar_comandos() -> None:

    lisp_code = f'''
(defun c:custom_fillet ( h1 h2 / linha1 linha2)
    (setq linha1 (handent h1))
    (setq linha2 (handent h2))
    (command "_.fillet" linha1 linha2)
    (princ "\nComando")
    (princ)
)
'''
    acad, acad_ModelSpace = get_acad()

    #__file__ retorna a pasta atual, lisp é a pasta a ser criada, os.path.join junta os 2 caminhos
    dir_base = os.path.join(os.path.dirname(__file__), 'lisp')
    os.makedirs(dir_base, exist_ok=True)
    dir_lisp = os.path.join(dir_base, "custom_fillet_perfil_U.lsp")

    with open(dir_lisp, "w") as file:
        file.write(lisp_code.strip())
    caminho_lisp = os.path.normpath(dir_lisp).replace("\\", "\\\\")
    acad.SendCommand(f'(load "{caminho_lisp}")\n')
    sleep(3)

def remover_guias() -> None:
    """Remove as guias dos vidros do AutoCAD.

    Returns:
        None: Função remove elementos do AutoCAD sem retorno.
    """
    acad, acad_ModelSpace = get_acad()

    for i in range(acad_ModelSpace.Count - 1, -1, -1):  # reverso
        try:
            entidade = acad_ModelSpace.Item(i)
            if entidade.EntityName == 'AcDbLine' and entidade.Layer == '0':
                entidade.Delete()
        except Exception as e:
            print(f"Erro ao deletar entidade {i}: {e}")

def adicionar_texto_layout(texto, posicao: tuple[float, float, float], altura: float) -> None:
    acad, acad_ModelSpace = get_acad()
    autocad = Autocad()
    layout_space = autocad.doc.PaperSpace
    model_space = autocad.doc.ModelSpace

    texto = layout_space.AddText(texto, posicao, altura)
    return texto

def adicionar_texto_modelspace(texto, posicao: tuple[float, float, float], altura: float) -> None:
    acad, acad_ModelSpace = get_acad()
    autocad = Autocad()
    layout_space = autocad.doc.PaperSpace
    model_space = autocad.doc.ModelSpace

    texto = model_space.AddText(texto, posicao, altura)
    return texto

def adicionar_mtext_modelspace(texto, posicao: tuple[float, float, float], altura: float, largura: float) -> None:
    acad, acad_ModelSpace = get_acad()
    autocad = Autocad()
    layout_space = autocad.doc.PaperSpace
    model_space = autocad.doc.ModelSpace

    texto = model_space.AddMText(posicao, largura, texto)
    texto.Height = altura
    return texto

def garantir_layer_ativa():
    acad = Autocad()
    layer_padrao = '0'

    try:
        layers = acad.doc.Layers
        
        target_layer = layers.Item(layer_padrao)
        
        acad.doc.ActiveLayer = target_layer
                
    except Exception as e:
        print(f"Erro: Não foi possível definir a layer. Verifique se o nome '{layer_padrao}' existe.")
        print(f"Detalhes: {e}")
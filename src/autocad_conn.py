"""
Módulo de conexão com o AutoCAD via COM.

Fornece função utilitária para obter o documento ativo e o ModelSpace do AutoCAD, permitindo integração com outros módulos do projeto.
"""
import win32com.client

def get_acad() -> tuple:
    """Estabelece conexão com o AutoCAD ativo.

    Conecta com a instância ativa do AutoCAD e retorna o documento e o ModelSpace.

    Returns:
        tuple: Tupla contendo:
            - Documento ativo do AutoCAD
            - ModelSpace do documento

    Raises:
        RuntimeError: Se não conseguir conectar com o AutoCAD.
    """
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application").ActiveDocument
        return acad, acad.ModelSpace
    except Exception as erro:
        print('Erro ao conectar ao AutoCAD')
        raise RuntimeError("Erro ao conectar com o AutoCAD") from erro


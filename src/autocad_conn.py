import win32com.client

def get_acad() -> tuple:
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application").ActiveDocument
        return acad, acad.ModelSpace
    except Exception as erro:
        print('Erro ao conectar ao AutoCAD')
        raise RuntimeError("Erro ao conectar com o AutoCAD") from erro


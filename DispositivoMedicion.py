class DispositivoMedicion:
    def __init__(self, id:int,tipo_de_variable: str, umbral_limite: float, aviso_activo: bool):
        self.id = id
        self.tipo_de_variable = tipo_de_variable
        self.umbral_limite = umbral_limite
        self.aviso_activo = aviso_activo
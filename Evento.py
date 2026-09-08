import datetime
class Evento:           #Poner una validacion para que el evento que estamos metiendo en el historial ya esté cerrado
    def __init__(self,fecha: datetime ,descripcion:str,personal:list, componentes_utilizados:list):
        self.fecha=fecha
        self.descripcion=descripcion
        self.personal=personal
        self.componentes_utilizados= componentes_utilizados
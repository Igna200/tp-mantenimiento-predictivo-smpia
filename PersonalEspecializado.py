import datetime
from estados.Especialidad import Especialidad
class PersonalEspecializado:
    def __init__(self, id:int, nombre:str,apellido: str, especialidad:Especialidad, fecha_nacimiento: datetime.date, disponibilidad:bool = True):
        self.nombre=nombre
        self.apellido=apellido
        self.especialidad=especialidad
        self.id=id
        self.fecha_nacimiento= fecha_nacimiento
        self.disponibilidad=disponibilidad

    def ocupar(self):

        if not self.disponibilidad:
            raise ValueError(f"El personal {self.nombre} {self.apellido} ya está ocupado.")
        self.disponibilidad = False

    def liberar(self):

        self.disponibilidad = True
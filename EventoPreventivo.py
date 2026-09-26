from Evento import Evento
import datetime

class EventoPreventivo(Evento):
    def __init__(self, fecha: datetime.date, descripcion: str, programa):
        super().__init__(fecha, descripcion)
        self.programa = programa

    def __str__(self):
        return f"{super().__str__()} | Programa: {self.programa}"
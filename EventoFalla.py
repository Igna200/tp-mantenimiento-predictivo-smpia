from Evento import Evento
import datetime

class EventoFalla(Evento):
    def __init__(self, fecha: datetime.date, descripcion: str, causa: str, dispositivo_origen):
        super().__init__(fecha, descripcion)
        if not causa or not causa.strip():
            raise ValueError("El evento de falla debe indicar una causa")

        self.causa = causa
        self.dispositivo_origen = dispositivo_origen

    def __str__(self):
        return f"{super().__str__()} | Causa: {self.causa} | Dispositivo: {self.dispositivo_origen}"
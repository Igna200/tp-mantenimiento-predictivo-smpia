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

    def to_dict(self):
        datos = super().to_dict()
        datos["tipo_evento"] = "falla"
        datos["causa"] = self.causa
        datos["dispositivo_origen_id"] = self.dispositivo_origen.id if self.dispositivo_origen else None
        return datos

    @classmethod
    def from_dict(cls, datos, dispositivo_origen):
        return cls(
            fecha=datetime.date.fromisoformat(datos["fecha"]),
            descripcion=datos["descripcion"],
            causa=datos["causa"],
            dispositivo_origen=dispositivo_origen,
        )
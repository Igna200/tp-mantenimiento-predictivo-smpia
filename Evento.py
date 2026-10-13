import datetime

class Evento:
    def __init__(self, fecha: datetime.date, descripcion: str):
        if fecha > datetime.date.today():
            raise ValueError("La fecha de un evento no puede ser futura")
        if not descripcion or not descripcion.strip():
            raise ValueError("El evento debe tener una descripción")

        self.fecha = fecha
        self.descripcion = descripcion

    def __str__(self):
        return f"[{self.fecha}] {self.descripcion}"

    def to_dict(self):
        # Las hijas llaman a este método con super().to_dict() y le agregan sus propios
        # campos + un "tipo_evento" para saber, al leer el JSON, qué subclase reconstruir.
        return {"fecha": self.fecha.isoformat(), "descripcion": self.descripcion}
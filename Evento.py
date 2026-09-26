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
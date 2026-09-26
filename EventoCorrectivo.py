from Evento import Evento
import datetime

class EventoCorrectivo(Evento):
    def __init__(self, fecha: datetime.date, descripcion: str,
                 personal: list, componentes_utilizados: list, aviso_resuelto):
        super().__init__(fecha, descripcion)
        if not personal:
            raise ValueError("El evento correctivo debe tener al menos un miembro del personal asociado")

        self.personal = personal
        self.componentes_utilizados = componentes_utilizados if componentes_utilizados is not None else []
        self.aviso_resuelto = aviso_resuelto

    def __str__(self):
        nombres_personal = ", ".join(p.nombre for p in self.personal)
        nombres_componentes = ", ".join(c.nombre for c in self.componentes_utilizados)
        return (f"{super().__str__()} | Personal: {nombres_personal} | "
                f"Componentes: {nombres_componentes}")
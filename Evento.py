import datetime
class Evento:
    def __init__(self, fecha: datetime.date, descripcion: str,
                 personal: list, componentes_utilizados: list):

        if fecha > datetime.date.today():
            raise ValueError("La fecha de un evento no puede ser futura")

        if not descripcion or not descripcion.strip():
            raise ValueError("El evento debe tener una descripción")

        if not personal:
            raise ValueError("El evento debe tener al menos un miembro del personal asociado")

        self.fecha = fecha
        self.descripcion = descripcion
        self.personal = personal
        self.componentes_utilizados = componentes_utilizados
        if componentes_utilizados is None:
            self.componentes_utilizados = []
        
    def __str__(self):
        nombres_personal = ", ".join(p.nombre for p in self.personal)
        nombres_componentes = ", ".join(c.nombre for c in self.componentes_utilizados)
        return (f"[{self.fecha}] {self.descripcion} | "
                f"Personal: {nombres_personal} | Componentes: {nombres_componentes}")    

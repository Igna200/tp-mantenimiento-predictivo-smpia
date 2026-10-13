from Evento import Evento
import datetime

class EventoPreventivo(Evento):
    def __init__(self, fecha: datetime.date, descripcion: str, programa):
        super().__init__(fecha, descripcion)
        self.programa = programa
        # "Foto" del programa al momento de completarse. El programa sigue su ciclo (se reprograma
        # y vuelve a PROGRAMADO), pero el historial tiene que mostrar lo que pasó en esta ejecución.
        self.procedimiento = programa.procedimiento
        self.personal = list(programa.personal_asignado)
        self.componentes_utilizados = dict(programa.componentes_requeridos)
        self.fecha_proxima = programa.fecha_programada

    def __str__(self):
        nombres_personal = ", ".join(p.nombre for p in self.personal) or "ninguno"
        componentes = ", ".join(f"{c.nombre} x{n}" for c, n in self.componentes_utilizados.items()) or "ninguno"
        return (f"{super().__str__()} | Programa: {self.procedimiento} (completado) | "
                f"Personal: {nombres_personal} | Componentes: {componentes} | "
                f"Próxima ejecución: {self.fecha_proxima}")

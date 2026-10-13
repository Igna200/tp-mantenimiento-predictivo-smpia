from Evento import Evento
from ComponenteRecambio import ComponenteRecambio
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

    def to_dict(self):
        datos = super().to_dict()
        datos["tipo_evento"] = "preventivo"
        datos["procedimiento"] = self.procedimiento
        datos["personal_ids"] = [p.id for p in self.personal]
        datos["componentes_utilizados"] = ComponenteRecambio.serializar_requeridos(self.componentes_utilizados)
        datos["fecha_proxima"] = self.fecha_proxima.isoformat()
        # ProgramaIntervencion no tiene un id propio: lo referenciamos por su posición
        # dentro de la lista de programas de su maquinaria (siempre el mismo orden).
        datos["programa_indice"] = self.programa.maquinaria.programas.index(self.programa)
        return datos

    @classmethod
    def from_dict(cls, datos, programa, personal_por_id, componentes_por_id):
        # El __init__ normal arma procedimiento/personal/componentes/fecha_proxima leyéndolos
        # del estado ACTUAL de `programa` — pero ese programa ya se pudo haber reprogramado
        # (o re-ejecutado con otro personal) desde que se guardó ESTE evento histórico.
        # Necesitamos la "foto" que se guardó en su momento, no el estado de hoy, así que
        # no pasamos por __init__: armamos el objeto directo y asignamos todo a mano.
        obj = cls.__new__(cls)
        obj.fecha = datetime.date.fromisoformat(datos["fecha"])
        obj.descripcion = datos["descripcion"]
        obj.programa = programa
        obj.procedimiento = datos["procedimiento"]
        obj.personal = [personal_por_id[pid] for pid in datos["personal_ids"]]
        obj.componentes_utilizados = ComponenteRecambio.deserializar_requeridos(
            datos["componentes_utilizados"], componentes_por_id
        )
        obj.fecha_proxima = datetime.date.fromisoformat(datos["fecha_proxima"])
        return obj

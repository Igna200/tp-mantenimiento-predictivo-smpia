import datetime
from ProgramaIntervencion import ProgramaIntervencion
from EventoPreventivo import EventoPreventivo
from ComponenteRecambio import ComponenteRecambio
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from estados.Especialidad import Especialidad
class ProgramaPreventivo(ProgramaIntervencion):
    def __init__(self,maquinaria, procedimiento, componentes_requeridos, tiempo_requerido,especialidad_requerida, periodicidad, tipo_equipo):
        super().__init__(maquinaria,procedimiento, componentes_requeridos,tiempo_requerido, especialidad_requerida)
        
        self.periodicidad = periodicidad          # cantidad de días entre ejecuciones
        self.tipo_equipo = tipo_equipo
        self.fecha_ultima_ejecucion = None
        self.fecha_programada = datetime.date.today()

    def programar_siguiente(self):
        if self.estado != EstadoProgramaIntervencion.COMPLETADO:
            raise ValueError(
                "No se puede programar el siguiente mantenimiento: "
                "el programa actual todavía no fue completado"
            )

        base = self.fecha_ultima_ejecucion or datetime.date.today()
        self.fecha_programada = base + datetime.timedelta(days=self.periodicidad)
        self.estado = EstadoProgramaIntervencion.PROGRAMADO
        return self.fecha_programada
    # En ProgramaPreventivo

    def crear_evento_especifico(self):
        # Primero se reprograma y después se crea el evento, así el evento ya conoce
        # la fecha de la próxima ejecución
        self.fecha_ultima_ejecucion = datetime.date.today()
        self.programar_siguiente()

        return EventoPreventivo(
            fecha=datetime.date.today(),
            descripcion=f"Mantenimiento preventivo periódico de {self.tipo_equipo}",
            programa=self
        )

    def to_dict(self):
        return {
            "tipo": "preventivo",
            "procedimiento": self.procedimiento,
            "componentes_requeridos": ComponenteRecambio.serializar_requeridos(self.componentes_requeridos),
            "tiempo_requerido": self.tiempo_requerido,
            "especialidad_requerida": self.especialidad_requerida.value,
            "estado": self.estado.value,
            "personal_asignado_ids": [p.id for p in self.personal_asignado],
            "tipo_equipo": self.tipo_equipo,
            "periodicidad": self.periodicidad,
            "fecha_ultima_ejecucion": (
                self.fecha_ultima_ejecucion.isoformat() if self.fecha_ultima_ejecucion else None
            ),
            "fecha_programada": self.fecha_programada.isoformat(),
        }

    @classmethod
    def from_dict(cls, datos, maquinaria, personal_por_id, componentes_por_id):
        # El constructor no tiene ninguna regla que pueda rechazar un estado ya avanzado
        # (a diferencia de ProgramaCorrectivo), así que alcanza con llamarlo normal y
        # después pisar los campos que el __init__ deja "de fábrica" (PROGRAMADO, sin
        # personal, sin fecha de última ejecución) con el estado real que tenía al guardar.
        programa = cls(
            maquinaria,
            datos["procedimiento"],
            ComponenteRecambio.deserializar_requeridos(datos["componentes_requeridos"], componentes_por_id),
            datos["tiempo_requerido"],
            Especialidad(datos["especialidad_requerida"]),
            datos["periodicidad"],
            datos["tipo_equipo"],
        )
        programa.estado = EstadoProgramaIntervencion(datos["estado"])
        programa.personal_asignado = [personal_por_id[pid] for pid in datos["personal_asignado_ids"]]
        fecha_ult = datos.get("fecha_ultima_ejecucion")
        programa.fecha_ultima_ejecucion = datetime.date.fromisoformat(fecha_ult) if fecha_ult else None
        programa.fecha_programada = datetime.date.fromisoformat(datos["fecha_programada"])
        return programa

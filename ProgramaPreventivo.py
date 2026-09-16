import datetime
from ProgramaIntervencion import ProgramaIntervencion
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
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

    def _generar_descripcion_evento(self):
        return f"Mantenimiento preventivo periódico de {self.tipo_equipo}"

    def _acciones_especificas_al_finalizar(self):
        self.fecha_ultima_ejecucion = datetime.date.today()
        self.programar_siguiente()
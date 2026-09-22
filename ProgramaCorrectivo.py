from Aviso import Aviso
from ProgramaIntervencion import ProgramaIntervencion
from estados.EstadoAviso import EstadoAviso
from estados.EstadoMaquinaria import EstadoMaquinaria

class ProgramaCorrectivo(ProgramaIntervencion):
    es_correctivo = True

    def __init__(self,maquinaria, procedimiento, componentes_requeridos, tiempo_requerido,especialidad_requerida, aviso_asociado: Aviso, tipo_equipo: str):
        if aviso_asociado.estado != EstadoAviso.ACTIVO:
            raise ValueError("Un programa correctivo debe estar asociado a un aviso activo")

        super().__init__(maquinaria,procedimiento, componentes_requeridos,tiempo_requerido, especialidad_requerida)
        self.aviso_asociado = aviso_asociado
        self.tipo_equipo = tipo_equipo
    # En ProgramaCorrectivo

    def generar_descripcion_evento(self):
        return f"Corrección de {self.tipo_equipo}: {self.aviso_asociado.parametro_anomalo}"

    def acciones_especificas_al_finalizar(self):
        self.aviso_asociado.cerrar_aviso()
        try:
            self.maquinaria.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
        except Exception:
            pass  # sigue habiendo avisos críticos u otros correctivos pendientes: se queda como está
        

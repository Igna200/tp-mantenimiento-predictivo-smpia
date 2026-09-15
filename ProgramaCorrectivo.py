from Aviso import Aviso
from ProgramaIntervencion import ProgramaIntervencion
class ProgramaCorrectivo(ProgramaIntervencion):
    def __init__(self,maquinaria, procedimiento, componentes_requeridos, tiempo_requerido,especialidad_requerida, aviso_asociado: Aviso, tipo_equipo: str):
        super().__init__(maquinaria,procedimiento, componentes_requeridos,tiempo_requerido, especialidad_requerida)
        self.aviso_asociado = aviso_asociado
        self.tipo_equipo = tipo_equipo
    # En ProgramaCorrectivo

    def _generar_descripcion_evento(self):
        return f"Corrección de {self.tipo_equipo}: {self.aviso_asociado.parametro_anomalo}"

    def _acciones_especificas_al_finalizar(self):
        self.aviso_asociado.cerrar_aviso()

    #Al finalizar un correctivo, usar el setter de estado maquinaria
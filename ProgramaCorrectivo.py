from Aviso import Aviso
class ProgramaCorrectivo(ProgramaIntervencion):
    def __init__(self, procedimiento, componentes_requeridos, tiempo_requerido,especialidad_requerida, aviso_asociado: Aviso, tipo_equipo: str):
        super().__init__(procedimiento, componentes_requeridos,tiempo_requerido, especialidad_requerida)
        self.aviso_asociado = aviso_asociado
        self.tipo_equipo = tipo_equipo


    #Al finalizar un correctivo, usar el setter de estado maquinaria
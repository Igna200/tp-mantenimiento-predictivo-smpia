from Aviso import Aviso
from ProgramaIntervencion import ProgramaIntervencion
from estados.EstadoAviso import EstadoAviso
from estados.EstadoMaquinaria import EstadoMaquinaria
import datetime
from EventoCorrectivo import EventoCorrectivo

class ProgramaCorrectivo(ProgramaIntervencion):
    es_correctivo = True

    def __init__(self,maquinaria, procedimiento, componentes_requeridos, tiempo_requerido,especialidad_requerida, aviso_asociado: Aviso, tipo_equipo: str):
        if aviso_asociado.estado != EstadoAviso.ACTIVO:
            raise ValueError("Un programa correctivo debe estar asociado a un aviso activo")

        super().__init__(maquinaria,procedimiento, componentes_requeridos,tiempo_requerido, especialidad_requerida)
        self.aviso_asociado = aviso_asociado
        self.tipo_equipo = tipo_equipo
    # En ProgramaCorrectivo




    def crear_evento_especifico(self):
        # Regla 8: al completar el correctivo, el aviso se resuelve automáticamente
        if self.aviso_asociado.estado == EstadoAviso.ACTIVO:  # puede haberlo desactivado alguien a mano
            self.aviso_asociado.cerrar_aviso()

        evento = EventoCorrectivo(
            fecha=datetime.date.today(),
            descripcion=f"Corrección de {self.tipo_equipo}: {self.aviso_asociado.parametro_anomalo}",
            personal=list(self.personal_asignado),
            componentes_utilizados=list(self.componentes_requeridos.keys()),
            aviso_resuelto=self.aviso_asociado
        )

        # Regla 8: vuelve a operativa "si no hay otras condiciones que lo impidan"
        try:
            self.maquinaria.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
        except ValueError:
            pass  # sigue habiendo avisos críticos u otros correctivos pendientes: se queda como está

        return evento


    def generar_descripcion_evento(self):
        return f"Corrección de {self.tipo_equipo}: {self.aviso_asociado.parametro_anomalo}"

    def acciones_especificas_al_finalizar(self):
        self.aviso_asociado.cerrar_aviso()
        try:
            self.maquinaria.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
        except Exception:
            pass  # sigue habiendo avisos críticos u otros correctivos pendientes: se queda como está
        

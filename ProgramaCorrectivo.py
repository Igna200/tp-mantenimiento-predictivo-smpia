from Aviso import Aviso
from ProgramaIntervencion import ProgramaIntervencion
from estados.EstadoAviso import EstadoAviso
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.Especialidad import Especialidad
import datetime
import unicodedata
from EventoCorrectivo import EventoCorrectivo

class ProgramaCorrectivo(ProgramaIntervencion):
    es_correctivo = True

    # Regla 7: la especialidad requerida depende de la naturaleza de la anomalía
    ESPECIALIDAD_POR_VARIABLE = {
        "presion": Especialidad.hidraulico,
        "caudal": Especialidad.hidraulico,
        "vibracion": Especialidad.mecanico,
        "temperatura": Especialidad.mecanico,
        "consumo energetico": Especialidad.electronico,
        "voltaje": Especialidad.electronico,
        "corriente": Especialidad.electronico,
    }

    def __init__(self, maquinaria, procedimiento, componentes_requeridos, tiempo_requerido,
                 aviso_asociado: Aviso, tipo_equipo: str, especialidad_requerida=None):
        if aviso_asociado.estado != EstadoAviso.ACTIVO:
            raise ValueError("Un programa correctivo debe estar asociado a un aviso activo")

        if especialidad_requerida is None:
            especialidad_requerida = self.especialidad_para_variable(aviso_asociado.parametro_anomalo)

        super().__init__(maquinaria,procedimiento, componentes_requeridos,tiempo_requerido, especialidad_requerida)
        self.aviso_asociado = aviso_asociado
        self.tipo_equipo = tipo_equipo

    @classmethod
    def especialidad_para_variable(cls, variable: str):
        # Normaliza "Presión " -> "presion" para que no importen mayúsculas, espacios ni tildes
        sin_tildes = unicodedata.normalize("NFD", str(variable)).encode("ascii", "ignore").decode()
        clave = sin_tildes.strip().lower()
        if clave not in cls.ESPECIALIDAD_POR_VARIABLE:
            raise ValueError(
                f"No se puede deducir la especialidad para la variable '{variable}'; "
                f"indíquela explícitamente"
            )
        return cls.ESPECIALIDAD_POR_VARIABLE[clave]




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

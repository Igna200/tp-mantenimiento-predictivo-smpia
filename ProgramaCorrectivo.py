from Aviso import Aviso
from ProgramaIntervencion import ProgramaIntervencion
from ComponenteRecambio import ComponenteRecambio
from estados.EstadoAviso import EstadoAviso
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
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
            # Copia del diccionario componente -> cantidad: el evento guarda qué y cuánto se usó
            componentes_utilizados=dict(self.componentes_requeridos),
            aviso_resuelto=self.aviso_asociado
        )

        # Regla 8: vuelve a operativa "si no hay otras condiciones que lo impidan"
        try:
            self.maquinaria.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
        except ValueError:
            pass  # sigue habiendo avisos críticos u otros correctivos pendientes: se queda como está

        return evento

    def to_dict(self):
        return {
            "tipo": "correctivo",
            "procedimiento": self.procedimiento,
            "componentes_requeridos": ComponenteRecambio.serializar_requeridos(self.componentes_requeridos),
            "tiempo_requerido": self.tiempo_requerido,
            "especialidad_requerida": self.especialidad_requerida.value,
            "estado": self.estado.value,
            "personal_asignado_ids": [p.id for p in self.personal_asignado],
            "tipo_equipo": self.tipo_equipo,
            "aviso_asociado_id": self.aviso_asociado.id_aviso,
        }

    @classmethod
    def from_dict(cls, datos, maquinaria, personal_por_id, componentes_por_id, aviso_asociado):
        # El __init__ normal exige que el aviso asociado esté ACTIVO (regla 5) — tiene sentido
        # al crear un correctivo nuevo, pero acá podemos estar restaurando uno ya COMPLETADO,
        # cuyo aviso ya quedó RESUELTO automáticamente (regla 8). El constructor lo rechazaría
        # aunque sea un dato históricamente válido. Por eso no lo llamamos: se arma el objeto
        # directo con __new__ (sin pasar por __init__) y se asignan los atributos a mano.
        obj = cls.__new__(cls)
        obj.maquinaria = maquinaria
        obj.procedimiento = datos["procedimiento"]
        obj.componentes_requeridos = ComponenteRecambio.deserializar_requeridos(
            datos["componentes_requeridos"], componentes_por_id
        )
        obj.tiempo_requerido = datos["tiempo_requerido"]
        obj.especialidad_requerida = Especialidad(datos["especialidad_requerida"])
        obj.estado = EstadoProgramaIntervencion(datos["estado"])
        obj.personal_asignado = [personal_por_id[pid] for pid in datos["personal_asignado_ids"]]
        obj.aviso_asociado = aviso_asociado
        obj.tipo_equipo = datos["tipo_equipo"]
        # __init__ nunca corrió, así que el auto-registro en la maquinaria hay que hacerlo acá
        maquinaria.agregar_programa(obj)
        return obj

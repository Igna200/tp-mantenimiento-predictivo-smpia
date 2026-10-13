import datetime
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad
from Maquinaria import Maquinaria
from PersonalEspecializado import PersonalEspecializado

class Aviso:
    id_counter=0
    def __init__(self, severidad: EstadoSeveridad, equipo_afectado: Maquinaria, dispositivo_que_detecto, parametro_anomalo, estado=EstadoAviso.ACTIVO, fecha_cierre=None, fecha_creacion=None):
        if not isinstance(severidad, EstadoSeveridad):
            raise TypeError("severidad debe ser una instancia de EstadoSeveridad")
        if not isinstance(estado, EstadoAviso):
            raise TypeError("estado debe ser una instancia de EstadoAviso")
        if not isinstance(equipo_afectado, Maquinaria):
            raise TypeError("equipo_afectado debe ser una instancia de Maquinaria")

        self.id_aviso=Aviso.id_counter
        Aviso.id_counter+=1
        self.severidad=severidad
        self.equipo_afectado=equipo_afectado
        self.dispositivo_que_detecto=dispositivo_que_detecto
        self.parametro_anomalo=parametro_anomalo
        self.estado=estado
        self.fecha_creacion=fecha_creacion if fecha_creacion is not None else datetime.date.today()
        self.fecha_cierre=fecha_cierre
        self.resuelto_por=None
        self.equipo_afectado.agregar_aviso(self)

    def cerrar_aviso(self):
        if self.estado != EstadoAviso.ACTIVO:
            raise ValueError("El aviso ya está resuelto")
        self.estado = EstadoAviso.RESUELTO
        self.fecha_cierre = datetime.date.today()

    def desactivar(self, personal):
        # Regla 4: resolución manual por parte del personal capacitado
        if not isinstance(personal, PersonalEspecializado):
            raise TypeError("Solo el personal especializado puede desactivar un aviso")
        self.cerrar_aviso()
        self.resuelto_por = personal

    def __repr__(self):
        return (f"Aviso(id={self.id_aviso}, severidad={self.severidad.value}, "
                f"estado={self.estado.value}, equipo={self.equipo_afectado.id_unico})")

    def to_dict(self):
        return {
            "id_aviso": self.id_aviso,
            "severidad": self.severidad.value,
            "estado": self.estado.value,
            "parametro_anomalo": self.parametro_anomalo,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_cierre": self.fecha_cierre.isoformat() if self.fecha_cierre else None,
            "dispositivo_que_detecto_id": self.dispositivo_que_detecto.id if self.dispositivo_que_detecto else None,
            "resuelto_por_id": self.resuelto_por.id if self.resuelto_por else None,
        }

    @classmethod
    def from_dict(cls, datos, maquinaria, dispositivo_que_detecto, personal_por_id):
        # El constructor no tiene ninguna regla que dependa de "cuánto tiempo pasó" ni de
        # si ya está resuelto, así que reconstruirlo así es seguro (a diferencia de
        # ProgramaCorrectivo, que sí exige que el aviso esté activo al crearse).
        aviso = cls(
            severidad=EstadoSeveridad(datos["severidad"]),
            equipo_afectado=maquinaria,
            dispositivo_que_detecto=dispositivo_que_detecto,
            parametro_anomalo=datos["parametro_anomalo"],
            estado=EstadoAviso(datos["estado"]),
            fecha_cierre=datetime.date.fromisoformat(datos["fecha_cierre"]) if datos.get("fecha_cierre") else None,
            fecha_creacion=datetime.date.fromisoformat(datos["fecha_creacion"]),
        )
        # El constructor siempre asigna el próximo id autoincremental (0, 1, 2...), pero acá
        # necesitamos el id ORIGINAL guardado, así que lo pisamos. Y hay que asegurarse de que
        # el contador global quede por delante del máximo cargado, para que el próximo aviso
        # nuevo que se cree en el programa no repita un id ya usado.
        aviso.id_aviso = datos["id_aviso"]
        Aviso.id_counter = max(Aviso.id_counter, datos["id_aviso"] + 1)

        id_resuelto_por = datos.get("resuelto_por_id")
        aviso.resuelto_por = personal_por_id.get(id_resuelto_por) if id_resuelto_por is not None else None
        return aviso

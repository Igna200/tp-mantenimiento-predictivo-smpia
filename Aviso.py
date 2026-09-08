import datetime
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad

class Aviso:
    id_counter=0
    def __init__(self, severidad: EstadoSeveridad, equipo_afectado, dispositivo_que_detecto, parametro_anomalo, estado=EstadoAviso.ACTIVO, fecha_cierre=None, fecha_creacion=None):
        if not isinstance(severidad, EstadoSeveridad):
            raise TypeError("severidad debe ser una instancia de EstadoSeveridad")
        if not isinstance(estado, EstadoAviso):
            raise TypeError("estado debe ser una instancia de EstadoAviso")

        self.id_aviso=Aviso.id_counter
        Aviso.id_counter+=1
        self.severidad=severidad
        self.equipo_afectado=equipo_afectado
        self.dispositivo_que_detecto=dispositivo_que_detecto
        self.parametro_anomalo=parametro_anomalo
        self.estado=estado
        self.fecha_creacion=fecha_creacion if fecha_creacion is not None else datetime.date.today()
        self.fecha_cierre=fecha_cierre

    def cerrar_aviso(self):
        if self.estado != EstadoAviso.ACTIVO:
            raise ValueError("El aviso ya está resuelto")
        self.estado = EstadoAviso.RESUELTO
        self.fecha_cierre = datetime.date.today()

    def __repr__(self):
        return (f"Aviso(id={self.id_aviso}, severidad={self.severidad.value}, "
                f"estado={self.estado.value}, equipo={self.equipo_afectado})")

import datetime
from estados.EstadoMaquinaria import EstadoMaquinaria
class Maquinaria:
    def __init__(self,id_unico, historial, fecha_ultimo_mantenimiento:datetime.date, estado=EstadoMaquinaria.PLENAMENTE_OPERATIVA):
        self.id_unico=id_unico
        self.estado=estado
        self.historial=historial
        self.fecha_ultimo_mantenimiento=fecha_ultimo_mantenimiento

    def set_estado_maquinaria(self, nuevo_estado: EstadoMaquinaria):
        pass

    #Para el setter de plenamente operativa chequear que no hayan avisos ni programas de intervencion correctivos pendientes

    #Para el setter a plenamente operativo, pasar lo necesario a historial de eventos (Ver punto 8)
    
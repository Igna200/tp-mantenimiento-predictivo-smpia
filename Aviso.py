import datetime
class Aviso:
    id_counter=0
    def __init__ (self, id, tipo_aviso:str, equipo_afectado, dispositivo_que_detecto, parametro_anomalo, estado, fecha_cierre, fecha_creacion = datetime.now()):     #El tipo de aviso puede ser "advertencia" o "critica"
        self.id_counter=id
        id_counter+=1
        self.tipo_aviso=tipo_aviso
        self.equipo_afectado=equipo_afectado
        self.dispositivo_que_detecto=dispositivo_que_detecto
        self.parametro_anomalo=parametro_anomalo
        self.estado=estado
        self.fecha_creacion=fecha_creacion
        self.fecha_cierre=fecha_cierre

    def set_estado(self, estado):       #Metodo de instancia, no lleva decorador
        pass

    def set_estado_aviso(self, ?):      #Repasar que seria el estado aviso para saber que poner como parametro
        pass

    
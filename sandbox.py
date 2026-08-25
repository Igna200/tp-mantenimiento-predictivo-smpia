#Aqui empecemos a crear las clases:
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

class Especialidad:
    def __init__ (self, id, descripcion):
        self.id=id
        self.descripcion=descripcion

class ProgramaIntervencion:
    def __init__(self, procedimiento, componente_de_recambio, tiempo_requerido, especialidad_requerida):
        self.procedimiento=procedimiento
        self.componente_de_recambio=componente_de_recambio
        self.tiempo_requerido=tiempo_requerido
        self.especialidad_requerida=especialidad_requerida
        
class ProgramaCorrectivo:
    def __init__(self, aviso_asociado:Aviso, tipo_equipo: str):
        self.aviso_asociado = aviso_asociado  
        self.tipo_equipo = tipo_equipo

class ProgramaPreventivo:           #Un programa puede incluir mas de una maquina!!!
    def __init__ (self,periodicidad,tipo_equipo):
        self.periodicidad=periodicidad
        self.tipo_equipo=tipo_equipo        

class PersonalEspecializado:
    def __init__(self, id:int, nombre:str,especialidad:Especialidad):
        self.nombre=nombre
        self.especialidad=especialidad
        self.id=id
        
class ComponenteRecambio:
    def __init__(self,nombre:str,cantidad:str):
        self.nombre=nombre
        self.cantidad=cantidad

class Maquinaria:
    def __init__(self,id_unico,estado,historial):
        self.id_unico=id_unico
        self.estado=estado
        self.historial=historial
        
class DispositivoMedicion:
    def __init__(self, id:int,tipo_de_variable: str, umbral_limite: float, aviso_activo: bool):
        self.id = id
        self.tipo_de_variable = tipo_de_variable
        self.umbral_limite = umbral_limite
        self.aviso_activo = aviso_activo
class Eventos:           #Poner una validacion para que el evento que estamos metiendo en el historia ya esté cerrado
    def __init__(self,fecha,evento,descripcion,personal):
        self.fecha=fecha
        self.evento=evento
        self.descripcion=descripcion
        self.personal=personal

    
    
    

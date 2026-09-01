class Maquinaria:
    def __init__(self,id_unico,estado,historial):
        self.id_unico=id_unico
        self.estado=estado
        self.historial=historial

    def set_estado_maquinaria (self, estado):       #seguro habrá algo que validar antes de asignar el parametro a una instancia
        pass
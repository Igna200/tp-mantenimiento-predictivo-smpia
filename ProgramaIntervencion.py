from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from Evento import Evento
from Maquinaria import Maquinaria
import datetime
#probando

class ProgramaIntervencion:
    es_correctivo = False


    def __init__(self, maquinaria: Maquinaria, procedimiento, componentes_requeridos: dict,
                 tiempo_requerido, especialidad_requerida):
        if not isinstance(maquinaria, Maquinaria):
            raise TypeError("maquinaria debe ser una instancia de Maquinaria")

        self.maquinaria = maquinaria
        self.procedimiento = procedimiento
        self.componentes_requeridos = componentes_requeridos
        self.tiempo_requerido = tiempo_requerido
        self.especialidad_requerida = especialidad_requerida
        self.estado = EstadoProgramaIntervencion.PROGRAMADO
        self.personal_asignado = []
        self.maquinaria.agregar_programa(self)

    def chequear_stock(self):
        faltantes = []
        for componente, cantidad_necesaria in self.componentes_requeridos.items():
            if componente.cantidad < cantidad_necesaria:
                faltantes.append(componente)

        if faltantes:
            nombres = ", ".join(c.nombre for c in faltantes)
            raise ValueError(f"Stock insuficiente para: {nombres}")

        return True

    def set_estado(self, estado):
        if not isinstance(estado, EstadoProgramaIntervencion):
            raise TypeError("El estado debe ser una instancia de EstadoProgramaIntervencion")

        if estado == EstadoProgramaIntervencion.EN_EJECUCION:
            self.chequear_stock()
            for componente, cantidad_necesaria in self.componentes_requeridos.items():
                componente.descontar_stock(cantidad_necesaria)

        self.estado = estado

    def asignar_personal(self, tecnico):
        if tecnico.especialidad != self.especialidad_requerida:
            raise ValueError(
                f"Especialidad incompatible: se requiere {self.especialidad_requerida}, "
                f"el técnico tiene {tecnico.especialidad}"
            )
        self.personal_asignado.append(tecnico)

    def finalizar(self):
        if self.estado == EstadoProgramaIntervencion.COMPLETADO:
            raise ValueError("El programa ya fue completado anteriormente")

        self.estado = EstadoProgramaIntervencion.COMPLETADO

        evento = self.crear_evento_especifico()
        self.maquinaria.historial.append(evento)

        return evento
    
    def crear_evento_especifico(self):
        raise NotImplementedError("Las clases hijas deben implementar crear_evento_especifico")
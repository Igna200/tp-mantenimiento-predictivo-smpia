from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from Evento import Evento
from Maquinaria import Maquinaria
import datetime

class ProgramaIntervencion:
    es_correctivo = False   # las hijas correctivas lo pisan en True (Maquinaria lo usa para "correctivos pendientes")

    def __init__(self, maquinaria: Maquinaria,procedimiento, componentes_requeridos: dict,
                 tiempo_requerido, especialidad_requerida):
        if not isinstance(maquinaria, Maquinaria):
            raise TypeError("maquinaria debe ser una instancia de Maquinaria")

        self.maquinaria=maquinaria
        self.procedimiento = procedimiento
        self.componentes_requeridos = componentes_requeridos  # {ComponenteRecambio: cantidad}
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
            raise TypeError("El estado debe ser una instancia de Estado_ProgramaIntervencion")


    def asignar_personal():      #idem

        if estado == EstadoProgramaIntervencion.EN_EJECUCION:
            self.chequear_stock()  # levanta ValueError si falta algún componente; no se procede
            for componente, cantidad_necesaria in self.componentes_requeridos.items():
                componente.descontar_stock(cantidad_necesaria)  # reserva el stock para este programa

        self.estado = estado

    def asignar_personal(self, tecnico):
        if tecnico.especialidad != self.especialidad_requerida:
            raise ValueError(
                f"Especialidad incompatible: se requiere {self.especialidad_requerida}, "
                f"el técnico tiene {tecnico.especialidad}"
            )
        self.personal_asignado.append(tecnico)
    
    # En ProgramaIntervencion (clase base)

    def finalizar(self):
        if self.estado == EstadoProgramaIntervencion.COMPLETADO:
            raise ValueError("El programa ya fue completado anteriormente")

        self.estado = EstadoProgramaIntervencion.COMPLETADO

        evento = Evento(
            fecha=datetime.date.today(),
            descripcion=self._generar_descripcion_evento(),
            personal=self.personal_asignado,
            componentes_utilizados=list(self.componentes_requeridos.keys())
        )

        self.maquinaria.historial.append(evento)

        self._acciones_especificas_al_finalizar()

        return evento

    def generar_descripcion_evento(self):
        # Las hijas la sobreescriben; esto es un fallback
        return f"Intervención sobre {self.tipo_equipo}"

    def acciones_especificas_al_finalizar(self):
        # Las hijas la sobreescriben si necesitan hacer algo extra

        pass
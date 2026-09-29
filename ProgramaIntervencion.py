from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from Maquinaria import Maquinaria

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
            # Primero se hacen TODAS las validaciones y recién después se modifica algo
            # (stock y disponibilidad), así el programa nunca queda ejecutado a medias.

            # Regla 7: el personal también tiene que ser compatible para EJECUTAR
            if not self.personal_asignado:
                raise ValueError("No hay personal asignado para ejecutar el programa")
            for tecnico in self.personal_asignado:
                if tecnico.especialidad != self.especialidad_requerida:
                    raise ValueError(
                        f"Personal incompatible: {tecnico.nombre} no tiene la especialidad "
                        f"{self.especialidad_requerida.value}"
                    )
                # Un técnico puede estar asignado a varios programas, pero solo ejecutar
                # uno a la vez: si ya está ocupado en otro, no se arranca.
                if not tecnico.disponibilidad:
                    raise ValueError(f"{tecnico.nombre} ya está ocupado en otra intervención")
            self.chequear_stock()

            # A partir de acá ya se validó todo: se descuenta stock y se ocupa al personal
            for componente, cantidad_necesaria in self.componentes_requeridos.items():
                componente.descontar_stock(cantidad_necesaria)
            for tecnico in self.personal_asignado:
                tecnico.ocupar()

        self.estado = estado

    def asignar_personal(self, tecnico):
        if tecnico.especialidad != self.especialidad_requerida:
            raise ValueError(
                f"Especialidad incompatible: se requiere {self.especialidad_requerida}, "
                f"el técnico tiene {tecnico.especialidad}"
            )
        if not tecnico.disponibilidad:
            raise ValueError(f"{tecnico.nombre} ya está ocupado en otra intervención")
        self.personal_asignado.append(tecnico)

    def finalizar(self):
        # Solo se finaliza desde EN_EJECUCION; esto también rechaza un programa ya COMPLETADO
        if self.estado != EstadoProgramaIntervencion.EN_EJECUCION:
            raise ValueError("Solo se puede finalizar un programa que está en ejecución")

        self.estado = EstadoProgramaIntervencion.COMPLETADO

        for tecnico in self.personal_asignado:
            tecnico.liberar()

        evento = self.crear_evento_especifico()
        self.maquinaria.historial.append(evento)

        return evento
    
    def crear_evento_especifico(self):
        raise NotImplementedError("Las clases hijas deben implementar crear_evento_especifico")

    def __repr__(self):
        tipo = "Correctivo" if self.es_correctivo else "Preventivo"
        return f"Programa{tipo}(maquinaria={self.maquinaria.id_unico}, estado={self.estado.value})"
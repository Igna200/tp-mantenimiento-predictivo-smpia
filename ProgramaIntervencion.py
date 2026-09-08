from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion 
class ProgramaIntervencion:
    def __init__(self, procedimiento, componentes_requeridos: dict,
                 tiempo_requerido, especialidad_requerida):
        self.procedimiento = procedimiento
        self.componentes_requeridos = componentes_requeridos  # {ComponenteRecambio: cantidad}
        self.tiempo_requerido = tiempo_requerido
        self.especialidad_requerida = especialidad_requerida
        self.estado = EstadoProgramaIntervencion.PROGRAMADO
        self.personal_asignado = []

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
        self.estado = estado

    def asignar_personal(self, tecnico):
        if tecnico.especialidad != self.especialidad_requerida:
            raise ValueError(
                f"Especialidad incompatible: se requiere {self.especialidad_requerida}, "
                f"el técnico tiene {tecnico.especialidad}"
            )
        self.personal_asignado.append(tecnico)
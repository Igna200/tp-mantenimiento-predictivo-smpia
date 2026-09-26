import datetime
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from EventoFalla import EventoFalla

class Maquinaria:
    def __init__(self, id_unico, fecha_ultimo_mantenimiento: datetime.date = None, historial=None, estado=EstadoMaquinaria.PLENAMENTE_OPERATIVA):
        self.id_unico=id_unico
        self.estado=estado
        self.fecha_ultimo_mantenimiento=fecha_ultimo_mantenimiento
        self.historial=historial if historial is not None else []
        self.avisos=[]
        self.programas=[]
        self.dispositivos=[]

    @property
    def existe_aviso_critico_activo(self):
        return any(
            aviso.estado == EstadoAviso.ACTIVO and aviso.severidad == EstadoSeveridad.CRITICA
            for aviso in self.avisos
        )

    @property
    def existe_programa_correctivo_pendiente(self):
        return any(
            programa.es_correctivo and programa.estado != EstadoProgramaIntervencion.COMPLETADO
            for programa in self.programas
        )

    def agregar_aviso(self, aviso):
        self.avisos.append(aviso)

    def agregar_programa(self, programa):
        self.programas.append(programa)

    def agregar_dispositivo(self, dispositivo):
        self.dispositivos.append(dispositivo)

    def set_estado_maquinaria(self, nuevo_estado: EstadoMaquinaria, descripcion_falla: str = None,
                            causa: str = None, dispositivo_origen=None):
        if nuevo_estado not in EstadoMaquinaria:
            raise ValueError("El nuevo estado no es válido")

        if nuevo_estado == EstadoMaquinaria.PLENAMENTE_OPERATIVA:
            if self.existe_aviso_critico_activo or self.existe_programa_correctivo_pendiente:
                raise ValueError("Hay un aviso pendiente sin resolver")

        if nuevo_estado == EstadoMaquinaria.FALLA_DECLARADA:
            if not descripcion_falla:
                raise ValueError("Debe indicar una descripción de la falla")
            if not causa:
                raise ValueError("Debe indicar la causa de la falla")

            evento = EventoFalla(
                fecha=datetime.date.today(),
                descripcion=descripcion_falla,
                causa=causa,
                dispositivo_origen=dispositivo_origen
            )
            self.historial.append(evento)

        self.estado = nuevo_estado
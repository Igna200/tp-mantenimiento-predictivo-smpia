import datetime
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from EventoFalla import EventoFalla

class Maquinaria:
    def __init__(self, id_unico, fecha_ultimo_mantenimiento: datetime.date = None, historial=None):
        # Regla 1: el ID no puede faltar
        if id_unico is None or str(id_unico).strip() == "":
            raise ValueError("La maquinaria debe tener un ID único")
        self.id_unico=id_unico
        self.estado=EstadoMaquinaria.PLENAMENTE_OPERATIVA  # Regla 1: al registrarse, siempre operativa
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

    def set_estado_maquinaria(self, nuevo_estado: EstadoMaquinaria, **datos_falla):
        # **datos_falla (kwargs): datos opcionales que solo hacen falta al declarar una falla
        # (descripcion_falla, causa, dispositivo_origen). Para otros estados no se pasa nada,
        # así el mismo método sirve para todos los cambios de estado sin parámetros "de relleno".
        if nuevo_estado not in EstadoMaquinaria:
            raise ValueError("El nuevo estado no es válido")

        if nuevo_estado == EstadoMaquinaria.PLENAMENTE_OPERATIVA:
            if self.existe_aviso_critico_activo or self.existe_programa_correctivo_pendiente:
                raise ValueError("Hay un aviso pendiente sin resolver")

        if nuevo_estado == EstadoMaquinaria.FALLA_DECLARADA:
            # datos_falla es un diccionario: devuelve None si la clave no vino
            if not datos_falla.get("descripcion_falla"):
                raise ValueError("Debe indicar una descripción de la falla")
            if not datos_falla.get("causa"):
                raise ValueError("Debe indicar la causa de la falla")

            # Regla 8: toda falla queda registrada en el historial.
            # Se desempaqueta el diccionario con ** para pasarle a EventoFalla sus datos
            # (causa, dispositivo_origen); la descripción se saca aparte porque en Evento se llama "descripcion".
            descripcion = datos_falla.pop("descripcion_falla")
            datos_falla.setdefault("dispositivo_origen", None)  # el dispositivo es opcional
            evento = EventoFalla(fecha=datetime.date.today(), descripcion=descripcion, **datos_falla)
            self.historial.append(evento)

        self.estado = nuevo_estado
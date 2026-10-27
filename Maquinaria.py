import datetime
import re
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from EventoFalla import EventoFalla

class Maquinaria:
    # Letras, números, '-' y '_' únicamente (ej. "PRENSA-01"); nada de espacios ni símbolos.
    ID_PATTERN = re.compile(r'^[A-Za-z0-9_-]+$')

    @staticmethod
    def normalizar_id(id_unico):
        # El usuario lo puede escribir con mayúsculas o espacios de más (al registrar, al
        # buscar, da igual): siempre lo tratamos como el mismo ID. "PRENSA-01", "prensa-01"
        # y "  Prensa-01  " terminan siendo el mismo identificador interno: "prensa-01".
        if id_unico is None:
            return None
        return str(id_unico).strip().lower()

    @staticmethod
    def id_valido(id_unico):
        id_normalizado = Maquinaria.normalizar_id(id_unico)
        return id_normalizado is not None and bool(Maquinaria.ID_PATTERN.fullmatch(id_normalizado))

    def __init__(self, id_unico, fecha_ultimo_mantenimiento: datetime.date = None, historial=None):
        # Regla 1: el ID no puede faltar, y ahora además solo puede ser alfanumérico
        if not Maquinaria.id_valido(id_unico):
            raise ValueError(
                "El ID de la maquinaria debe ser alfanumérico (letras, números, '-' o '_') y no puede estar vacío"
            )
        self.id_unico=Maquinaria.normalizar_id(id_unico)
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

    def to_dict(self):
        # dispositivos, avisos, programas e historial van anidados acá porque son
        # propiedad de la maquinaria (composición): no existen por separado.
        return {
            "id_unico": self.id_unico,
            "estado": self.estado.value,
            "fecha_ultimo_mantenimiento": (
                self.fecha_ultimo_mantenimiento.isoformat() if self.fecha_ultimo_mantenimiento else None
            ),
            "dispositivos": [d.to_dict() for d in self.dispositivos],
            "avisos": [a.to_dict() for a in self.avisos],
            "programas": [p.to_dict() for p in self.programas],
            "historial": [e.to_dict() for e in self.historial],
        }

    @classmethod
    def from_dict(cls, datos):
        # Solo arma la maquinaria "pelada". Lo que le pertenece (dispositivos, avisos,
        # programas, historial) lo reconstruye SIMPIA.cargar(), porque necesita ir
        # resolviendo referencias cruzadas entre maquinarias, personal y componentes.
        fecha = datos.get("fecha_ultimo_mantenimiento")
        maquinaria = cls(
            datos["id_unico"],
            datetime.date.fromisoformat(fecha) if fecha else None,
        )
        # El constructor siempre deja la maquinaria Plenamente Operativa (Regla 1: así
        # arranca una maquinaria RECIÉN registrada). Acá no estamos registrando una
        # nueva, sino restaurando un estado que ya existía y ya fue validado antes de
        # guardarse, así que lo pisamos directo en vez de pasar por set_estado_maquinaria.
        maquinaria.estado = EstadoMaquinaria(datos["estado"])
        return maquinaria
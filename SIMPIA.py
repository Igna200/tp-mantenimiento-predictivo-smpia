from Maquinaria import Maquinaria
from PersonalEspecializado import PersonalEspecializado
from ComponenteRecambio import ComponenteRecambio
from EventoFalla import EventoFalla
from EventoCorrectivo import EventoCorrectivo
from EventoPreventivo import EventoPreventivo

class SIMPIA:
    def __init__(self):
        self.maquinas = []
        self.personal = []
        self.componentes = []

    def registrar_maquinaria(self, maquinaria: Maquinaria):
        if not isinstance(maquinaria, Maquinaria):
            raise TypeError("maquinaria debe ser una instancia de Maquinaria")
        if not maquinaria.id_unico:
            raise ValueError("La maquinaria debe tener un ID único")
        if any(m.id_unico == maquinaria.id_unico for m in self.maquinas):
            raise ValueError(f"Ya existe una maquinaria registrada con el ID {maquinaria.id_unico}")

        self.maquinas.append(maquinaria)

    def registrar_personal(self, tecnico: PersonalEspecializado):
        if not isinstance(tecnico, PersonalEspecializado):
            raise TypeError("tecnico debe ser una instancia de PersonalEspecializado")
        if any(p.id == tecnico.id for p in self.personal):
            raise ValueError(f"Ya existe personal registrado con el ID {tecnico.id}")

        self.personal.append(tecnico)

    def registrar_componente(self, componente: ComponenteRecambio):
        if not isinstance(componente, ComponenteRecambio):
            raise TypeError("componente debe ser una instancia de ComponenteRecambio")
        if any(c.id == componente.id for c in self.componentes):
            raise ValueError(f"Ya existe un componente registrado con el ID {componente.id}")

        self.componentes.append(componente)

    def registrar_evento(self, maquinaria, fecha, descripcion, **contexto):
        claves = set(contexto.keys())

        if claves == {"causa", "dispositivo_origen"}:
            evento = EventoFalla(fecha, descripcion, **contexto)
        elif claves == {"personal", "componentes_utilizados", "aviso_resuelto"}:
            evento = EventoCorrectivo(fecha, descripcion, **contexto)
        elif claves == {"programa"}:
            evento = EventoPreventivo(fecha, descripcion, **contexto)
        else:
            raise ValueError(f"No se reconoce el tipo de evento con estos datos: {claves}")

        maquinaria.historial.append(evento)
        return evento
    
    
    def listar_avisos(self):
        return [aviso for maquinaria in self.maquinas for aviso in maquinaria.avisos]

    def listar_historial_eventos(self):
        return [evento for maquinaria in self.maquinas for evento in maquinaria.historial]

    
from Maquinaria import Maquinaria
from PersonalEspecializado import PersonalEspecializado
from ComponenteRecambio import ComponenteRecambio

class SIMPIA:
    def __init__(self):
        # Diccionarios indexados por ID: búsqueda directa y control de duplicados (Regla 1)
        self.maquinas = {}      # id_unico -> Maquinaria
        self.personal = {}      # id -> PersonalEspecializado
        self.componentes = {}   # id -> ComponenteRecambio

    def registrar_maquinaria(self, maquinaria: Maquinaria):
        if not isinstance(maquinaria, Maquinaria):
            raise TypeError("maquinaria debe ser una instancia de Maquinaria")
        if not maquinaria.id_unico:
            raise ValueError("La maquinaria debe tener un ID único")
        if maquinaria.id_unico in self.maquinas:
            raise ValueError(f"Ya existe una maquinaria registrada con el ID {maquinaria.id_unico}")

        self.maquinas[maquinaria.id_unico] = maquinaria

    def registrar_personal(self, tecnico: PersonalEspecializado):
        if not isinstance(tecnico, PersonalEspecializado):
            raise TypeError("tecnico debe ser una instancia de PersonalEspecializado")
        if tecnico.id in self.personal:
            raise ValueError(f"Ya existe personal registrado con el ID {tecnico.id}")

        self.personal[tecnico.id] = tecnico

    def registrar_componente(self, componente: ComponenteRecambio):
        if not isinstance(componente, ComponenteRecambio):
            raise TypeError("componente debe ser una instancia de ComponenteRecambio")
        if componente.id in self.componentes:
            raise ValueError(f"Ya existe un componente registrado con el ID {componente.id}")

        self.componentes[componente.id] = componente

    def buscar_maquinaria(self, id_unico):
        return self.maquinas.get(id_unico)

    def buscar_personal(self, id):
        return self.personal.get(id)

    def buscar_componente(self, id):
        return self.componentes.get(id)

    def listar_avisos(self):
        return [aviso for maquinaria in self.maquinas.values() for aviso in maquinaria.avisos]

    def listar_historial_eventos(self):
        return [evento for maquinaria in self.maquinas.values() for evento in maquinaria.historial]

    
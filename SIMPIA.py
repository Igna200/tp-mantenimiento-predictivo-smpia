from Maquinaria import Maquinaria
from PersonalEspecializado import PersonalEspecializado
from ComponenteRecambio import ComponenteRecambio
from DispositivoMedicion import DispositivoMedicion
from Aviso import Aviso
from ProgramaCorrectivo import ProgramaCorrectivo
from ProgramaPreventivo import ProgramaPreventivo
from EventoFalla import EventoFalla
from EventoCorrectivo import EventoCorrectivo
from EventoPreventivo import EventoPreventivo
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
import datetime
import json

ARCHIVO_POR_DEFECTO = "datos_smpia.json"

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

    def dar_de_baja_personal(self, id, fecha_egreso: datetime.date = None):
        # Baja de un técnico que deja la empresa (despido o renuncia).
        # Devuelve el técnico, el tiempo que estuvo (años, meses, días) y los programas de los que se lo quitó.
        tecnico = self.personal.get(id)
        if tecnico is None:
            # También cubre intentar dar de baja dos veces al mismo técnico
            raise ValueError(f"No existe personal registrado con el ID {id}")
        if not tecnico.disponibilidad:
            raise ValueError(
                f"{tecnico.nombre} {tecnico.apellido} está ejecutando una intervención; "
                f"la baja se puede registrar cuando finalice"
            )

        fecha_egreso = fecha_egreso if fecha_egreso is not None else datetime.date.today()
        periodo = tecnico.tiempo_en_empresa(fecha_egreso)

        # Si estaba asignado a programas que todavía no empezaron, se lo quita para que
        # nadie que ya no pertenece a la empresa pueda ejecutarlos. Los completados no se tocan:
        # su historial tiene que seguir mostrando quién intervino.
        programas_afectados = []
        for maquinaria in self.maquinas.values():
            for programa in maquinaria.programas:
                if programa.estado == EstadoProgramaIntervencion.PROGRAMADO and tecnico in programa.personal_asignado:
                    programa.personal_asignado.remove(tecnico)
                    programas_afectados.append(programa)

        del self.personal[id]
        return tecnico, periodo, programas_afectados

    def buscar_maquinaria(self, id_unico):
        # Las claves de self.maquinas ya están normalizadas (se normalizan en Maquinaria.__init__);
        # acá normalizamos el ID buscado de la misma forma, así da igual cómo lo haya tipeado el usuario.
        return self.maquinas.get(Maquinaria.normalizar_id(id_unico))

    def buscar_personal(self, id):
        return self.personal.get(id)

    def buscar_componente(self, id):
        return self.componentes.get(id)

    def listar_avisos(self):
        return [aviso for maquinaria in self.maquinas.values() for aviso in maquinaria.avisos]

    def listar_historial_eventos(self):
        return [evento for maquinaria in self.maquinas.values() for evento in maquinaria.historial]

    # ---------- Persistencia (JSON) ----------

    def guardar(self, archivo=ARCHIVO_POR_DEFECTO):
        # componentes y personal van sueltos (no pertenecen a ninguna maquinaria); todo lo
        # demás (dispositivos, avisos, programas, historial) queda anidado dentro de "su"
        # maquinaria, porque en el modelo es composición: no existen por separado.
        datos = {
            "componentes": [c.to_dict() for c in self.componentes.values()],
            "personal": [p.to_dict() for p in self.personal.values()],
            "maquinas": [m.to_dict() for m in self.maquinas.values()],
        }
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    @classmethod
    def cargar(cls, archivo=ARCHIVO_POR_DEFECTO):
        with open(archivo, encoding="utf-8") as f:
            datos = json.load(f)

        sistema = cls()

        # 1) Componentes y personal primero: no dependen de nada más y varias cosas
        #    más adelante (programas, eventos) necesitan poder buscarlos por id.
        for d in datos.get("componentes", []):
            componente = ComponenteRecambio.from_dict(d)
            sistema.componentes[componente.id] = componente

        for d in datos.get("personal", []):
            tecnico = PersonalEspecializado.from_dict(d)
            sistema.personal[tecnico.id] = tecnico

        # 2) Maquinarias, una por una. Dentro de cada una, en ESTE orden porque cada
        #    nivel necesita que el anterior ya esté reconstruido:
        #    dispositivos -> avisos (pueden referenciar un dispositivo) ->
        #    programas (los correctivos referencian un aviso) -> historial (puede
        #    referenciar un dispositivo, un aviso o un programa, según el tipo de evento)
        for d in datos.get("maquinas", []):
            maquinaria = Maquinaria.from_dict(d)
            sistema.maquinas[maquinaria.id_unico] = maquinaria

            dispositivos_por_id = {}
            for dd in d.get("dispositivos", []):
                dispositivo = DispositivoMedicion.from_dict(dd, maquinaria)
                dispositivos_por_id[dispositivo.id] = dispositivo

            avisos_por_id = {}
            for ad in d.get("avisos", []):
                dispositivo = dispositivos_por_id.get(ad.get("dispositivo_que_detecto_id"))
                aviso = Aviso.from_dict(ad, maquinaria, dispositivo, sistema.personal)
                if dispositivo is not None:
                    # El constructor normal de Aviso hace esto mismo dentro de
                    # DispositivoMedicion.registrar_lectura(); acá hay que repetirlo a mano
                    # porque Aviso.from_dict no pasa por ese camino.
                    dispositivo.avisos_generados.append(aviso)
                avisos_por_id[aviso.id_aviso] = aviso

            for pd in d.get("programas", []):
                if pd["tipo"] == "correctivo":
                    aviso_asociado = avisos_por_id[pd["aviso_asociado_id"]]
                    ProgramaCorrectivo.from_dict(
                        pd, maquinaria, sistema.personal, sistema.componentes, aviso_asociado
                    )
                else:
                    ProgramaPreventivo.from_dict(pd, maquinaria, sistema.personal, sistema.componentes)
                # Ambos from_dict ya dejan el programa agregado a maquinaria.programas
                # (el preventivo vía su __init__ normal, el correctivo a mano).

            for ed in d.get("historial", []):
                tipo = ed["tipo_evento"]
                if tipo == "falla":
                    dispositivo_origen = dispositivos_por_id.get(ed.get("dispositivo_origen_id"))
                    evento = EventoFalla.from_dict(ed, dispositivo_origen)
                elif tipo == "correctivo":
                    aviso_resuelto = avisos_por_id[ed["aviso_resuelto_id"]]
                    evento = EventoCorrectivo.from_dict(ed, sistema.personal, sistema.componentes, aviso_resuelto)
                else:  # "preventivo"
                    programa = maquinaria.programas[ed["programa_indice"]]
                    evento = EventoPreventivo.from_dict(ed, programa, sistema.personal, sistema.componentes)
                maquinaria.historial.append(evento)

        return sistema

    
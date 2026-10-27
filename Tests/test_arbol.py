import datetime
import pytest
from arbol import ArbolAgendaPreventivos
from SIMPIA import SIMPIA
from Maquinaria import Maquinaria
from Aviso import Aviso
from PersonalEspecializado import PersonalEspecializado
from ProgramaPreventivo import ProgramaPreventivo
from ProgramaCorrectivo import ProgramaCorrectivo
from estados.Especialidad import Especialidad
from estados.EstadoSeveridad import EstadoSeveridad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion


def fecha(dia):
    return datetime.date(2026, 11, dia)


def crear_preventivo(maquina, procedimiento, fecha_programada):
    programa = ProgramaPreventivo(maquina, procedimiento, {}, 1, Especialidad.mecanico, 30, "prensa")
    programa.fecha_programada = fecha_programada
    return programa


@pytest.fixture
def agenda():
    # Se insertan desordenados a propósito: el árbol tiene que devolverlos ordenados
    maquina = Maquinaria("M-001")
    arbol = ArbolAgendaPreventivos()
    for procedimiento, dia in [("C", 15), ("A", 5), ("E", 25), ("B", 10), ("D", 20)]:
        arbol.insertar(crear_preventivo(maquina, procedimiento, fecha(dia)))
    return arbol


def test_arbol_vacio():
    arbol = ArbolAgendaPreventivos()
    assert arbol.esta_vacio()
    assert arbol.proximo() is None
    assert arbol.en_orden() == []
    assert arbol.altura() == 0


def test_en_orden_devuelve_la_agenda_ordenada_por_fecha(agenda):
    assert [p.procedimiento for _, p in agenda.en_orden()] == ["A", "B", "C", "D", "E"]
    assert agenda.tamanio == 5


def test_proximo_es_la_fecha_mas_cercana(agenda):
    fecha_proxima, programas = agenda.proximo()
    assert fecha_proxima == fecha(5)
    assert [p.procedimiento for p in programas] == ["A"]


# Dos programas el mismo día comparten nodo: el árbol no crece por eso
def test_misma_fecha_se_agrupa_en_un_nodo(agenda):
    altura_antes = agenda.altura()
    agenda.insertar(crear_preventivo(Maquinaria("M-002"), "A2", fecha(5)))

    _, programas = agenda.proximo()
    assert [p.procedimiento for p in programas] == ["A", "A2"]
    assert agenda.altura() == altura_antes
    assert agenda.tamanio == 6


def test_entre_devuelve_solo_el_rango_pedido(agenda):
    assert [p.procedimiento for _, p in agenda.entre(fecha(10), fecha(20))] == ["B", "C", "D"]
    assert [p.procedimiento for _, p in agenda.entre(hasta=fecha(9))] == ["A"]
    assert [p.procedimiento for _, p in agenda.entre(desde=fecha(21))] == ["E"]
    assert agenda.entre(fecha(11), fecha(14)) == []


# La agenda de SIMPIA incluye solo preventivos que esperan ejecutarse
def test_agenda_de_simpia_ignora_correctivos_y_programas_en_ejecucion():
    sistema = SIMPIA()
    maquina = Maquinaria("M-001")
    sistema.registrar_maquinaria(maquina)

    pendiente = crear_preventivo(maquina, "Lubricar", fecha(5))
    en_curso = crear_preventivo(maquina, "Revisar bomba", fecha(1))
    en_curso.asignar_personal(
        PersonalEspecializado(1, "Juan", "Pérez", Especialidad.mecanico, datetime.date(1985, 4, 12))
    )
    en_curso.set_estado(EstadoProgramaIntervencion.EN_EJECUCION)
    aviso = Aviso(EstadoSeveridad.CRITICA, maquina, None, "presión")
    ProgramaCorrectivo(maquina, "Cambiar junta", {}, 2, aviso, "prensa")

    agenda = sistema.agenda_preventivos()
    assert [p for _, p in agenda.en_orden()] == [pendiente]

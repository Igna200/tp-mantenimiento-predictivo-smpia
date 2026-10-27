import pytest
import datetime
from Maquinaria import Maquinaria
from ComponenteRecambio import ComponenteRecambio
from PersonalEspecializado import PersonalEspecializado
from DispositivoMedicion import DispositivoMedicion
from ProgramaCorrectivo import ProgramaCorrectivo
from ProgramaPreventivo import ProgramaPreventivo
from estados.Especialidad import Especialidad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion


def _tecnico(id=1):
    return PersonalEspecializado(id, "Juan", "Pérez", Especialidad.mecanico, datetime.date(1985, 4, 12))


def _preventivo(maquinaria, procedimiento="Lubricar"):
    return ProgramaPreventivo(maquinaria, procedimiento, {}, 1, Especialidad.mecanico, 30, "prensa")


def _correctivo(maquinaria):
    # Un correctivo necesita un aviso activo: se genera disparando una lectura por encima del umbral
    dispositivo = DispositivoMedicion(1, maquinaria, "temperatura", 80.0)
    aviso = dispositivo.registrar_lectura(95.0)
    return ProgramaCorrectivo(maquinaria, "Reparar", {}, 1, aviso, "prensa",
                              especialidad_requerida=Especialidad.mecanico)


# asignar_personal encola automáticamente, en orden
def test_asignar_personal_encola_el_programa():
    tecnico = _tecnico()
    maquinaria = Maquinaria("M-001")
    p1 = _preventivo(maquinaria, "Lubricar")
    p2 = _preventivo(maquinaria, "Calibrar")

    p1.asignar_personal(tecnico)
    p2.asignar_personal(tecnico)

    assert tecnico.cola_trabajos_pendientes.recorrer() == [p1, p2]


# ejecutar el siguiente trabajo lo inicia y lo finaliza en un solo paso
def test_ejecutar_siguiente_trabajo_inicia_y_finaliza():
    tecnico = _tecnico()
    maquinaria = Maquinaria("M-001")
    programa = _correctivo(maquinaria)
    programa.asignar_personal(tecnico)

    resultado = tecnico.get_ejecutar_siguiente_trabajo()

    assert resultado is programa
    assert programa.estado == EstadoProgramaIntervencion.COMPLETADO
    assert tecnico.cola_trabajos_pendientes.get_esta_vacia()
    assert tecnico.disponibilidad is True  # se liberó al finalizar


# Caso particular: un preventivo, al finalizar, se reprograma solo y vuelve a PROGRAMADO
# (no se queda en COMPLETADO) -> se verifica que la cola también funcione con ese ciclo
def test_ejecutar_siguiente_trabajo_con_preventivo_lo_reprograma():
    tecnico = _tecnico()
    maquinaria = Maquinaria("M-001")
    programa = _preventivo(maquinaria)
    programa.asignar_personal(tecnico)

    tecnico.get_ejecutar_siguiente_trabajo()

    assert programa.estado == EstadoProgramaIntervencion.PROGRAMADO  # reprogramado, no completado
    assert programa.fecha_ultima_ejecucion == datetime.date.today()
    assert tecnico.cola_trabajos_pendientes.get_esta_vacia()


# cola vacía da un error claro, no una excepción críptica de la cola interna
def test_ejecutar_sin_trabajos_pendientes_lanza_value_error():
    tecnico = _tecnico()
    with pytest.raises(ValueError, match="no tiene trabajos pendientes"):
        tecnico.get_ejecutar_siguiente_trabajo()


# Un correctivo con dos técnicos: si uno ya lo atendió (queda COMPLETADO para siempre),
# al otro no le explota -- se descarta solo y listo (no queda nada más pendiente)
def test_programa_ya_atendido_por_otro_tecnico_se_descarta_sin_error():
    mecanico1 = _tecnico(1)
    mecanico2 = _tecnico(2)
    maquinaria = Maquinaria("M-001")
    programa = _correctivo(maquinaria)
    programa.asignar_personal(mecanico1)
    programa.asignar_personal(mecanico2)

    mecanico1.get_ejecutar_siguiente_trabajo()  # mecanico1 lo atiende primero
    assert programa.estado == EstadoProgramaIntervencion.COMPLETADO

    # mecanico2 todavía lo tiene en su cola, pero ya no sirve de nada: se descarta solo
    with pytest.raises(ValueError, match="no tiene trabajos pendientes"):
        mecanico2.get_ejecutar_siguiente_trabajo()
    assert mecanico2.cola_trabajos_pendientes.get_esta_vacia()


# Si falla por un motivo real (acá: falta stock), el programa NO se pierde de la cola
def test_si_falla_al_iniciar_el_programa_no_se_pierde_de_la_cola():
    tecnico = _tecnico()
    maquinaria = Maquinaria("M-001")
    componente = ComponenteRecambio(1, "Rodamiento", 1)
    programa = ProgramaPreventivo(maquinaria, "Lubricar", {componente: 5}, 1,
                                  Especialidad.mecanico, 30, "prensa")  # pide 5, hay 1
    programa.asignar_personal(tecnico)

    with pytest.raises(ValueError, match="Stock insuficiente"):
        tecnico.get_ejecutar_siguiente_trabajo()

    # el programa sigue en la cola y en estado PROGRAMADO: se puede reintentar
    assert tecnico.cola_trabajos_pendientes.recorrer() == [programa]
    assert programa.estado == EstadoProgramaIntervencion.PROGRAMADO

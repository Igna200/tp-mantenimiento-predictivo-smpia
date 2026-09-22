import pytest
import datetime
from Aviso import Aviso
from Maquinaria import Maquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad


@pytest.fixture
def maquinaria_de_prueba():
    return Maquinaria(id_unico="M-001")


@pytest.fixture
def aviso_de_prueba(maquinaria_de_prueba):
    return Aviso(
        severidad=EstadoSeveridad.CRITICA,
        equipo_afectado=maquinaria_de_prueba,
        dispositivo_que_detecto=None,
        parametro_anomalo="temperatura"
    )


def test_aviso_nuevo_no_tiene_fecha_cierre(aviso_de_prueba):
    assert aviso_de_prueba.fecha_cierre is None
    assert aviso_de_prueba.estado == EstadoAviso.ACTIVO


def test_cerrar_aviso_setea_fecha_cierre(aviso_de_prueba):
    aviso_de_prueba.cerrar_aviso()

    assert aviso_de_prueba.fecha_cierre == datetime.date.today()
    assert aviso_de_prueba.estado == EstadoAviso.RESUELTO


def test_cerrar_aviso_ya_resuelto_lanza_excepcion(aviso_de_prueba):
    aviso_de_prueba.cerrar_aviso()  # primera vez: válida

    with pytest.raises(ValueError):
        aviso_de_prueba.cerrar_aviso()  # segunda vez: debe fallar
        
def test_crear_aviso_con_severidad_invalida_lanza_typeerror(maquinaria_de_prueba):
    with pytest.raises(TypeError):
        Aviso(
            severidad="critica",  # string en vez de EstadoSeveridad → inválido
            equipo_afectado=maquinaria_de_prueba,
            dispositivo_que_detecto=None,
            parametro_anomalo="temperatura"
        )
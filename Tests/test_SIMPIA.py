import pytest
import datetime
from SIMPIA import SIMPIA
from Maquinaria import Maquinaria
from PersonalEspecializado import PersonalEspecializado
from ProgramaPreventivo import ProgramaPreventivo
from estados.Especialidad import Especialidad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion


@pytest.fixture
def sistema_con_tecnico():
    sistema = SIMPIA()
    sistema.registrar_maquinaria(Maquinaria("M-001"))
    sistema.registrar_personal(
        PersonalEspecializado(1, "Juan", "Pérez", Especialidad.mecanico, datetime.date(1985, 4, 12),
                              fecha_ingreso=datetime.date(2015, 3, 2))
    )
    return sistema


def test_dar_de_baja_quita_al_tecnico_y_devuelve_el_periodo(sistema_con_tecnico):
    tecnico, periodo, _ = sistema_con_tecnico.dar_de_baja_personal(1, datetime.date(2026, 10, 13))

    assert tecnico.nombre == "Juan"
    assert periodo == (11, 7, 11)
    assert sistema_con_tecnico.buscar_personal(1) is None


# No se puede dar de baja dos veces al mismo técnico
def test_dar_de_baja_dos_veces_lanza_value_error(sistema_con_tecnico):
    sistema_con_tecnico.dar_de_baja_personal(1)

    with pytest.raises(ValueError):
        sistema_con_tecnico.dar_de_baja_personal(1)


def test_no_se_puede_dar_de_baja_a_un_tecnico_ocupado(sistema_con_tecnico):
    sistema_con_tecnico.buscar_personal(1).ocupar()

    with pytest.raises(ValueError):
        sistema_con_tecnico.dar_de_baja_personal(1)
    assert sistema_con_tecnico.buscar_personal(1) is not None


# Al darlo de baja se lo quita de los programas que todavía no empezaron
def test_dar_de_baja_lo_quita_de_programas_programados(sistema_con_tecnico):
    maquina = sistema_con_tecnico.buscar_maquinaria("M-001")
    tecnico = sistema_con_tecnico.buscar_personal(1)
    programa = ProgramaPreventivo(maquina, "Lubricar", {}, 1, Especialidad.mecanico, 30, "prensa")
    programa.asignar_personal(tecnico)

    _, _, afectados = sistema_con_tecnico.dar_de_baja_personal(1)

    assert programa.personal_asignado == []
    assert afectados == [programa]
    assert programa.estado == EstadoProgramaIntervencion.PROGRAMADO

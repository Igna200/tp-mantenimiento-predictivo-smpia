import pytest
import datetime
from Maquinaria import Maquinaria
from ComponenteRecambio import ComponenteRecambio
from PersonalEspecializado import PersonalEspecializado
from ProgramaPreventivo import ProgramaPreventivo
from estados.Especialidad import Especialidad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion


@pytest.fixture
def programa_y_componente():
    componente = ComponenteRecambio(1, "Rodamiento", 10)
    programa = ProgramaPreventivo(Maquinaria("M-001"), "Lubricar", {componente: 3}, 1,
                                  Especialidad.mecanico, 30, "prensa")
    programa.asignar_personal(
        PersonalEspecializado(1, "Juan", "Pérez", Especialidad.mecanico, datetime.date(1985, 4, 12))
    )
    return programa, componente


# Iniciar dos veces el mismo programa no debe descontar el stock dos veces
def test_iniciar_programa_en_ejecucion_lanza_value_error_sin_descontar_stock(programa_y_componente):
    programa, componente = programa_y_componente
    programa.set_estado(EstadoProgramaIntervencion.EN_EJECUCION)
    assert componente.get_stock() == 7

    with pytest.raises(ValueError):
        programa.set_estado(EstadoProgramaIntervencion.EN_EJECUCION)
    assert componente.get_stock() == 7


def test_asignar_tecnico_de_otra_especialidad_lanza_value_error(programa_y_componente):
    programa, _ = programa_y_componente
    hidraulico = PersonalEspecializado(2, "Lucía", "Gómez", Especialidad.hidraulico, datetime.date(1990, 9, 3))

    with pytest.raises(ValueError, match="HIDRAULICO"):
        programa.asignar_personal(hidraulico)

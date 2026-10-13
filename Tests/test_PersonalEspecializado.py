import pytest
import datetime
from PersonalEspecializado import PersonalEspecializado
from estados.Especialidad import Especialidad


def crear_tecnico(fecha_ingreso):
    return PersonalEspecializado(1, "Lucía", "Gómez", Especialidad.hidraulico,
                                 datetime.date(1990, 9, 3), fecha_ingreso=fecha_ingreso)


def test_tiempo_en_empresa_en_anios_meses_y_dias():
    tecnico = crear_tecnico(datetime.date(2019, 7, 15))
    assert tecnico.tiempo_en_empresa(datetime.date(2026, 10, 20)) == (7, 3, 5)


# Si el día de egreso es menor al de ingreso, el mes todavía no se completó
def test_tiempo_en_empresa_con_mes_incompleto():
    tecnico = crear_tecnico(datetime.date(2025, 1, 31))
    assert tecnico.tiempo_en_empresa(datetime.date(2025, 3, 1)) == (0, 1, 1)


def test_sin_fecha_de_ingreso_toma_hoy():
    tecnico = crear_tecnico(None)
    assert tecnico.fecha_ingreso == datetime.date.today()
    assert tecnico.tiempo_en_empresa() == (0, 0, 0)


def test_fecha_de_ingreso_futura_lanza_value_error():
    with pytest.raises(ValueError):
        crear_tecnico(datetime.date.today() + datetime.timedelta(days=1))

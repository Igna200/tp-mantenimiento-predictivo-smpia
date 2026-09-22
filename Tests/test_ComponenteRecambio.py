import pytest
from ComponenteRecambio import ComponenteRecambio


@pytest.fixture
def componente_de_prueba():
    return ComponenteRecambio(id=1, nombre="Junta hidráulica", cantidad=10)


def test_get_stock_devuelve_cantidad_correcta(componente_de_prueba):
    assert componente_de_prueba.get_stock() == 10


def test_descontar_stock_con_stock_suficiente(componente_de_prueba):
    componente_de_prueba.descontar_stock(4)
    assert componente_de_prueba.get_stock() == 6


def test_descontar_stock_mayor_al_disponible_lanza_excepcion(componente_de_prueba):
    with pytest.raises(ValueError):
        componente_de_prueba.descontar_stock(15)


def test_descontar_stock_exacto_deja_cantidad_en_cero(componente_de_prueba):
    componente_de_prueba.descontar_stock(10)
    assert componente_de_prueba.get_stock() == 0


def test_agregar_stock_suma_correctamente(componente_de_prueba):
    componente_de_prueba.setter_agregar_stock(5)
    assert componente_de_prueba.get_stock() == 15


def test_agregar_stock_cantidad_cero_lanza_excepcion(componente_de_prueba):
    with pytest.raises(ValueError):
        componente_de_prueba.setter_agregar_stock(0)


def test_agregar_stock_cantidad_negativa_lanza_excepcion(componente_de_prueba):
    with pytest.raises(ValueError):
        componente_de_prueba.setter_agregar_stock(-3)


def test_descontar_stock_con_valor_negativo_lanza_excepcion(componente_de_prueba):
    with pytest.raises(ValueError):
        componente_de_prueba.descontar_stock(-5)
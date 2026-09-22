import pytest
from DispositivoMedicion import DispositivoMedicion
from Maquinaria import Maquinaria  # <--- Usamos la clase real
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad

def test_lectura_maquinaria_no_operativa_lanza_value_error():
    maquina = Maquinaria(id_unico=101)
    maquina.estado = EstadoMaquinaria.FALLA_DECLARADA
    dispositivo = DispositivoMedicion(
        id=1, maquinaria=maquina, tipo_de_variable="Temperatura", umbral_limite=80.0
    )

    with pytest.raises(ValueError):
        dispositivo.registrar_lectura(85.0)

def test_lectura_supera_umbral_crea_aviso():
    maquina = Maquinaria(id_unico=101)
    dispositivo = DispositivoMedicion(
        id=1, maquinaria=maquina, tipo_de_variable="Temperatura", umbral_limite=80.0
    )

    aviso_creado = dispositivo.registrar_lectura(90.0)

    assert aviso_creado is not None
    assert len(dispositivo.avisos_generados) == 1
    assert dispositivo.avisos_generados[0].severidad == EstadoSeveridad.CRITICA

def test_lectura_supera_umbral_con_aviso_activo_no_duplica():
    maquina = Maquinaria(id_unico=101)
    dispositivo = DispositivoMedicion(
        id=1, maquinaria=maquina, tipo_de_variable="Temperatura", umbral_limite=80.0
    )

    dispositivo.registrar_lectura(90.0)
    assert len(dispositivo.avisos_generados) == 1

    segundo_aviso = dispositivo.registrar_lectura(95.0)
    assert segundo_aviso is None
    assert len(dispositivo.avisos_generados) == 1
import pytest
from Maquinaria import Maquinaria
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad
from EventoFalla import EventoFalla




# TEST 1: Bloqueo por aviso crítico 
def test_bloqueo_plenamente_operativa_por_aviso_critico():
   maquina = Maquinaria(id_unico=101)
   maquina.estado = EstadoMaquinaria.FALLA_DECLARADA


   class MockAviso:
       estado = EstadoAviso.ACTIVO
       severidad = EstadoSeveridad.CRITICA


   maquina.agregar_aviso(MockAviso())


   with pytest.raises(ValueError):
       maquina.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)




# TEST 2: Intento de usar un estado inexistente/inválido
def test_cambio_estado_invalido_lanza_value_error():
   maquina = Maquinaria(id_unico=101)
  
   with pytest.raises(ValueError):
       maquina.set_estado_maquinaria("ESTADO_INEXISTENTE")




def test_cambio_estado_exitoso_sin_bloqueos():
    maquina = Maquinaria(id_unico=101)

    # Le pasamos la descripción y la causa requerida para EventoFalla
    maquina.set_estado_maquinaria(
        EstadoMaquinaria.FALLA_DECLARADA,
        descripcion_falla="Filtro tapado",
        causa="Acumulacion de residuos en el filtro"
    )
    assert maquina.estado == EstadoMaquinaria.FALLA_DECLARADA
    assert len(maquina.historial) == 1  # Verifica que registró el Evento en el historial
    assert isinstance(maquina.historial[0], EventoFalla)
    
    # Volvemos a PLENAMENTE_OPERATIVA (como no hay bloqueos, debe funcionar)
    maquina.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
    assert maquina.estado == EstadoMaquinaria.PLENAMENTE_OPERATIVA


# TEST kwargs: los datos de la falla llegan como diccionario y se desempaquetan con **
def test_falla_con_kwargs_desempaquetados_desde_diccionario():
    maquina = Maquinaria(id_unico=101)
    datos_falla = {
        "descripcion_falla": "Sobrecalentamiento",
        "causa": "Ventilador roto",
        "dispositivo_origen": "sensor-temp-1",
    }

    maquina.set_estado_maquinaria(EstadoMaquinaria.FALLA_DECLARADA, **datos_falla)

    evento = maquina.historial[0]
    assert evento.descripcion == "Sobrecalentamiento"
    assert evento.causa == "Ventilador roto"
    assert evento.dispositivo_origen == "sensor-temp-1"


# TEST kwargs: si falta un dato obligatorio de la falla, no cambia el estado
def test_falla_sin_causa_lanza_value_error():
    maquina = Maquinaria(id_unico=101)

    with pytest.raises(ValueError):
        maquina.set_estado_maquinaria(EstadoMaquinaria.FALLA_DECLARADA, descripcion_falla="Filtro tapado")

    assert maquina.estado == EstadoMaquinaria.PLENAMENTE_OPERATIVA
    assert maquina.historial == []
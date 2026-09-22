import pytest
from Maquinaria import Maquinaria
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad




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

    # Le pasamos tanto la descripción como la lista de personal requerida
    maquina.set_estado_maquinaria(
        EstadoMaquinaria.FALLA_DECLARADA,
        descripcion_falla="Filtro tapado",
        personal=["Tecnico_01"]
    )
    assert maquina.estado == EstadoMaquinaria.FALLA_DECLARADA
    assert len(maquina.historial) == 1  # Verifica que registró el Evento en el historial

    # Volvemos a PLENAMENTE_OPERATIVA (como no hay bloqueos, debe funcionar)
    maquina.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
    assert maquina.estado == EstadoMaquinaria.PLENAMENTE_OPERATIVA
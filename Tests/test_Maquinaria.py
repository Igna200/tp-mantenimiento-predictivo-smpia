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




# TEST 3: Transición exitosa de estados sin bloqueos
def test_cambio_estado_exitoso_sin_bloqueos():
   maquina = Maquinaria(id_unico=101)
  
   # 1. Cambiamos de PLENAMENTE_OPERATIVA a FALLA_DECLARADA
   maquina.set_estado_maquinaria(EstadoMaquinaria.FALLA_DECLARADA)
   assert maquina.estado == EstadoMaquinaria.FALLA_DECLARADA


   # 2. Volvemos a PLENAMENTE_OPERATIVA (como no hay avisos pendientes, debe permitirlo)
   maquina.set_estado_maquinaria(EstadoMaquinaria.PLENAMENTE_OPERATIVA)
   assert maquina.estado == EstadoMaquinaria.PLENAMENTE_OPERATIVA

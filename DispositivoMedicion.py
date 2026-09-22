from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoSeveridad import EstadoSeveridad
from Aviso import Aviso
class DispositivoMedicion:
    def __init__(self, id: int, maquinaria, tipo_de_variable: str, umbral_limite: float):
        self.id = id
        self.maquinaria = maquinaria
        self.tipo_de_variable = tipo_de_variable
        self.umbral_limite = umbral_limite
        self.avisos_generados = []  # reemplaza al booleano aviso_activo

    def hay_aviso_critico_activo(self):
        return any(
            aviso.estado == EstadoAviso.ACTIVO and aviso.severidad == EstadoSeveridad.CRITICA
            for aviso in self.avisos_generados
        )

    def registrar_lectura(self, valor: float):
        # Regla 3: no se puede registrar si la maquinaria no está operativa
        if self.maquinaria.estado != EstadoMaquinaria.PLENAMENTE_OPERATIVA:
            raise ValueError(
                f"No se puede registrar lectura: la maquinaria {self.maquinaria.id_unico} "
                f"está en estado {self.maquinaria.estado.value}"
            )

        # Regla 2: si supera el umbral y no hay ya un aviso crítico activo, generar uno nuevo
        if valor > self.umbral_limite:
            if not self.hay_aviso_critico_activo():
                nuevo_aviso = Aviso(
                    severidad=EstadoSeveridad.CRITICA,
                    equipo_afectado=self.maquinaria,
                    dispositivo_que_detecto=self,
                    parametro_anomalo=self.tipo_de_variable,
                )
                self.avisos_generados.append(nuevo_aviso)
                return nuevo_aviso
            else:
                print("Ya existe un aviso crítico activo para este dispositivo, no se genera uno nuevo.")
                return None

        return None

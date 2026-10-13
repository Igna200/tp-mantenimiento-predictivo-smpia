from Evento import Evento
from ComponenteRecambio import ComponenteRecambio
import datetime

class EventoCorrectivo(Evento):
    def __init__(self, fecha: datetime.date, descripcion: str,
                 personal: list, componentes_utilizados: dict, aviso_resuelto):
        super().__init__(fecha, descripcion)
        if not personal:
            raise ValueError("El evento correctivo debe tener al menos un miembro del personal asociado")

        self.personal = personal
        # Diccionario componente -> cantidad usada, para que el historial muestre cuánto se usó (Regla 8)
        self.componentes_utilizados = componentes_utilizados if componentes_utilizados is not None else {}
        self.aviso_resuelto = aviso_resuelto

    def __str__(self):
        nombres_personal = ", ".join(p.nombre for p in self.personal)
        nombres_componentes = ", ".join(f"{c.nombre} x{n}" for c, n in self.componentes_utilizados.items()) or "ninguno"
        return (f"{super().__str__()} | Personal: {nombres_personal} | "
                f"Componentes: {nombres_componentes}")

    def to_dict(self):
        datos = super().to_dict()
        datos["tipo_evento"] = "correctivo"
        datos["personal_ids"] = [p.id for p in self.personal]
        datos["componentes_utilizados"] = ComponenteRecambio.serializar_requeridos(self.componentes_utilizados)
        # El aviso tiene id propio (global, no por maquinaria): lo usamos para referenciarlo
        datos["aviso_resuelto_id"] = self.aviso_resuelto.id_aviso
        return datos

    @classmethod
    def from_dict(cls, datos, personal_por_id, componentes_por_id, aviso_resuelto):
        return cls(
            fecha=datetime.date.fromisoformat(datos["fecha"]),
            descripcion=datos["descripcion"],
            personal=[personal_por_id[pid] for pid in datos["personal_ids"]],
            componentes_utilizados=ComponenteRecambio.deserializar_requeridos(
                datos["componentes_utilizados"], componentes_por_id
            ),
            aviso_resuelto=aviso_resuelto,
        )
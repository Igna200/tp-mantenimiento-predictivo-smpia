class ComponenteRecambio:
    def __init__(self,id:int, nombre:str,cantidad:int):
        self.id=id
        self.nombre=nombre
        self.cantidad=cantidad

    def get_stock(self):
        return self.cantidad

    def descontar_stock(self, cantidad_descontar: int):
        if cantidad_descontar <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor a cero")
        if self.cantidad - cantidad_descontar < 0:
            raise ValueError("No hay suficiente stock disponible para realizar la operación")
        self.cantidad -= cantidad_descontar
    
    def setter_agregar_stock(self, cantidad_a_sumar:int):
        if cantidad_a_sumar <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor a cero.")
        self.cantidad += cantidad_a_sumar

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "cantidad": self.cantidad}

    @classmethod
    def from_dict(cls, datos):
        return cls(datos["id"], datos["nombre"], datos["cantidad"])

    @staticmethod
    def serializar_requeridos(componentes_requeridos):
        # {ComponenteRecambio: cantidad} -> [{"componente_id": id, "cantidad": n}, ...]
        # En JSON las claves de un objeto tienen que ser strings; un ComponenteRecambio
        # no sirve como clave, por eso se guarda como una lista de pares.
        return [{"componente_id": c.id, "cantidad": n} for c, n in componentes_requeridos.items()]

    @staticmethod
    def deserializar_requeridos(lista, componentes_por_id):
        return {componentes_por_id[item["componente_id"]]: item["cantidad"] for item in lista}
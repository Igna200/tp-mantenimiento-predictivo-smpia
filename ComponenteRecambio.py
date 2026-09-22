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
class ComponenteRecambio:
    def __init__(self,id:int, nombre:str,cantidad:int):
        self.id=id
        self.nombre=nombre
        self.cantidad=cantidad

    def get_stock(self):
        return self.cantidad

    def actualizar_stock(self):
        pass
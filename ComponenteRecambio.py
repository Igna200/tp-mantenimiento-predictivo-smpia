class ComponenteRecambio:
    def __init__(self,nombre:str,cantidad:int):
        self.nombre=nombre
        self.cantidad=cantidad


    def get_stock(self):
        return self.cantidad

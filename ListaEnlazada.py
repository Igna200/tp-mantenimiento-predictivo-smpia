class nodo:
    def __init__(self, dato):
        self.dato=dato
        self.siguiente=None

    def getter_nodo(self):
        return self.dato

    def getter_siguiente(self):
        return self.siguiente

    def setter_nodo(self, set):
        self.dato=set


class ListaEnlazada:
    def __init__ (self):
        self.cabeza=None

    def esta_vacia(self):
        return self.cabeza is None

    def longitud (self):
        long_counter=0
        actual=self.cabeza
        while actual is not None:
            long_counter+=1
            actual=actual.siguiente
        return long_counter

    def getter_by_posicion(self, indice_pedido):
        if indice_pedido >= self.longitud():
            raise IndexError ("Fuera de rango")
        pos_actual=0
        actual=self.cabeza
        while pos_actual != indice_pedido:
            pos_actual+=1
            actual=actual.siguiente
        return actual.dato


    #Falta insertar nodos, eliminar nodos, etc
    # Ver presentacion
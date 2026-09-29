class Nodo:
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

    def insertar_inicio (self, dato):
        nuevo_nodo=Nodo(dato)
        nuevo_nodo.siguiente=self.cabeza
        self.cabeza=nuevo_nodo

    def insertar_final (self, dato):
        nuevo_nodo=Nodo(dato)
        actual=self.cabeza
        if actual is None:
            self.insertar_inicio(dato)
            return
        while actual.siguiente is not None:
            actual=actual.siguiente
        actual.siguiente=nuevo_nodo

    def eliminar_primero (self):
        if self.cabeza is None:
            raise IndexError ("La lista seleccionada está vacía")
        self.cabeza=self.cabeza.siguiente

    def eliminar_ultimo(self):
        actual=self.cabeza
        if actual is None:
            raise IndexError("Lista vacía")
        if actual.siguiente is None:
            self.eliminar_primero()
            return
        while actual.siguiente.siguiente is not None:
            actual=actual.siguiente
        actual.siguiente=None

    def buscar_posicion(self, valor):
        if self.cabeza is None:
            raise IndexError ("Lista vacía")
        actual=self.cabeza
        posicion=0
        while actual.dato != valor:
            if actual.siguiente is None:
                raise ValueError ("No se encontró el valor pedido")
            actual=actual.siguiente
            posicion+=1
        return f"Posicion del valor: {posicion}"
        



    #Falta insertar nodos, eliminar nodos, etc
    # Ver presentacion
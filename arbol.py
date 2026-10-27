import datetime


class NodoArbol:
    """Nodo del árbol: una fecha y todos los programas que vencen ese día."""
    def __init__(self, fecha: datetime.date, programa):
        self.fecha = fecha              # clave por la que se ordena el árbol
        self.programas = [programa]     # varios programas pueden vencer el mismo día
        self.izquierdo = None           # fechas anteriores
        self.derecho = None             # fechas posteriores


class ArbolAgendaPreventivos:
    """Árbol binario de búsqueda (ABB) de programas preventivos, ordenado por fecha_programada.

    Regla del ABB: en cada nodo, todo lo que está a la izquierda tiene una fecha anterior
    y todo lo que está a la derecha, una fecha posterior. Gracias a eso:
      - el próximo mantenimiento es el nodo de más a la izquierda (no hay que recorrer todo),
      - recorrerlo "en orden" (izquierda, nodo, derecha) da la agenda ordenada por fecha,
      - para buscar un rango de fechas se descartan ramas enteras que quedan fuera del rango.
    """
    def __init__(self):
        self.raiz = None
        self.tamanio = 0    # cantidad de programas (no de nodos)

    def esta_vacio(self) -> bool:
        return self.raiz is None

    def insertar(self, programa):
        """Agrega un programa en la posición que le corresponde según su fecha_programada."""
        fecha = programa.fecha_programada
        self.tamanio += 1
        if self.raiz is None:
            self.raiz = NodoArbol(fecha, programa)
            return

        actual = self.raiz
        while True:
            if fecha == actual.fecha:
                # Misma fecha: no se crea otro nodo, se suma a la lista de ese día
                actual.programas.append(programa)
                return
            if fecha < actual.fecha:
                if actual.izquierdo is None:
                    actual.izquierdo = NodoArbol(fecha, programa)
                    return
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = NodoArbol(fecha, programa)
                    return
                actual = actual.derecho

    def proximo(self):
        """Devuelve (fecha, programas) del vencimiento más cercano, o None si el árbol está vacío.
        Es el nodo de más a la izquierda: se baja siempre por la izquierda."""
        if self.raiz is None:
            return None
        actual = self.raiz
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual.fecha, actual.programas

    def en_orden(self):
        """Lista de (fecha, programa) de todo el árbol, ordenada por fecha."""
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        # Recorrido recursivo: primero las fechas anteriores, después este nodo, después las posteriores
        if nodo is None:
            return
        self._en_orden(nodo.izquierdo, resultado)
        for programa in nodo.programas:
            resultado.append((nodo.fecha, programa))
        self._en_orden(nodo.derecho, resultado)

    def entre(self, desde: datetime.date = None, hasta: datetime.date = None):
        """Lista ordenada de (fecha, programa) con desde <= fecha <= hasta.
        Si desde o hasta son None, el rango queda abierto de ese lado."""
        resultado = []
        self._entre(self.raiz, desde, hasta, resultado)
        return resultado

    def _entre(self, nodo, desde, hasta, resultado):
        if nodo is None:
            return
        # Solo se baja a la izquierda si ahí puede haber fechas dentro del rango
        # (si este nodo ya es anterior a "desde", todo su subárbol izquierdo también lo es)
        if desde is None or nodo.fecha > desde:
            self._entre(nodo.izquierdo, desde, hasta, resultado)
        if (desde is None or nodo.fecha >= desde) and (hasta is None or nodo.fecha <= hasta):
            for programa in nodo.programas:
                resultado.append((nodo.fecha, programa))
        # Igual para la derecha: si este nodo ya es posterior a "hasta", no hace falta seguir
        if hasta is None or nodo.fecha < hasta:
            self._entre(nodo.derecho, desde, hasta, resultado)

    def altura(self):
        """Cantidad de niveles del árbol (0 si está vacío)."""
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

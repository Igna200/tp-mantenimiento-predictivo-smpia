from ListaEnlazada import Nodo

class ColaProgramasTrabajo:
    """Cola (FIFO) basada en Nodos para gestionar el plan de trabajo del personal."""
    def __init__(self):
        self.frente = None  # Apunta al primer programa ingresado (el que sale primero)
        self.final = None   # Apunta al último programa ingresado (donde se encola)
        self.tamanio = 0

    def set_encolar_programa(self, programa):
        """Método setter (Enqueue): Agrega un programa al final de la cola."""
        nuevo_nodo = Nodo(programa)
        if self.final is None:  # Si la cola estaba vacía
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.tamanio += 1

    def get_desencolar_programa(self):
        """Método getter (Dequeue): Extrae y retorna el programa más antiguo pendiente."""
        if self.frente is None:
            raise ValueError("No hay programas pendientes en la cola de trabajo.")

        programa_atender = self.frente.dato
        self.frente = self.frente.siguiente
        
        if self.frente is None:  # Si la cola quedó vacía tras la extracción
            self.final = None
            
        self.tamanio -= 1
        return programa_atender

    def get_proximo_programa(self):
        """Método getter (Front): Consulta el programa en el frente sin sacarlo."""
        if self.frente is None:
            return None
        return self.frente.dato

    def get_esta_vacia(self) -> bool:
        """Método getter: Indica si la cola no tiene trabajos pendientes."""
        return self.frente is None
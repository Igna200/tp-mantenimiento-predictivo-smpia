import datetime
import calendar
from estados.Especialidad import Especialidad
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from cola import ColaProgramasTrabajo
class PersonalEspecializado:
    def __init__(self, id:int, nombre:str,apellido: str, especialidad:Especialidad, fecha_nacimiento: datetime.date, disponibilidad:bool = True, fecha_ingreso: datetime.date = None):
        self.nombre=nombre
        self.apellido=apellido
        self.especialidad=especialidad
        self.id=id
        self.fecha_nacimiento= fecha_nacimiento
        self.disponibilidad=disponibilidad
        # Fecha en que entró a la empresa; si no se indica, se toma hoy.
        # Se usa para calcular cuánto tiempo estuvo cuando se lo da de baja.
        self.fecha_ingreso = fecha_ingreso if fecha_ingreso is not None else datetime.date.today()
        if self.fecha_ingreso > datetime.date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        # Cola FIFO de programas pendientes de atender (se van sumando al asignarlo a un
        # programa con ProgramaIntervencion.asignar_personal). Arranca siempre vacía; si se
        # está restaurando desde un archivo guardado, SIMPIA.cargar() la vuelve a llenar
        # en una segunda pasada (necesita que las maquinarias ya existan).
        self.cola_trabajos_pendientes = ColaProgramasTrabajo()

    def ocupar(self):

        if not self.disponibilidad:
            raise ValueError(f"El personal {self.nombre} {self.apellido} ya está ocupado.")
        self.disponibilidad = False

    def liberar(self):

        self.disponibilidad = True

    @staticmethod
    def _sumar_meses(fecha: datetime.date, meses: int):
        # Suma meses a una fecha. Si el día no existe en el mes de destino (ej. 31 de febrero),
        # se usa el último día de ese mes. calendar.monthrange devuelve cuántos días tiene el mes.
        anio = fecha.year + (fecha.month - 1 + meses) // 12
        mes = (fecha.month - 1 + meses) % 12 + 1
        dia = min(fecha.day, calendar.monthrange(anio, mes)[1])
        return datetime.date(anio, mes, dia)

    def tiempo_en_empresa(self, fecha_hasta: datetime.date = None):
        # Devuelve (años, meses, días) desde la fecha de ingreso hasta fecha_hasta (por defecto, hoy).
        # Primero cuenta los meses completos y después los días que sobran.
        fecha_hasta = fecha_hasta if fecha_hasta is not None else datetime.date.today()
        if fecha_hasta < self.fecha_ingreso:
            raise ValueError("La fecha de egreso no puede ser anterior a la de ingreso")

        meses = (fecha_hasta.year - self.fecha_ingreso.year) * 12 + (fecha_hasta.month - self.fecha_ingreso.month)
        # Si todavía no se llegó al día del mes en que ingresó, el último mes no está completo
        if self._sumar_meses(self.fecha_ingreso, meses) > fecha_hasta:
            meses -= 1
        dias = (fecha_hasta - self._sumar_meses(self.fecha_ingreso, meses)).days

        return meses // 12, meses % 12, dias

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "especialidad": self.especialidad.value,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "disponibilidad": self.disponibilidad,
            "fecha_ingreso": self.fecha_ingreso.isoformat(),
            # ProgramaIntervencion no tiene id propio: cada pendiente se referencia por
            # su maquinaria + la posición en maquinaria.programas (igual que EventoPreventivo).
            "cola_trabajos_pendientes": [
                {"maquinaria_id": p.maquinaria.id_unico, "programa_indice": p.maquinaria.programas.index(p)}
                for p in self.cola_trabajos_pendientes.recorrer()
            ],
        }

    @classmethod
    def from_dict(cls, datos):
        # El constructor normal no tiene ninguna regla de negocio que pueda rechazar
        # un estado ya guardado (disponibilidad y fecha_ingreso se aceptan tal cual),
        # así que alcanza con llamarlo directo.
        return cls(
            datos["id"], datos["nombre"], datos["apellido"],
            Especialidad(datos["especialidad"]),
            datetime.date.fromisoformat(datos["fecha_nacimiento"]),
            disponibilidad=datos["disponibilidad"],
            fecha_ingreso=datetime.date.fromisoformat(datos["fecha_ingreso"]),
        )

    def set_asignar_programa_a_cola(self, programa):
        """Encola el programa de trabajo en la Cola FIFO del técnico."""
        # Se asume que la verificación de especialidad/compatibilidad ya fue realizada previamente
        self.cola_trabajos_pendientes.set_encolar_programa(programa)

    def get_ejecutar_siguiente_trabajo(self):
        """Atiende el próximo programa pendiente de la cola: lo inicia y lo finaliza.

        Un mismo programa puede tener varios técnicos asignados (cada uno con el programa
        en su propia cola); si otro técnico ya lo inició o finalizó, ya no sirve de nada acá
        -> se descarta sin avisar y se sigue con el próximo. Si falla por otro motivo real
        (falta stock, otro técnico asignado está ocupado, etc.) el programa NO se pierde:
        queda al frente de la cola para reintentar más tarde, en vez de desaparecer.
        """
        while True:
            if self.cola_trabajos_pendientes.get_esta_vacia():
                raise ValueError(f"{self.nombre} {self.apellido} no tiene trabajos pendientes.")

            programa = self.cola_trabajos_pendientes.get_proximo_programa()
            if programa.estado != EstadoProgramaIntervencion.PROGRAMADO:
                # Quedó obsoleto: otro técnico asignado al mismo programa ya lo atendió.
                self.cola_trabajos_pendientes.get_desencolar_programa()
                continue

            programa.set_estado(EstadoProgramaIntervencion.EN_EJECUCION)  # puede fallar (stock, otro técnico ocupado)
            self.cola_trabajos_pendientes.get_desencolar_programa()  # recién se saca si arrancó bien
            programa.finalizar()
            return programa
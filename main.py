import datetime
import json
from Maquinaria import Maquinaria
from DispositivoMedicion import DispositivoMedicion
from PersonalEspecializado import PersonalEspecializado
from ComponenteRecambio import ComponenteRecambio
from ProgramaPreventivo import ProgramaPreventivo
from ProgramaCorrectivo import ProgramaCorrectivo
from SIMPIA import SIMPIA, ARCHIVO_POR_DEFECTO
from estados.EstadoMaquinaria import EstadoMaquinaria
from estados.EstadoAviso import EstadoAviso
from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
from estados.Especialidad import Especialidad

# Orden del archivo: 1) imports  2) definición de funciones  3) main(), que las llama.
# Las funciones reciben el sistema como parámetro en lugar de usar una variable global.


# ---------- Funciones auxiliares para pedir datos ----------
# Todas repiten la pregunta mientras el dato sea inválido.
# Si el usuario deja el dato vacío devuelven None, que significa "cancelar".

def pedir_texto(mensaje):
    valor = input(mensaje).strip()
    return valor if valor else None


def pedir_entero(mensaje, minimo=None):
    while True:
        respuesta = input(mensaje).strip()
        if not respuesta:
            return None
        try:
            numero = int(respuesta)
        except ValueError:
            print("Debe ingresar un número entero.")
            continue
        if minimo is not None and numero < minimo:
            print(f"El número debe ser mayor o igual a {minimo}.")
            continue
        return numero


def pedir_decimal(mensaje, minimo=None):
    while True:
        respuesta = input(mensaje).strip()
        if not respuesta:
            return None
        try:
            numero = float(respuesta)
        except ValueError:
            print("Debe ingresar un número (use punto para los decimales, ej. 1.5).")
            continue
        if minimo is not None and numero < minimo:
            print(f"El número debe ser mayor o igual a {minimo}.")
            continue
        return numero


def pedir_fecha(mensaje):
    # Formato AAAA-MM-DD; no se aceptan fechas futuras
    while True:
        respuesta = input(mensaje).strip()
        if not respuesta:
            return None
        try:
            fecha = datetime.date.fromisoformat(respuesta)
        except ValueError:
            print("Fecha inválida: use el formato AAAA-MM-DD (ej. 1990-05-23).")
            continue
        if fecha > datetime.date.today():
            print("La fecha no puede ser futura.")
            continue
        return fecha


def pedir_opcion(mensaje, opciones):
    # opciones es un diccionario "lo que se tipea" -> valor; repite hasta que la clave exista
    while True:
        respuesta = input(mensaje).strip()
        if not respuesta:
            return None
        if respuesta in opciones:
            return opciones[respuesta]
        print("Opción inválida.")


def elegir_de_lista(elementos, mensaje):
    # Elige un elemento de una lista ya mostrada en pantalla con números desde 1.
    # Se arma un diccionario "1" -> primer elemento, "2" -> segundo, etc.
    opciones = {str(i): e for i, e in enumerate(elementos, start=1)}
    return pedir_opcion(mensaje, opciones)


def elegir_maquinaria(sistema):
    # Pide el ID hasta que exista una maquinaria con ese ID
    while True:
        id_unico = pedir_texto("ID de la maquinaria: ")
        if id_unico is None:
            return None
        maquinaria = sistema.buscar_maquinaria(id_unico)
        if maquinaria is not None:
            return maquinaria
        print(f"No existe maquinaria con ID {id_unico}. Ingréselo de nuevo.")


def elegir_tecnico(sistema):
    # Pide el ID hasta que exista un técnico con ese ID
    while True:
        id_tecnico = pedir_entero("ID del técnico: ")
        if id_tecnico is None:
            return None
        tecnico = sistema.buscar_personal(id_tecnico)
        if tecnico is not None:
            return tecnico
        print(f"No existe personal con ID {id_tecnico}. Ingréselo de nuevo.")


def elegir_especialidad():
    # Diccionario número -> Especialidad armado a partir del Enum, así el menú
    # se actualiza solo si se agrega una especialidad nueva
    opciones = {str(i): esp for i, esp in enumerate(Especialidad, start=1)}
    for numero, esp in opciones.items():
        print(f"{numero}. {esp.value}")
    return pedir_opcion("Seleccione la especialidad: ", opciones)


def pedir_componentes(sistema):
    # Arma el diccionario componente -> cantidad que necesita un programa (Regla 6).
    # Se cargan de a uno y Enter vacío termina la carga.
    componentes_requeridos = {}
    if not sistema.componentes:
        print("No hay componentes registrados; el programa no usará repuestos.")
        return componentes_requeridos

    print("Componentes disponibles:")
    for c in sistema.componentes.values():
        print(f"  ID {c.id}: {c.nombre} (stock: {c.cantidad})")

    while True:
        id_componente = pedir_entero("ID del componente a usar (Enter para terminar): ")
        if id_componente is None:
            return componentes_requeridos
        componente = sistema.buscar_componente(id_componente)
        if componente is None:
            print("No existe un componente con ese ID.")
            continue
        cantidad = pedir_entero(f"Cantidad de {componente.nombre}: ", minimo=1)
        if cantidad is None:
            continue
        # El stock no se controla acá: se verifica al iniciar la ejecución (Regla 6)
        componentes_requeridos[componente] = cantidad


def elegir_programa(sistema):
    # Elige una maquinaria, muestra sus programas numerados y devuelve el elegido
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return None
    if not maquinaria.programas:
        print("Esta maquinaria no tiene programas de intervención.")
        return None
    mostrar_programas(maquinaria)
    return elegir_de_lista(maquinaria.programas, "Seleccione el programa: ")


def mostrar_programas(maquinaria):
    for i, p in enumerate(maquinaria.programas, start=1):
        tipo = "Correctivo" if p.es_correctivo else "Preventivo"
        personal = ", ".join(t.nombre for t in p.personal_asignado) or "sin asignar"
        componentes = ", ".join(f"{c.nombre} x{n}" for c, n in p.componentes_requeridos.items()) or "ninguno"
        print(f"{i}. [{tipo}] {p.procedimiento} | Estado: {p.estado.value} | "
              f"Especialidad: {p.especialidad_requerida.value} | Personal: {personal} | "
              f"Componentes: {componentes}")
        if p.es_correctivo:
            print(f"     Aviso asociado: {p.aviso_asociado}")
        else:
            print(f"     Cada {p.periodicidad} días | Próxima fecha: {p.fecha_programada}")


# ---------- 1. Maquinaria ----------

def menu_maquinaria(sistema):
    ejecutar_submenu(sistema, "Gestión de Maquinaria", {
        "1": ("Registrar nueva maquinaria", registrar_maquinaria),
        "2": ("Listar maquinaria", listar_maquinaria),
        "3": ("Cambiar estado de maquinaria", cambiar_estado_maquinaria),
    })


def registrar_maquinaria(sistema):
    # Regla 1: el ID no puede faltar ni repetirse; si está repetido se vuelve a pedir
    while True:
        id_unico = pedir_texto("ID único de la maquinaria: ")
        if id_unico is None:
            return
        if id_unico in sistema.maquinas:
            print(f"Ya existe una maquinaria con el ID {id_unico}. Ingrese otro.")
            continue
        break

    sistema.registrar_maquinaria(Maquinaria(id_unico))
    print(f"Maquinaria {id_unico} registrada como Plenamente Operativa.")


def listar_maquinaria(sistema):
    if not sistema.maquinas:
        print("No hay maquinaria registrada.")
        return
    for m in sistema.maquinas.values():
        print(f"ID: {m.id_unico} | Estado: {m.estado.value}")


def cambiar_estado_maquinaria(sistema):
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return

    print("\n--- Nuevo estado ---")
    print("1. Plenamente Operativa")
    print("2. En Proceso de Mantenimiento")
    print("3. Falla Declarada")

    opciones_estado = {
        "1": EstadoMaquinaria.PLENAMENTE_OPERATIVA,
        "2": EstadoMaquinaria.EN_PROCESO_MANTENIMIENTO,
        "3": EstadoMaquinaria.FALLA_DECLARADA,
    }
    nuevo_estado = pedir_opcion("Seleccione una opción: ", opciones_estado)
    if nuevo_estado is None:
        return

    # Diccionario con los datos extra del cambio de estado; solo se llena si es una falla.
    # Después se pasa con ** a set_estado_maquinaria, que lo recibe como kwargs.
    datos_falla = {}

    if nuevo_estado == EstadoMaquinaria.FALLA_DECLARADA:
        descripcion = pedir_texto("Descripción de la falla: ")
        if descripcion is None:
            return
        causa = pedir_texto("Causa de la falla: ")
        if causa is None:
            return
        datos_falla["descripcion_falla"] = descripcion
        datos_falla["causa"] = causa

        if maquinaria.dispositivos:
            print("Dispositivo que originó la falla (opcional):")
            for i, d in enumerate(maquinaria.dispositivos, start=1):
                print(f"{i}. {d.tipo_de_variable} (umbral: {d.umbral_limite})")
            # Acá Enter vacío no cancela: significa "sin dispositivo de origen"
            dispositivo = elegir_de_lista(maquinaria.dispositivos, "Número de dispositivo, o Enter para omitir: ")
            if dispositivo is not None:
                datos_falla["dispositivo_origen"] = dispositivo

    try:
        maquinaria.set_estado_maquinaria(nuevo_estado, **datos_falla)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Maquinaria {maquinaria.id_unico} actualizada a estado: {nuevo_estado.value}")


# ---------- 2. Dispositivos de medición ----------

def menu_dispositivos(sistema):
    ejecutar_submenu(sistema, "Gestión de Dispositivos de Medición", {
        "1": ("Registrar nuevo dispositivo", registrar_dispositivo),
        "2": ("Listar dispositivos de una maquinaria", listar_dispositivos),
        "3": ("Registrar lectura", registrar_lectura_dispositivo),
    })


def registrar_dispositivo(sistema):
    print("Maquinaria a la que pertenece:")
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return

    # El ID del dispositivo no puede repetirse dentro de la misma maquinaria
    while True:
        id_dispositivo = pedir_entero("ID del dispositivo: ")
        if id_dispositivo is None:
            return
        if any(d.id == id_dispositivo for d in maquinaria.dispositivos):
            print(f"La maquinaria {maquinaria.id_unico} ya tiene un dispositivo con ID {id_dispositivo}. Ingrese otro.")
            continue
        break

    tipo_de_variable = pedir_texto("Variable que monitorea (ej. temperatura, vibración): ")
    if tipo_de_variable is None:
        return
    umbral_limite = pedir_decimal("Umbral límite: ")
    if umbral_limite is None:
        return

    DispositivoMedicion(id_dispositivo, maquinaria, tipo_de_variable, umbral_limite)
    print(f"Dispositivo {id_dispositivo} registrado en la maquinaria {maquinaria.id_unico}.")


def listar_dispositivos(sistema):
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return

    if not maquinaria.dispositivos:
        print("Esta maquinaria no tiene dispositivos registrados.")
        return

    for d in maquinaria.dispositivos:
        print(f"ID: {d.id} | Variable: {d.tipo_de_variable} | Umbral: {d.umbral_limite}")


def registrar_lectura_dispositivo(sistema):
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return

    if not maquinaria.dispositivos:
        print("Esta maquinaria no tiene dispositivos registrados.")
        return

    print("Dispositivos disponibles:")
    for i, d in enumerate(maquinaria.dispositivos, start=1):
        print(f"{i}. {d.tipo_de_variable} (umbral: {d.umbral_limite})")

    dispositivo = elegir_de_lista(maquinaria.dispositivos, "Seleccione el dispositivo: ")
    if dispositivo is None:
        return
    valor = pedir_decimal("Valor medido: ")
    if valor is None:
        return

    try:
        aviso = dispositivo.registrar_lectura(valor)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if aviso is not None:
        print(f"¡Aviso generado! {aviso}")
    else:
        print("Lectura registrada sin novedades.")


# ---------- 3. Personal especializado ----------

def menu_personal(sistema):
    ejecutar_submenu(sistema, "Gestión de Personal Especializado", {
        "1": ("Registrar técnico", registrar_personal),
        "2": ("Listar personal", listar_personal),
        "3": ("Dar de baja técnico (despido o renuncia)", dar_de_baja_personal),
    })


def registrar_personal(sistema):
    # El ID no puede repetirse; si ya existe se vuelve a pedir
    while True:
        id_tecnico = pedir_entero("ID del técnico: ")
        if id_tecnico is None:
            return
        if id_tecnico in sistema.personal:
            print(f"Ya existe personal con el ID {id_tecnico}. Ingrese otro.")
            continue
        break

    nombre = pedir_texto("Nombre: ")
    if nombre is None:
        return
    apellido = pedir_texto("Apellido: ")
    if apellido is None:
        return
    fecha_nacimiento = pedir_fecha("Fecha de nacimiento (AAAA-MM-DD): ")
    if fecha_nacimiento is None:
        return

    # Fecha de ingreso: acá Enter vacío no cancela, significa "ingresa hoy".
    # Se usa para calcular el tiempo en la empresa al darlo de baja.
    while True:
        respuesta = input("Fecha de ingreso a la empresa (AAAA-MM-DD, Enter = hoy): ").strip()
        if not respuesta:
            fecha_ingreso = None
            break
        try:
            fecha_ingreso = datetime.date.fromisoformat(respuesta)
        except ValueError:
            print("Fecha inválida: use el formato AAAA-MM-DD.")
            continue
        if fecha_ingreso > datetime.date.today():
            print("La fecha de ingreso no puede ser futura.")
            continue
        if fecha_ingreso < fecha_nacimiento:
            print("La fecha de ingreso no puede ser anterior a la de nacimiento.")
            continue
        break

    especialidad = elegir_especialidad()
    if especialidad is None:
        return

    sistema.registrar_personal(
        PersonalEspecializado(id_tecnico, nombre, apellido, especialidad, fecha_nacimiento,
                              fecha_ingreso=fecha_ingreso)
    )
    print(f"Técnico {nombre} {apellido} registrado ({especialidad.value}).")


def listar_personal(sistema):
    if not sistema.personal:
        print("No hay personal registrado.")
        return
    for t in sistema.personal.values():
        estado = "Disponible" if t.disponibilidad else "Ocupado"
        print(f"ID: {t.id} | {t.nombre} {t.apellido} | {t.especialidad.value} | {estado} | "
              f"Ingreso: {t.fecha_ingreso}")


def plural(cantidad, singular, plural_):
    # "1 año" / "3 años": evita mostrar "año(s)"
    return f"{cantidad} {singular if cantidad == 1 else plural_}"


def dar_de_baja_personal(sistema):
    if not sistema.personal:
        print("No hay personal registrado.")
        return
    listar_personal(sistema)
    tecnico = elegir_tecnico(sistema)
    if tecnico is None:
        return

    # Confirmación antes de una acción que no se puede deshacer
    confirmacion = pedir_opcion(f"¿Confirma la baja de {tecnico.nombre} {tecnico.apellido}? (s/n): ",
                                {"s": True, "S": True, "n": False, "N": False})
    if not confirmacion:
        print("Baja cancelada.")
        return

    try:
        # SIMPIA valida que esté disponible y lo quita de los programas que aún no empezaron
        tecnico, (anios, meses, dias), programas_afectados = sistema.dar_de_baja_personal(tecnico.id)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Baja registrada: {tecnico.nombre} {tecnico.apellido}.")
    print(f"Estuvo en la empresa {plural(anios, 'año', 'años')}, {plural(meses, 'mes', 'meses')} "
          f"y {plural(dias, 'día', 'días')} (del {tecnico.fecha_ingreso} al {datetime.date.today()}).")
    for programa in programas_afectados:
        print(f"  Se lo quitó del programa '{programa.procedimiento}' de {programa.maquinaria.id_unico}; "
              f"hay que asignar otro técnico.")


# ---------- 4. Componentes de recambio ----------

def menu_componentes(sistema):
    ejecutar_submenu(sistema, "Gestión de Componentes de Recambio", {
        "1": ("Registrar componente", registrar_componente),
        "2": ("Listar componentes y stock", listar_componentes),
        "3": ("Reponer stock", reponer_stock),
    })


def registrar_componente(sistema):
    # El ID no puede repetirse; si ya existe se vuelve a pedir
    while True:
        id_componente = pedir_entero("ID del componente: ")
        if id_componente is None:
            return
        if id_componente in sistema.componentes:
            print(f"Ya existe un componente con el ID {id_componente}. Ingrese otro.")
            continue
        break

    nombre = pedir_texto("Nombre: ")
    if nombre is None:
        return
    cantidad = pedir_entero("Cantidad inicial en stock: ", minimo=0)
    if cantidad is None:
        return

    sistema.registrar_componente(ComponenteRecambio(id_componente, nombre, cantidad))
    print(f"Componente {nombre} registrado con {cantidad} unidades.")


def listar_componentes(sistema):
    if not sistema.componentes:
        print("No hay componentes registrados.")
        return
    for c in sistema.componentes.values():
        print(f"ID: {c.id} | {c.nombre} | Stock: {c.get_stock()}")


def reponer_stock(sistema):
    if not sistema.componentes:
        print("No hay componentes registrados.")
        return
    listar_componentes(sistema)
    while True:
        id_componente = pedir_entero("ID del componente: ")
        if id_componente is None:
            return
        componente = sistema.buscar_componente(id_componente)
        if componente is not None:
            break
        print("No existe un componente con ese ID. Ingréselo de nuevo.")

    cantidad = pedir_entero("Cantidad a agregar: ", minimo=1)
    if cantidad is None:
        return
    componente.setter_agregar_stock(cantidad)
    print(f"Stock de {componente.nombre} actualizado: {componente.get_stock()} unidades.")


# ---------- 5. Programas de intervención ----------

def menu_programas(sistema):
    ejecutar_submenu(sistema, "Gestión de Programas de Intervención", {
        "1": ("Crear programa preventivo", crear_programa_preventivo),
        "2": ("Crear programa correctivo (a partir de un aviso activo)", crear_programa_correctivo),
        "3": ("Listar programas de una maquinaria", listar_programas),
        "4": ("Asignar técnico a un programa", asignar_tecnico_a_programa),
        "5": ("Iniciar ejecución de un programa", iniciar_programa),
        "6": ("Finalizar programa", finalizar_programa),
    })


def listar_programas(sistema):
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return
    if maquinaria.programas:
        mostrar_programas(maquinaria)
    else:
        print("Esta maquinaria no tiene programas de intervención.")


def crear_programa_preventivo(sistema):
    # Regla 5: los preventivos se programan periódicamente
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return
    procedimiento = pedir_texto("Procedimiento a realizar: ")
    if procedimiento is None:
        return
    tipo_equipo = pedir_texto("Tipo de equipo (ej. prensa hidráulica): ")
    if tipo_equipo is None:
        return
    tiempo_requerido = pedir_decimal("Tiempo estimado (horas): ", minimo=0)
    if tiempo_requerido is None:
        return
    periodicidad = pedir_entero("Periodicidad (cada cuántos días): ", minimo=1)
    if periodicidad is None:
        return
    especialidad = elegir_especialidad()
    if especialidad is None:
        return
    componentes = pedir_componentes(sistema)

    ProgramaPreventivo(maquinaria, procedimiento, componentes, tiempo_requerido,
                       especialidad, periodicidad, tipo_equipo)
    print(f"Programa preventivo creado para {maquinaria.id_unico}.")


def crear_programa_correctivo(sistema):
    # Regla 5: un correctivo debe estar asociado a un aviso activo
    maquinaria = elegir_maquinaria(sistema)
    if maquinaria is None:
        return
    avisos_activos = [a for a in maquinaria.avisos if a.estado == EstadoAviso.ACTIVO]
    if not avisos_activos:
        print("Esta maquinaria no tiene avisos activos; no se puede crear un correctivo.")
        return

    print("Avisos activos:")
    for i, a in enumerate(avisos_activos, start=1):
        print(f"{i}. {a} | Parámetro: {a.parametro_anomalo}")
    aviso = elegir_de_lista(avisos_activos, "Seleccione el aviso: ")
    if aviso is None:
        return
    procedimiento = pedir_texto("Procedimiento a realizar: ")
    if procedimiento is None:
        return
    tipo_equipo = pedir_texto("Tipo de equipo (ej. prensa hidráulica): ")
    if tipo_equipo is None:
        return
    tiempo_requerido = pedir_decimal("Tiempo estimado (horas): ", minimo=0)
    if tiempo_requerido is None:
        return

    # Regla 7: se intenta deducir la especialidad a partir de la variable anómala;
    # si la variable no está en el diccionario del correctivo, se elige a mano
    try:
        especialidad = ProgramaCorrectivo.especialidad_para_variable(aviso.parametro_anomalo)
        print(f"Especialidad requerida (deducida de '{aviso.parametro_anomalo}'): {especialidad.value}")
    except ValueError:
        print(f"No se puede deducir la especialidad para '{aviso.parametro_anomalo}'. Elíjala:")
        especialidad = elegir_especialidad()
        if especialidad is None:
            return

    componentes = pedir_componentes(sistema)

    try:
        ProgramaCorrectivo(maquinaria, procedimiento, componentes, tiempo_requerido,
                           aviso, tipo_equipo, especialidad_requerida=especialidad)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Programa correctivo creado para {maquinaria.id_unico}.")


def asignar_tecnico_a_programa(sistema):
    programa = elegir_programa(sistema)
    if programa is None:
        return
    # Si el técnico no sirve para este programa (otra especialidad u ocupado), se pide otro
    while True:
        tecnico = elegir_tecnico(sistema)
        if tecnico is None:
            return
        try:
            # Regla 7: el programa rechaza técnicos de otra especialidad u ocupados
            programa.asignar_personal(tecnico)
        except ValueError as e:
            print(f"Error: {e}. Ingrese otro técnico.")
            continue
        print(f"{tecnico.nombre} {tecnico.apellido} asignado al programa.")
        return


def iniciar_programa(sistema):
    programa = elegir_programa(sistema)
    if programa is None:
        return
    try:
        # set_estado valida que esté PROGRAMADO y, por las reglas 6 y 7,
        # personal, especialidad, disponibilidad y stock antes de arrancar
        programa.set_estado(EstadoProgramaIntervencion.EN_EJECUCION)
    except ValueError as e:
        print(f"No es posible iniciar el programa: {e}")
        return
    print("Programa en ejecución. Se descontó el stock y el personal quedó ocupado.")


def finalizar_programa(sistema):
    programa = elegir_programa(sistema)
    if programa is None:
        return
    try:
        # Regla 8: registra el evento en el historial; si es correctivo, resuelve el aviso
        evento = programa.finalizar()
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Programa finalizado. Evento registrado: {evento}")
    if programa.es_correctivo:
        print(f"Aviso resuelto. Estado de {programa.maquinaria.id_unico}: "
              f"{programa.maquinaria.estado.value}")
    else:
        print(f"El programa preventivo quedó reprogramado para el {programa.fecha_programada}.")


# ---------- 6. Avisos ----------

def menu_avisos(sistema):
    ejecutar_submenu(sistema, "Gestión de Avisos", {
        "1": ("Listar avisos", ver_avisos),
        "2": ("Desactivar un aviso manualmente (personal capacitado)", desactivar_aviso),
    })


def ver_avisos(sistema):
    avisos = sistema.listar_avisos()
    if not avisos:
        print("No hay avisos registrados.")
        return
    for aviso in avisos:
        print(f"{aviso} | Parámetro: {aviso.parametro_anomalo} | Creado: {aviso.fecha_creacion}"
              + (f" | Cerrado: {aviso.fecha_cierre}" if aviso.fecha_cierre else ""))


def desactivar_aviso(sistema):
    # Regla 4: un aviso se resuelve si el personal capacitado lo desactiva explícitamente
    activos = [a for a in sistema.listar_avisos() if a.estado == EstadoAviso.ACTIVO]
    if not activos:
        print("No hay avisos activos.")
        return
    for a in activos:
        print(a)
    # Diccionario id del aviso (como texto) -> aviso, para elegirlo por su ID
    aviso = pedir_opcion("ID del aviso a desactivar: ", {str(a.id_aviso): a for a in activos})
    if aviso is None:
        return
    tecnico = elegir_tecnico(sistema)
    if tecnico is None:
        return
    aviso.desactivar(tecnico)
    print(f"Aviso {aviso.id_aviso} resuelto por {tecnico.nombre} {tecnico.apellido} "
          f"el {aviso.fecha_cierre}.")


# ---------- 7. Historial ----------

def ver_historial(sistema):
    eventos = sistema.listar_historial_eventos()
    if not eventos:
        print("No hay eventos registrados.")
        return
    for evento in eventos:
        print(evento)


def ejecutar_submenu(sistema, titulo, opciones):
    # Submenú genérico: opciones es un diccionario número -> (texto, función).
    # Se queda abierto hasta elegir 0, igual que el menú principal; si la opción no existe,
    # avisa y la vuelve a pedir en vez de volver al menú principal.
    while True:
        print(f"\n--- {titulo} ---")
        for numero, (texto, _) in opciones.items():
            print(f"{numero}. {texto}")
        print("0. Volver")
        print("(En cualquier dato, Enter sin escribir nada cancela y vuelve a este menú)")

        opcion = input("Seleccione una opción: ")
        if opcion == "0":
            return
        entrada = opciones.get(opcion)
        if entrada is None:
            print("Opción inválida.")
        else:
            # Cada función del submenú recibe el sistema como parámetro
            entrada[1](sistema)


def menu_principal(sistema):
    # Diccionario opción -> función: reemplaza la cadena de if/elif.
    # Se guarda la función sin paréntesis (no se ejecuta acá) y se llama después con acción(sistema).
    # Para agregar una opción nueva alcanza con sumar una entrada al diccionario y una línea al print.
    acciones = {
        "1": menu_maquinaria,
        "2": menu_dispositivos,
        "3": menu_personal,
        "4": menu_componentes,
        "5": menu_programas,
        "6": menu_avisos,
        "7": ver_historial,
    }

    while True:
        print("\n===== SMPIA - Menú Principal =====")
        print("1. Gestionar Maquinaria")
        print("2. Gestionar Dispositivos de Medición")
        print("3. Gestionar Personal Especializado")
        print("4. Gestionar Componentes de Recambio")
        print("5. Gestionar Programas de Intervención")
        print("6. Gestionar Avisos")
        print("7. Ver Historial de Eventos")
        print("0. Salir")
        print("(Los datos se guardan automáticamente después de cada operación)")

        opcion = input("Seleccione una opción: ")

        if opcion == "0":
            print("Saliendo del sistema...")
            break

        # .get() devuelve None si la opción no está en el diccionario
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida.")
        else:
            accion(sistema)
            # Guardado automático al volver de cada opción: si el programa se corta,
            # no se pierde lo que se hizo
            sistema.guardar()


# ---------- Programa principal ----------

def main():
    # Carga los datos guardados de una corrida anterior; si no hay archivo
    # (o está dañado) arranca con el sistema vacío
    try:
        sistema = SIMPIA.cargar()
        print(f"Datos cargados desde {ARCHIVO_POR_DEFECTO} "
              f"({len(sistema.maquinas)} maquinaria(s), {len(sistema.personal)} técnico(s), "
              f"{len(sistema.componentes)} componente(s)).")
    except FileNotFoundError:
        sistema = SIMPIA()
        print("No se encontró un archivo de datos previo; se arranca con el sistema vacío.")
    except (json.JSONDecodeError, KeyError) as e:
        # Archivo corrupto o incompleto: no se aborta el programa, se arranca vacío
        sistema = SIMPIA()
        print(f"No se pudo leer {ARCHIVO_POR_DEFECTO} ({e}); se arranca con el sistema vacío.")

    menu_principal(sistema)


# No cambiar a partir de aqui
if __name__ == "__main__":
    main()

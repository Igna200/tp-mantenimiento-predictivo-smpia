def main():
    import datetime
    from Maquinaria import Maquinaria
    from DispositivoMedicion import DispositivoMedicion
    from PersonalEspecializado import PersonalEspecializado
    from ComponenteRecambio import ComponenteRecambio
    from ProgramaPreventivo import ProgramaPreventivo
    from ProgramaCorrectivo import ProgramaCorrectivo
    from SIMPIA import SIMPIA
    from estados.EstadoMaquinaria import EstadoMaquinaria
    from estados.EstadoAviso import EstadoAviso
    from estados.EstadoProgramaIntervencion import EstadoProgramaIntervencion
    from estados.Especialidad import Especialidad

# "Base de datos" en memoria
    sistema = SIMPIA()


    def menu_principal():
        # Diccionario opción -> función: reemplaza la cadena de if/elif.
        # Se guarda la función sin paréntesis (no se ejecuta acá) y se llama después con acción().
        # Para agregar una opción nueva alcanza con sumar una entrada al diccionario y una línea al print.
        acciones = {
            "1": menu_maquinaria,
            "2": menu_dispositivos,
            "3": menu_personal,
            "4": menu_componentes,
            "5": menu_programas,
            "6": menu_avisos,
            "7": ver_historial,
            "8": cargar_datos_ejemplo,
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
            print("8. Cargar datos de ejemplo (para probar o hacer la demo)")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "0":
                print("Saliendo del sistema...")
                break

            # .get() devuelve None si la opción no está en el diccionario
            accion = acciones.get(opcion)
            if accion is None:
                print("Opción inválida.")
            else:
                accion()


    def menu_maquinaria():
        print("\n--- Gestión de Maquinaria ---")
        print("1. Registrar nueva maquinaria")
        print("2. Listar maquinaria")
        print("3. Cambiar estado de maquinaria")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_maquinaria()
        elif opcion == "2":
            listar_maquinaria()
        elif opcion == "3":
            cambiar_estado_maquinaria()
        elif opcion != "0":
            # Antes volvía al menú principal sin avisar si la opción no existía
            print("Opción inválida.")


    def registrar_maquinaria():
        id_unico = input("ID único de la maquinaria: ")


        try:
            nueva = Maquinaria(id_unico)           #si el id es vacio salta el error.
            sistema.registrar_maquinaria(nueva)
        except ValueError as e:
            print(f"Error: {e}")
            return

        print(f"Maquinaria {id_unico} registrada como Plenamente Operativa.")


    def listar_maquinaria():
        if not sistema.maquinas:
            print("No hay maquinaria registrada.")
            return
        for m in sistema.maquinas.values():
            print(f"ID: {m.id_unico} | Estado: {m.estado.value}")


    def cambiar_estado_maquinaria():
        id_unico = input("ID de la maquinaria: ")
        maquinaria = sistema.buscar_maquinaria(id_unico)
        if maquinaria is None:
            print(f"Error: no existe maquinaria con ID {id_unico}.")
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
        nuevo_estado = opciones_estado.get(input("Seleccione una opción: "))
        if nuevo_estado is None:
            print("Opción inválida.")
            return

        # Diccionario con los datos extra del cambio de estado; solo se llena si es una falla.
        # Después se pasa con ** a set_estado_maquinaria, que lo recibe como kwargs.
        datos_falla = {}

        if nuevo_estado == EstadoMaquinaria.FALLA_DECLARADA:
            datos_falla["descripcion_falla"] = input("Descripción de la falla: ")
            datos_falla["causa"] = input("Causa de la falla: ")

            if maquinaria.dispositivos:
                print("Dispositivo que originó la falla (opcional):")
                for i, d in enumerate(maquinaria.dispositivos, start=1):
                    print(f"{i}. {d.tipo_de_variable} (umbral: {d.umbral_limite})")
                respuesta = input("Número de dispositivo, o Enter para omitir: ").strip()
                if respuesta:
                    try:
                        datos_falla["dispositivo_origen"] = maquinaria.dispositivos[int(respuesta) - 1]
                    except (ValueError, IndexError):
                        print("Selección inválida, se omite el dispositivo de origen.")

        try:
            maquinaria.set_estado_maquinaria(nuevo_estado, **datos_falla)
        except ValueError as e:
            print(f"Error: {e}")
            return

        print(f"Maquinaria {id_unico} actualizada a estado: {nuevo_estado.value}")


    def menu_dispositivos():
        print("\n--- Gestión de Dispositivos de Medición ---")
        print("1. Registrar nuevo dispositivo")
        print("2. Listar dispositivos de una maquinaria")
        print("3. Registrar lectura")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_dispositivo()
        elif opcion == "2":
            listar_dispositivos()
        elif opcion == "3":
            registrar_lectura_dispositivo()
        elif opcion != "0":
            print("Opción inválida.")


    def registrar_dispositivo():
        id_maquinaria = input("ID de la maquinaria a la que pertenece: ")
        maquinaria = sistema.buscar_maquinaria(id_maquinaria)
        if maquinaria is None:
            print(f"Error: no existe maquinaria con ID {id_maquinaria}.")
            return

        try:
            id_dispositivo = int(input("ID del dispositivo: "))
            tipo_de_variable = input("Variable que monitorea (ej. temperatura, vibración): ")
            umbral_limite = float(input("Umbral límite: "))
        except ValueError:
            print("Error: el ID y el umbral deben ser numéricos.")
            return

        # El ID del dispositivo no puede repetirse dentro de la misma maquinaria
        if any(d.id == id_dispositivo for d in maquinaria.dispositivos):
            print(f"Error: la maquinaria {maquinaria.id_unico} ya tiene un dispositivo con ID {id_dispositivo}.")
            return

        DispositivoMedicion(id_dispositivo, maquinaria, tipo_de_variable, umbral_limite)
        print(f"Dispositivo {id_dispositivo} registrado en la maquinaria {maquinaria.id_unico}.")


    def listar_dispositivos():
        id_maquinaria = input("ID de la maquinaria: ")
        maquinaria = sistema.buscar_maquinaria(id_maquinaria)
        if maquinaria is None:
            print(f"Error: no existe maquinaria con ID {id_maquinaria}.")
            return

        if not maquinaria.dispositivos:
            print("Esta maquinaria no tiene dispositivos registrados.")
            return

        for d in maquinaria.dispositivos:
            print(f"ID: {d.id} | Variable: {d.tipo_de_variable} | Umbral: {d.umbral_limite}")


    def registrar_lectura_dispositivo():
        id_maquinaria = input("ID de la maquinaria: ")
        maquinaria = sistema.buscar_maquinaria(id_maquinaria)
        if maquinaria is None:
            print(f"Error: no existe maquinaria con ID {id_maquinaria}.")
            return

        if not maquinaria.dispositivos:
            print("Esta maquinaria no tiene dispositivos registrados.")
            return

        print("Dispositivos disponibles:")
        for i, d in enumerate(maquinaria.dispositivos, start=1):
            print(f"{i}. {d.tipo_de_variable} (umbral: {d.umbral_limite})")

        try:
            indice = int(input("Seleccione el dispositivo: ")) - 1
            dispositivo = maquinaria.dispositivos[indice]
            valor = float(input("Valor medido: "))
        except (ValueError, IndexError):
            print("Error: selección o valor inválido.")
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


    # ---------- Funciones auxiliares para pedir datos (las usan varios menús) ----------

    def elegir_maquinaria():
        # Pide un ID y devuelve la maquinaria, o None (con mensaje) si no existe
        id_unico = input("ID de la maquinaria: ")
        maquinaria = sistema.buscar_maquinaria(id_unico)
        if maquinaria is None:
            print(f"Error: no existe maquinaria con ID {id_unico}.")
        return maquinaria


    def elegir_tecnico():
        # Pide un ID numérico y devuelve el técnico, o None si no existe
        try:
            id_tecnico = int(input("ID del técnico: "))
        except ValueError:
            print("Error: el ID debe ser numérico.")
            return None
        tecnico = sistema.buscar_personal(id_tecnico)
        if tecnico is None:
            print(f"Error: no existe personal con ID {id_tecnico}.")
        return tecnico


    def elegir_especialidad():
        # Arma un diccionario número -> Especialidad a partir del Enum, así el menú
        # se actualiza solo si se agrega una especialidad nueva
        opciones = {str(i): esp for i, esp in enumerate(Especialidad, start=1)}
        for numero, esp in opciones.items():
            print(f"{numero}. {esp.value}")
        especialidad = opciones.get(input("Seleccione la especialidad: "))
        if especialidad is None:
            print("Opción inválida.")
        return especialidad


    def pedir_componentes():
        # Arma el diccionario componente -> cantidad que necesita un programa (Regla 6).
        # Se cargan de a uno; Enter vacío termina. Devuelve None si hubo un error.
        componentes_requeridos = {}
        if not sistema.componentes:
            print("No hay componentes registrados; el programa no usará repuestos.")
            return componentes_requeridos

        print("Componentes disponibles:")
        for c in sistema.componentes.values():
            print(f"  ID {c.id}: {c.nombre} (stock: {c.cantidad})")

        while True:
            respuesta = input("ID del componente a usar (Enter para terminar): ").strip()
            if not respuesta:
                return componentes_requeridos
            try:
                componente = sistema.buscar_componente(int(respuesta))
                if componente is None:
                    print("No existe un componente con ese ID.")
                    continue
                cantidad = int(input(f"Cantidad de {componente.nombre}: "))
                if cantidad <= 0:
                    print("La cantidad debe ser mayor a cero.")
                    continue
            except ValueError:
                print("Error: el ID y la cantidad deben ser numéricos.")
                return None
            # El stock no se controla acá: se verifica al iniciar la ejecución (Regla 6)
            componentes_requeridos[componente] = cantidad


    def elegir_programa():
        # Elige una maquinaria, muestra sus programas numerados y devuelve el elegido
        maquinaria = elegir_maquinaria()
        if maquinaria is None:
            return None
        if not maquinaria.programas:
            print("Esta maquinaria no tiene programas de intervención.")
            return None
        mostrar_programas(maquinaria)
        try:
            indice = int(input("Seleccione el programa: ")) - 1
            if indice < 0:
                raise IndexError
            return maquinaria.programas[indice]
        except (ValueError, IndexError):
            print("Error: selección inválida.")
            return None


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


    # ---------- 3. Personal especializado ----------

    def menu_personal():
        print("\n--- Gestión de Personal Especializado ---")
        print("1. Registrar técnico")
        print("2. Listar personal")
        print("3. Dar de baja técnico (despido o renuncia)")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_personal()
        elif opcion == "2":
            listar_personal()
        elif opcion == "3":
            dar_de_baja_personal()
        elif opcion != "0":
            print("Opción inválida.")


    def registrar_personal():
        try:
            id_tecnico = int(input("ID del técnico: "))
            fecha_nacimiento = datetime.date.fromisoformat(input("Fecha de nacimiento (AAAA-MM-DD): "))
            # Enter vacío = ingresa hoy; se usa para calcular el tiempo en la empresa al darlo de baja
            respuesta_ingreso = input("Fecha de ingreso a la empresa (AAAA-MM-DD, Enter = hoy): ").strip()
            fecha_ingreso = datetime.date.fromisoformat(respuesta_ingreso) if respuesta_ingreso else None
        except ValueError:
            print("Error: el ID debe ser numérico y las fechas con formato AAAA-MM-DD.")
            return
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        especialidad = elegir_especialidad()
        if especialidad is None:
            return

        try:
            # SIMPIA controla que el ID no esté repetido
            sistema.registrar_personal(
                PersonalEspecializado(id_tecnico, nombre, apellido, especialidad, fecha_nacimiento,
                                      fecha_ingreso=fecha_ingreso)
            )
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"Técnico {nombre} {apellido} registrado ({especialidad.value}).")


    def listar_personal():
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


    def dar_de_baja_personal():
        if not sistema.personal:
            print("No hay personal registrado.")
            return
        listar_personal()
        tecnico = elegir_tecnico()
        if tecnico is None:
            return

        # Confirmación antes de una acción que no se puede deshacer
        confirmacion = input(f"¿Confirma la baja de {tecnico.nombre} {tecnico.apellido}? (s/n): ")
        if confirmacion.strip().lower() != "s":
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

    def menu_componentes():
        print("\n--- Gestión de Componentes de Recambio ---")
        print("1. Registrar componente")
        print("2. Listar componentes y stock")
        print("3. Reponer stock")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_componente()
        elif opcion == "2":
            listar_componentes()
        elif opcion == "3":
            reponer_stock()
        elif opcion != "0":
            print("Opción inválida.")


    def registrar_componente():
        try:
            id_componente = int(input("ID del componente: "))
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad inicial en stock: "))
        except ValueError:
            print("Error: el ID y la cantidad deben ser numéricos.")
            return
        if cantidad < 0:
            print("Error: la cantidad no puede ser negativa.")
            return

        try:
            sistema.registrar_componente(ComponenteRecambio(id_componente, nombre, cantidad))
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"Componente {nombre} registrado con {cantidad} unidades.")


    def listar_componentes():
        if not sistema.componentes:
            print("No hay componentes registrados.")
            return
        for c in sistema.componentes.values():
            print(f"ID: {c.id} | {c.nombre} | Stock: {c.get_stock()}")


    def reponer_stock():
        try:
            componente = sistema.buscar_componente(int(input("ID del componente: ")))
            if componente is None:
                print("Error: no existe un componente con ese ID.")
                return
            # setter_agregar_stock valida que la cantidad sea mayor a cero
            componente.setter_agregar_stock(int(input("Cantidad a agregar: ")))
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"Stock de {componente.nombre} actualizado: {componente.get_stock()} unidades.")


    # ---------- 5. Programas de intervención ----------

    def menu_programas():
        print("\n--- Gestión de Programas de Intervención ---")
        print("1. Crear programa preventivo")
        print("2. Crear programa correctivo (a partir de un aviso activo)")
        print("3. Listar programas de una maquinaria")
        print("4. Asignar técnico a un programa")
        print("5. Iniciar ejecución de un programa")
        print("6. Finalizar programa")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_programa_preventivo()
        elif opcion == "2":
            crear_programa_correctivo()
        elif opcion == "3":
            maquinaria = elegir_maquinaria()
            if maquinaria is not None:
                if maquinaria.programas:
                    mostrar_programas(maquinaria)
                else:
                    print("Esta maquinaria no tiene programas de intervención.")
        elif opcion == "4":
            asignar_tecnico_a_programa()
        elif opcion == "5":
            iniciar_programa()
        elif opcion == "6":
            finalizar_programa()
        elif opcion != "0":
            print("Opción inválida.")


    def crear_programa_preventivo():
        # Regla 5: los preventivos se programan periódicamente
        maquinaria = elegir_maquinaria()
        if maquinaria is None:
            return
        procedimiento = input("Procedimiento a realizar: ")
        tipo_equipo = input("Tipo de equipo (ej. prensa hidráulica): ")
        try:
            tiempo_requerido = float(input("Tiempo estimado (horas): "))
            periodicidad = int(input("Periodicidad (cada cuántos días): "))
        except ValueError:
            print("Error: el tiempo y la periodicidad deben ser numéricos.")
            return
        especialidad = elegir_especialidad()
        if especialidad is None:
            return
        componentes = pedir_componentes()
        if componentes is None:
            return

        ProgramaPreventivo(maquinaria, procedimiento, componentes, tiempo_requerido,
                           especialidad, periodicidad, tipo_equipo)
        print(f"Programa preventivo creado para {maquinaria.id_unico}.")


    def crear_programa_correctivo():
        # Regla 5: un correctivo debe estar asociado a un aviso activo
        maquinaria = elegir_maquinaria()
        if maquinaria is None:
            return
        avisos_activos = [a for a in maquinaria.avisos if a.estado == EstadoAviso.ACTIVO]
        if not avisos_activos:
            print("Esta maquinaria no tiene avisos activos; no se puede crear un correctivo.")
            return

        print("Avisos activos:")
        for i, a in enumerate(avisos_activos, start=1):
            print(f"{i}. {a} | Parámetro: {a.parametro_anomalo}")
        try:
            indice = int(input("Seleccione el aviso: ")) - 1
            if indice < 0:
                raise IndexError
            aviso = avisos_activos[indice]
            procedimiento = input("Procedimiento a realizar: ")
            tipo_equipo = input("Tipo de equipo (ej. prensa hidráulica): ")
            tiempo_requerido = float(input("Tiempo estimado (horas): "))
        except (ValueError, IndexError):
            print("Error: selección o valor inválido.")
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

        componentes = pedir_componentes()
        if componentes is None:
            return

        try:
            ProgramaCorrectivo(maquinaria, procedimiento, componentes, tiempo_requerido,
                               aviso, tipo_equipo, especialidad_requerida=especialidad)
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"Programa correctivo creado para {maquinaria.id_unico}.")


    def asignar_tecnico_a_programa():
        programa = elegir_programa()
        if programa is None:
            return
        tecnico = elegir_tecnico()
        if tecnico is None:
            return
        try:
            # Regla 7: el programa rechaza técnicos de otra especialidad u ocupados
            programa.asignar_personal(tecnico)
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"{tecnico.nombre} {tecnico.apellido} asignado al programa.")


    def iniciar_programa():
        programa = elegir_programa()
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


    def finalizar_programa():
        programa = elegir_programa()
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


    # ---------- 6. Avisos ----------

    def menu_avisos():
        print("\n--- Gestión de Avisos ---")
        print("1. Listar avisos")
        print("2. Desactivar un aviso manualmente (personal capacitado)")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_avisos()
        elif opcion == "2":
            desactivar_aviso()
        elif opcion != "0":
            print("Opción inválida.")


    def ver_avisos():
        avisos = sistema.listar_avisos()
        if not avisos:
            print("No hay avisos registrados.")
            return
        for aviso in avisos:
            print(f"{aviso} | Parámetro: {aviso.parametro_anomalo} | Creado: {aviso.fecha_creacion}"
                  + (f" | Cerrado: {aviso.fecha_cierre}" if aviso.fecha_cierre else ""))


    def desactivar_aviso():
        # Regla 4: un aviso se resuelve si el personal capacitado lo desactiva explícitamente
        activos = [a for a in sistema.listar_avisos() if a.estado == EstadoAviso.ACTIVO]
        if not activos:
            print("No hay avisos activos.")
            return
        for a in activos:
            print(a)
        try:
            id_aviso = int(input("ID del aviso a desactivar: "))
        except ValueError:
            print("Error: el ID debe ser numérico.")
            return
        aviso = next((a for a in activos if a.id_aviso == id_aviso), None)
        if aviso is None:
            print("Error: no hay un aviso activo con ese ID.")
            return
        tecnico = elegir_tecnico()
        if tecnico is None:
            return
        aviso.desactivar(tecnico)
        print(f"Aviso {aviso.id_aviso} resuelto por {tecnico.nombre} {tecnico.apellido} "
              f"el {aviso.fecha_cierre}.")


    # ---------- 8. Datos de ejemplo ----------

    def cargar_datos_ejemplo():
        # Carga un escenario listo para probar el sistema o hacer la demo. Contiene:
        #   Maquinarias:  PRENSA-01 y HORNO-02 (ambas plenamente operativas)
        #   Personal:     1 Juan Pérez (mecánico, ingresó 2015-03-02), 2 Lucía Gómez (hidráulico, 2019-07-15),
        #                 3 Martín Díaz (electrónico, 2022-11-01)
        #   Componentes:  1 Junta hidráulica (10 u.), 2 Rodamiento (6 u.), 3 Fusible (20 u.)
        #   Dispositivos: 1 presión, umbral 100, en PRENSA-01 / 2 temperatura, umbral 80, en HORNO-02
        # No crea avisos ni programas: se generan durante la prueba (ej. una lectura de 150 en el
        # dispositivo de presión genera un aviso, y su correctivo requiere un técnico hidráulico).
        if "PRENSA-01" in sistema.maquinas:
            print("Los datos de ejemplo ya estaban cargados.")
            return

        prensa = Maquinaria("PRENSA-01")
        horno = Maquinaria("HORNO-02")
        for m in (prensa, horno):
            sistema.registrar_maquinaria(m)

        for tecnico in (
            PersonalEspecializado(1, "Juan", "Pérez", Especialidad.mecanico, datetime.date(1985, 4, 12),
                                  fecha_ingreso=datetime.date(2015, 3, 2)),
            PersonalEspecializado(2, "Lucía", "Gómez", Especialidad.hidraulico, datetime.date(1990, 9, 3),
                                  fecha_ingreso=datetime.date(2019, 7, 15)),
            PersonalEspecializado(3, "Martín", "Díaz", Especialidad.electronico, datetime.date(1988, 1, 25),
                                  fecha_ingreso=datetime.date(2022, 11, 1)),
        ):
            sistema.registrar_personal(tecnico)

        for componente in (
            ComponenteRecambio(1, "Junta hidráulica", 10),
            ComponenteRecambio(2, "Rodamiento", 6),
            ComponenteRecambio(3, "Fusible", 20),
        ):
            sistema.registrar_componente(componente)

        DispositivoMedicion(1, prensa, "presión", 100.0)
        DispositivoMedicion(2, horno, "temperatura", 80.0)

        print("Datos de ejemplo cargados:")
        print("  Maquinarias:  PRENSA-01, HORNO-02")
        print("  Personal:     1 Juan Pérez (mecánico, desde 2015-03-02), 2 Lucía Gómez (hidráulico, desde 2019-07-15),")
        print("                3 Martín Díaz (electrónico, desde 2022-11-01)")
        print("  Componentes:  1 Junta hidráulica (10), 2 Rodamiento (6), 3 Fusible (20)")
        print("  Dispositivos: 1 presión (umbral 100) en PRENSA-01, 2 temperatura (umbral 80) en HORNO-02")
        print("  Sugerencia: registrá una lectura de 150 en el dispositivo de presión de PRENSA-01.")


    def ver_historial():
        eventos = sistema.listar_historial_eventos()
        if not eventos:
            print("No hay eventos registrados.")
            return
        for evento in eventos:
            print(evento)

    menu_principal()

# No cambiar a partir de aqui
if __name__ == "__main__":
    main()

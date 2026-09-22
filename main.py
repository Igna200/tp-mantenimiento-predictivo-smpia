def main():
    from Maquinaria import Maquinaria
    from DispositivoMedicion import DispositivoMedicion
    from Aviso import Aviso
    from PersonalEspecializado import PersonalEspecializado
    from ComponenteRecambio import ComponenteRecambio
    from ProgramaPreventivo import ProgramaPreventivo
    from ProgramaCorrectivo import ProgramaCorrectivo
    from SIMPIA import SIMPIA
    from estados.EstadoMaquinaria import EstadoMaquinaria

# "Base de datos" en memoria
    sistema = SIMPIA()


    def menu_principal():
        while True:
            print("\n===== SMPIA - Menú Principal =====")
            print("1. Gestionar Maquinaria")
            print("2. Gestionar Dispositivos de Medición")
            print("3. Gestionar Personal Especializado")
            print("4. Gestionar Componentes de Recambio")
            print("5. Gestionar Programas de Intervención")
            print("6. Ver Avisos")
            print("7. Ver Historial de Eventos")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                menu_maquinaria()
            elif opcion == "2":
                menu_dispositivos()
            elif opcion == "3":
                menu_personal()
            elif opcion == "4":
                menu_componentes()
            elif opcion == "5":
                menu_programas()
            elif opcion == "6":
                ver_avisos()
            elif opcion == "7":
                ver_historial()
            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")


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


    def registrar_maquinaria():
        id_unico = input("ID único de la maquinaria: ")

        nueva = Maquinaria(id_unico)
        try:
            sistema.registrar_maquinaria(nueva)
        except ValueError as e:
            print(f"Error: {e}")
            return

        print(f"Maquinaria {id_unico} registrada como Plenamente Operativa.")


    def listar_maquinaria():
        if not sistema.maquinas:
            print("No hay maquinaria registrada.")
            return
        for m in sistema.maquinas:
            print(f"ID: {m.id_unico} | Estado: {m.estado.value}")


    def buscar_maquinaria(id_unico):
        return next((m for m in sistema.maquinas if m.id_unico == id_unico), None)


    def cambiar_estado_maquinaria():
        id_unico = input("ID de la maquinaria: ")
        maquinaria = buscar_maquinaria(id_unico)
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

        descripcion_falla = None
        personal_interviniente = None

        if nuevo_estado == EstadoMaquinaria.FALLA_DECLARADA:
            if not sistema.personal:
                print("Error: no hay personal especializado registrado para asociar a la falla.")
                return

            descripcion_falla = input("Descripción de la falla: ")

            print("Personal disponible:")
            for i, tecnico in enumerate(sistema.personal, start=1):
                print(f"{i}. {tecnico.nombre} {tecnico.apellido}")
            try:
                indice = int(input("Seleccione el técnico que detectó la falla: ")) - 1
                personal_interviniente = [sistema.personal[indice]]
            except (ValueError, IndexError):
                print("Error: selección inválida.")
                return

        try:
            maquinaria.set_estado_maquinaria(nuevo_estado, descripcion_falla, personal_interviniente)
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


    def registrar_dispositivo():
        id_maquinaria = input("ID de la maquinaria a la que pertenece: ")
        maquinaria = buscar_maquinaria(id_maquinaria)
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

        DispositivoMedicion(id_dispositivo, maquinaria, tipo_de_variable, umbral_limite)
        print(f"Dispositivo {id_dispositivo} registrado en la maquinaria {maquinaria.id_unico}.")


    def listar_dispositivos():
        id_maquinaria = input("ID de la maquinaria: ")
        maquinaria = buscar_maquinaria(id_maquinaria)
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
        maquinaria = buscar_maquinaria(id_maquinaria)
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


    def menu_personal():
        pass  # placeholder


    def menu_componentes():
        pass  # placeholder


    def menu_programas():
        pass  # placeholder


    def ver_avisos():
        avisos = sistema.listar_avisos()
        if not avisos:
            print("No hay avisos registrados.")
            return
        for aviso in avisos:
            print(aviso)


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

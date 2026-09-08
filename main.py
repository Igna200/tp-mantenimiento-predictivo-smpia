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
    maquinas = []
    personal = []
    componentes = []


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

        if any(m.id_unico == id_unico for m in maquinas):
            print("Error: ya existe una maquinaria con ese ID.")
            return

        nueva = Maquinaria(id_unico)
        maquinas.append(nueva)
        print(f"Maquinaria {id_unico} registrada como Plenamente Operativa.")


    def listar_maquinaria():
        if not maquinas:
            print("No hay maquinaria registrada.")
            return
        for m in maquinas:
            print(f"ID: {m.id_unico} | Estado: {m.estado.value}")


    def cambiar_estado_maquinaria():
        # placeholder - lo definimos según cómo terminó set_estado_maquinaria
        pass


    def menu_dispositivos():
        pass  # placeholder


    def menu_personal():
        pass  # placeholder


    def menu_componentes():
        pass  # placeholder


    def menu_programas():
        pass  # placeholder


    def ver_avisos():
        pass  # placeholder


    def ver_historial():
        pass  # placeholder

# No cambiar a partir de aqui
if __name__ == "__main__":
    main()

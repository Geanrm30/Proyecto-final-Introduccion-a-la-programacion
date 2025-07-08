from funciones import *

# =========================
# MENÚ PRINCIPAL Y FLUJO DEL SISTEMA
# =========================

# =========================
# FUNCIÓN: mostrar_menu
# Muestra el menú principal con todas las opciones disponibles para el usuario.
# =========================
def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN ===")
    print("1. Agregar producto")
    print("2. Agregar producto con lotes")
    print("3. Listar productos")
    print("4. Vender producto")
    print("5. Chequear alertas")
    print("6. Resumen de ventas")
    print("7. Aumentar stock")
    print("8. Cambiar fecha de vencimiento")
    print("9. Eliminar productos vencidos")
    print("10. Ver historial de eliminados")
    print("11. Salir")

# =========================
# FUNCIÓN: main
# Controla el flujo principal del programa:
# - Carga los datos iniciales.
# - Solicita inicio de sesión.
# - Muestra el menú y ejecuta la opción seleccionada.
# =========================
def main():
    cargar_datos()  # Carga los datos necesarios al iniciar el sistema

    # =========================
    # USUARIOS Y AUTENTICACIÓN
    # Solicita inicio de sesión al usuario.
    # Si la autenticación falla, termina el programa.
    # =========================
    if not inicio_sesion():
        return

    # =========================
    # BUCLE PRINCIPAL DEL MENÚ
    # Permite al usuario seleccionar opciones hasta que decida salir.
    # =========================
    while True:
        mostrar_menu()  # Muestra el menú de opciones
        opcion = input("Seleccione una opción (1-11): ")

        try:
            opc = int(opcion)  # Intenta convertir la opción ingresada a entero
        except ValueError:
            print("Error: Ingrese un número del 1 al 11")  # Si falla, muestra error y repite
            continue

        # =========================
        # SELECCIÓN DE OPCIONES DEL MENÚ
        # Ejecuta la función correspondiente según la opción seleccionada.
        # =========================
        if opc == 1:
            agregar_producto()  # Agrega un nuevo producto al sistema
        elif opc == 2:
            agregar_producto_lotes()  # Agrega un producto con manejo de lotes
        elif opc == 3:
            listar_productos()  # Lista todos los productos registrados
        elif opc == 4:
            vender_producto()  # Realiza la venta de un producto
        elif opc == 5:
            chequear_alertas()  # Muestra alertas de productos (por ejemplo, vencimientos)
        elif opc == 6:
            resumen_ventas()  # Muestra un resumen de las ventas realizadas
        elif opc == 7:
            aumentar_stock()  # Permite aumentar el stock de un producto
        elif opc == 8:
            cambiar_fecha_vencimiento()  # Cambia la fecha de vencimiento de un producto
        elif opc == 9:
            eliminar_vencidos()  # Elimina productos que ya están vencidos
        elif opc == 10:
            mostrar_eliminados()  # Muestra el historial de productos eliminados
        elif opc == 11:
            # =========================
            # SALIDA DEL SISTEMA
            # Guarda los datos y termina la ejecución del programa.
            # =========================
            print("\nGuardando datos y saliendo del sistema...")
            generar_resumen_diario()  # Guarda el resumen diario antes de salir
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")  # Si la opción no es válida, muestra mensaje

# =========================
# PUNTO DE ENTRADA DEL PROGRAMA
# Ejecuta la función principal si el archivo es ejecutado directamente.
# =========================
if __name__ == "__main__":
    main()
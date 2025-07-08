Algoritmo SistemaGestionInventarioPali
    // Definición de variables para productos
    Dimension codigos[100]       // Arreglo para almacenar los códigos de hasta 100 productos
    Dimension nombres[100]       // Arreglo para almacenar los nombres de los productos (como cadenas de caracteres)
    Dimension precios[100]       // Arreglo para guardar los precios de cada producto
    Dimension stocks[100]        // Arreglo para llevar el control del inventario (cantidad disponible)
    
    Dimension ventas[100,3]      // Matriz para registrar ventas: [codigo_producto, cantidad, total]
	// Capacidad para 100 ventas con 3 datos cada una
    
    // Declaración de variables
    Definir opcion, codigo, cantidad, i, total_productos, total_ventas Como Entero
    Definir nombre Como Caracter  // Variable temporal para lectura de nombres
    Definir precio, total_venta Como Real  // Variables para manejar valores decimales (precios y totales)
    Definir continuar, encontrado Como Logico  // Variables booleanas para control de flujo
    
    // Inicialización de variables
    total_productos <- 0         // Contador de productos registrados (inicia en 0)
    total_ventas <- 0           // Contador de ventas realizadas (inicia en 0)
    continuar <- Verdadero      // Bandera para controlar el ciclo principal
    
    // Ciclo principal del programa
    Mientras continuar Hacer
        // Mostrar menú de opciones
        Escribir ""
        Escribir "=== MENÚ PRINCIPAL ==="
        Escribir "1. Agregar producto"
        Escribir "2. Listar productos"
        Escribir "3. Vender producto"
        Escribir "4. Salir"
        Escribir "Seleccione una opción (1-4): "
        Leer opcion  // Leer la opción seleccionada por el usuario
        
        // Estructura de control para las diferentes opciones
        Segun opcion Hacer
            1:  // Opción 1: Agregar producto
                Si total_productos < 100 Entonces  // Verificar si hay espacio para más productos
                    // Solicitar datos del producto
                    Escribir "Ingrese código del producto (número): "
                    Leer codigos[total_productos+1]  // Almacenar código en la siguiente posición disponible
                    Escribir "Ingrese nombre del producto: "
                    Leer nombre
                    nombres[total_productos+1] <- nombre  // Guardar nombre
                    Escribir "Ingrese precio(C$): "
                    Leer precios[total_productos+1]  // Guardar precio
                    Escribir "Ingrese cantidad en stock: "
                    Leer stocks[total_productos+1]  // Guardar cantidad en stock
                    
                    total_productos <- total_productos + 1  // Incrementar contador de productos
                    Escribir "Producto agregado correctamente."
                Sino
                    Escribir "No se pueden agregar más productos (límite alcanzado)."  // Mensaje si se excede capacidad
                FinSi
                
            2:  // Opción 2: Listar productos
                Si total_productos = 0 Entonces  // Verificar si hay productos registrados
                    Escribir "No hay productos registrados."
                Sino
                    Escribir ""
                    Escribir "=== LISTA DE PRODUCTOS ==="
                    // Recorrer todos los productos registrados
                    Para i <- 1 Hasta total_productos Hacer
                        // Mostrar información de cada producto
                        Escribir "Código: ", codigos[i]
                        Escribir "Nombre: ", nombres[i]
                        Escribir "Precio: C$", precios[i]
                        Escribir "Stock: ", stocks[i]
                        Escribir "-----------------------"
                    FinPara
                FinSi
                
            3:  // Opción 3: Vender producto
                Si total_productos = 0 Entonces  // Verificar si hay productos disponibles
                    Escribir "No hay productos para vender."
                Sino
                    Escribir "Ingrese código del producto a vender: "
                    Leer codigo  // Leer código del producto a vender
                    
                    encontrado <- Falso  // Bandera para saber si se encontró el producto
                    // Buscar el producto en el arreglo
                    Para i <- 1 Hasta total_productos Hacer
                        Si codigos[i] = codigo Entonces  // Si se encuentra el código
                            encontrado <- Verdadero
                            
                            // Mostrar información del producto encontrado
                            Escribir "Producto: ", nombres[i]
                            Escribir "Stock disponible: ", stocks[i]
                            Escribir "Ingrese cantidad a vender: "
                            Leer cantidad  // Leer cantidad a vender
                            
                            Si cantidad <= 0 Entonces  // Validar cantidad positiva
                                Escribir "Cantidad no válida."
                            Sino
                                Si cantidad > stocks[i] Entonces  // Verificar stock suficiente
                                    Escribir "No hay suficiente stock."
                                Sino
                                    // Calcular total de la venta
                                    total_venta <- cantidad * precios[i]
                                    // Actualizar stock (reducir la cantidad vendida)
                                    stocks[i] <- stocks[i] - cantidad
                                    
                                    // Registrar la venta
                                    total_ventas <- total_ventas + 1
                                    ventas[total_ventas,1] <- codigos[i]  // Guardar código
                                    ventas[total_ventas,2] <- cantidad    // Guardar cantidad
                                    ventas[total_ventas,3] <- total_venta // Guardar total
                                    
                                    Escribir "Venta realizada. Total: C$", total_venta
                                FinSi
                            FinSi
                        FinSi
                    FinPara
                    
                    Si NO encontrado Entonces  // Si no se encontró el producto
                        Escribir "Producto no encontrado."
                    FinSi
                FinSi
                
            4:  // Opción 4: Salir del sistema
                Escribir ""
                Escribir "=== RESUMEN FINAL ==="
                Escribir ""
                Escribir "=== PRODUCTOS REGISTRADOS ==="
                Si total_productos = 0 Entonces  // Mostrar resumen de productos
                    Escribir "No hay productos registrados."
                Sino
                    Escribir "Total productos registrados: ", total_productos
                    Escribir ""
                    // Listar todos los productos con su estado actual
                    Para i <- 1 Hasta total_productos Hacer
                        Escribir "Producto #", i
                        Escribir "Código: ", codigos[i]
                        Escribir "Nombre: ", nombres[i]
                        Escribir "Precio: C$", precios[i]
                        Escribir "Stock actual: ", stocks[i]
                        Escribir "-----------------------"
                    FinPara
                FinSi
                
                Escribir ""
                Escribir "=== VENTAS REALIZADAS ==="
                Si total_ventas = 0 Entonces  // Mostrar resumen de ventas
                    Escribir "No se realizaron ventas."
                Sino
                    Escribir "Total ventas realizadas: ", total_ventas
                    Escribir "Detalle de ventas:"
                    Escribir ""
                    total_general <- 0  // Variable para acumular el total de todas las ventas
                    // Recorrer todas las ventas realizadas
                    Para i <- 1 Hasta total_ventas Hacer
                        Escribir "Venta #", i
                        Escribir "Código producto: ", ventas[i,1]
                        Escribir "Cantidad vendida: ", ventas[i,2]
                        Escribir "Total venta: C$", ventas[i,3]
                        total_general <- total_general + ventas[i,3]  // Acumular total
                        Escribir "-----------------------"
                    FinPara
                    Escribir ""
                    Escribir "TOTAL GENERAL DE VENTAS: C$", total_general
                FinSi
                
                Escribir ""
                Escribir "Gracias por usar el sistema."
                continuar <- Falso  // Cambiar bandera para salir del ciclo
                
            De Otro Modo:  // Opción no válida
                Escribir "Opción no válida. Intente nuevamente."
        FinSegun
    FinMientras
FinAlgoritmo
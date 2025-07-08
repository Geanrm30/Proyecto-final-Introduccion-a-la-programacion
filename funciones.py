import datetime  # Importa el módulo para trabajar con fechas y horas
import os        # Importa el módulo para interactuar con el sistema de archivos
import pwinput   # Importa el módulo para entrada de contraseñas enmascaradas

# =========================
# FUNCIONES DE USUARIOS Y AUTENTICACIÓN
# =========================

def cargar_usuarios():
    """
    Carga los usuarios y contraseñas desde el archivo 'usuarios.txt'.
    Devuelve un diccionario con usuario como clave y contraseña como valor.
    """
    usuarios = {}  # Diccionario para almacenar usuarios y contraseñas
    # Verifica si el archivo de usuarios existe
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                usuario, clave = linea.strip().split("|")  # Separa usuario y clave por '|'
                usuarios[usuario] = clave  # Agrega al diccionario
    return usuarios  # Devuelve el diccionario de usuarios

def inicio_sesion():
    """
    Solicita usuario y contraseña al usuario.
    Permite hasta 3 intentos para ingresar correctamente.
    Devuelve True si la autenticación es exitosa, False en caso contrario.
    """
    print("\n=== INICIO DE SESIÓN ===")
    usuarios = cargar_usuarios()  # Carga los usuarios registrados
    usuario = input("Usuario: ")  # Solicita el nombre de usuario
    
    intentos = 3  # Número máximo de intentos permitidos
    while intentos > 0:
        # Solicita la contraseña de forma oculta
        clave_ingresada = pwinput.pwinput(prompt='Contraseña: ', mask='*')
        # Verifica si el usuario existe y la contraseña es correcta
        if usuario in usuarios and usuarios[usuario] == clave_ingresada:
            print("\nAcceso permitido")
            return True  # Retorna True si la autenticación es exitosa
        else:
            intentos -= 1  # Resta un intento
            print(f"\nUsuario o contraseña incorrectos. Intentos restantes: {intentos}")
    
    print("\nHa superado el número máximo de intentos.")
    return False  # Retorna False si falla los intentos

# =========================
# VARIABLES GLOBALES
# =========================

productos = {}   # Diccionario para almacenar los productos
ventas = []      # Lista para almacenar las ventas realizadas
eliminados = []  # Lista para almacenar los productos eliminados

# =========================
# FUNCIONES DE CARGA Y GUARDADO DE DATOS
# =========================

def cargar_datos():
    """
    Carga los datos de productos, ventas y eliminados desde sus respectivos archivos.
    Actualiza las variables globales productos, ventas y eliminados.
    """
    # Carga productos desde 'stock.txt'
    if os.path.exists("stock.txt"):
        with open("stock.txt", "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split('|')  # Separa los campos por '|'
                producto = {}  # Diccionario para los datos del producto
                lotes = []     # Lista para los lotes del producto
                
                for campo in datos:
                    if '=' not in campo:
                        continue  # Ignora campos sin '='
                    clave, valor = campo.split('=', 1)  # Separa clave y valor
                    
                    if clave == 'codigo':
                        codigo = valor  # Guarda el código del producto
                    elif clave == 'nombre':
                        producto['nombre'] = valor  # Guarda el nombre
                    elif clave == 'precio':
                        producto['precio'] = float(valor)  # Convierte el precio a float
                    elif clave == 'stock':
                        producto['stock'] = int(valor)  # Convierte el stock a int
                    elif clave == 'vencimiento':
                        producto['vencimiento'] = datetime.datetime.strptime(valor, "%Y-%m-%d").date()  # Convierte la fecha
                    # Manejo de lotes: busca campos de lote y vencimiento
                    elif clave.startswith('lote') and clave.endswith('_vencimiento'):
                        lote_num = clave.split('_')[0][4:]  # Obtiene el número de lote
                        stock_key = f"lote{lote_num}_stock"  # Construye la clave del stock del lote
                        stock_val = next((c.split('=')[1] for c in datos if c.startswith(stock_key)), None)  # Busca el stock
                        if stock_val:
                            lote = {
                                'stock': int(stock_val),  # Stock del lote
                                'vencimiento': datetime.datetime.strptime(valor, "%Y-%m-%d").date()  # Fecha de vencimiento del lote
                            }
                            lotes.append(lote)  # Agrega el lote a la lista
                
                if lotes:
                    producto['lotes'] = lotes  # Si hay lotes, los agrega al producto
                productos[codigo] = producto  # Agrega el producto al diccionario global

    # Carga ventas desde 'ventas.txt'
    if os.path.exists("ventas.txt"):
        with open("ventas.txt", "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split('|')  # Separa los campos por '|'
                venta = {}  # Diccionario para los datos de la venta
                for campo in datos:
                    if '=' not in campo:
                        continue  # Ignora campos sin '='
                    clave, valor = campo.split('=', 1)
                    if clave == 'codigo':
                        venta['codigo'] = valor
                    elif clave == 'nombre':
                        venta['nombre'] = valor
                    elif clave == 'cantidad':
                        venta['cantidad'] = int(valor)
                    elif clave == 'total':
                        venta['total'] = float(valor)
                    elif clave == 'fecha':
                        venta['fecha'] = datetime.datetime.strptime(valor, "%Y-%m-%d").date()
                    elif clave == 'hora':
                        venta['hora'] = valor
                ventas.append(venta)  # Agrega la venta a la lista global

    # Carga productos eliminados desde 'eliminados.txt'
    if os.path.exists("eliminados.txt"):
        with open("eliminados.txt", "r", encoding="utf-8") as f:
            for linea in f:
                eliminados.append(linea.strip())  # Agrega cada línea a la lista de eliminados

def guardar_stock():
    """
    Guarda el estado actual de los productos en el archivo 'stock.txt'.
    Incluye información de lotes si existen.
    """
    with open("stock.txt", "w", encoding="utf-8") as f:
        for c, p in productos.items():
            # Construye la línea con los datos principales del producto
            linea = f"codigo={c}|nombre={p['nombre']}|precio={p['precio']}|stock={p['stock']}|vencimiento={p['vencimiento']}"
            # Si el producto tiene lotes, los agrega a la línea
            if 'lotes' in p:
                for i, lote in enumerate(p['lotes'], 1):
                    linea += f"|lote{i}_stock={lote['stock']}|lote{i}_vencimiento={lote['vencimiento']}"
            f.write(linea + "\n")  # Escribe la línea en el archivo

def guardar_venta(venta):
    """
    Guarda una venta individual en el archivo 'ventas.txt'.
    """
    with open("ventas.txt", "a", encoding="utf-8") as f:
        # Escribe los datos de la venta en una línea
        f.write(f"codigo={venta['codigo']}|nombre={venta['nombre']}|cantidad={venta['cantidad']}|total={venta['total']}|fecha={venta['fecha']}|hora={venta['hora']}\n")

# =========================
# FUNCIONES DE PRODUCTOS
# =========================

def agregar_producto():
    """
    Permite agregar un nuevo producto o aumentar el stock de uno existente.
    Solicita los datos al usuario y actualiza el archivo de stock.
    """
    codigo = input("Código: ")  # Solicita el código del producto
    
    # Si el producto ya existe, solo aumenta el stock
    if codigo in productos:
        print("El producto ya existe.")
        try:
            cantidad_extra = int(input("¿Cuánto stock deseas agregar?: "))  # Solicita la cantidad a agregar
            if cantidad_extra > 0:
                productos[codigo]['stock'] += cantidad_extra  # Suma el stock
                print(f"Stock actualizado. Nuevo stock: {productos[codigo]['stock']}")
                guardar_stock()  # Guarda los cambios
            else:
                print("Cantidad inválida.")
        except ValueError:
            print("Entrada no válida.")
        return  # Sale de la función si el producto ya existía
    
    # Solicita los datos del nuevo producto
    nombre = input("Nombre: ")
    try:
        precio = float(input("Precio (C$): "))  # Solicita el precio
        stock = int(input("Stock: "))           # Solicita el stock
    except ValueError:
        print("Entrada no válida. Usa números para precio y stock.")
        return
    
    fv = input("Fecha vencimiento (YYYY-MM-DD): ")  # Solicita la fecha de vencimiento
    try:
        fecha_v = datetime.datetime.strptime(fv, "%Y-%m-%d").date()  # Convierte la fecha
    except ValueError:
        print("Formato de fecha incorrecto.")
        return
    
    # Agrega el producto al diccionario global
    productos[codigo] = {
        'nombre': nombre,
        'precio': precio,
        'stock': stock,
        'vencimiento': fecha_v
    }
    print(f"Producto {nombre} agregado.")
    guardar_stock()  # Guarda los cambios

def agregar_producto_lotes():
    """
    Permite agregar un nuevo producto con varios lotes, cada uno con su propio stock y fecha de vencimiento.
    """
    codigo = input("Código: ")  # Solicita el código del producto
    
    # Si el producto ya existe, no permite agregarlo de nuevo
    if codigo in productos:
        print("El producto ya existe. Use la opción de aumentar stock o cambiar fecha de vencimiento.")
        return
    
    nombre = input("Nombre: ")  # Solicita el nombre del producto
    try:
        precio = float(input("Precio (C$): "))  # Solicita el precio
    except ValueError:
        print("Entrada no válida. Usa números para el precio.")
        return
    
    lotes = []  # Lista para almacenar los lotes
    while True:
        try:
            stock_lote = int(input("Stock para este lote (0 para terminar): "))  # Solicita el stock del lote
            if stock_lote == 0:
                break  # Sale del ciclo si el usuario ingresa 0
            if stock_lote < 0:
                print("La cantidad debe ser positiva.")
                continue  # Solicita de nuevo si la cantidad es negativa
                
            fv = input("Fecha vencimiento para este lote (YYYY-MM-DD): ")  # Solicita la fecha de vencimiento del lote
            fecha_v = datetime.datetime.strptime(fv, "%Y-%m-%d").date()  # Convierte la fecha
            
            lotes.append({'stock': stock_lote, 'vencimiento': fecha_v})  # Agrega el lote a la lista
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")
            continue  # Solicita de nuevo si hay error en la entrada
    
    if not lotes:
        print("No se agregaron lotes. Operación cancelada.")
        return
    
    # Calcula el stock total y la fecha de vencimiento más próxima
    stock_total = sum(lote['stock'] for lote in lotes)
    fecha_principal = min(lote['vencimiento'] for lote in lotes)
    
    productos[codigo] = {
        'nombre': nombre,
        'precio': precio,
        'stock': stock_total,
        'vencimiento': fecha_principal,
        'lotes': lotes
    }
    
    print(f"Producto {nombre} agregado con {len(lotes)} lotes. Stock total: {stock_total}")
    guardar_stock()  # Guarda los cambios

def cambiar_fecha_vencimiento():
    """
    Permite cambiar la fecha de vencimiento de un producto existente.
    """
    codigo = input("Código del producto: ")  # Solicita el código del producto
    if codigo not in productos:
        print("El producto no existe.")
        return
    
    fecha_actual = productos[codigo]['vencimiento']  # Obtiene la fecha actual de vencimiento
    print(f"Fecha de vencimiento actual: {fecha_actual}")
    
    nueva_fecha = input("Nueva fecha de vencimiento (YYYY-MM-DD): ")  # Solicita la nueva fecha
    try:
        fecha_v = datetime.datetime.strptime(nueva_fecha, "%Y-%m-%d").date()  # Convierte la fecha
        productos[codigo]['vencimiento'] = fecha_v  # Actualiza la fecha
        print("Fecha de vencimiento actualizada correctamente.")
        guardar_stock()  # Guarda los cambios
    except ValueError:
        print("Formato de fecha incorrecto. Use YYYY-MM-DD.")

def aumentar_stock():
    """
    Permite aumentar el stock de un producto existente.
    """
    codigo = input("Código del producto: ")  # Solicita el código del producto
    if codigo not in productos:
        print("El producto no existe.")
        return
    
    try:
        cantidad = int(input("Cantidad a agregar: "))  # Solicita la cantidad a agregar
        if cantidad > 0:
            productos[codigo]['stock'] += cantidad  # Suma el stock
            print(f"Nuevo stock de {productos[codigo]['nombre']}: {productos[codigo]['stock']}")
            guardar_stock()  # Guarda los cambios
        else:
            print("Cantidad inválida.")
    except ValueError:
        print("Entrada no válida.")

def eliminar_vencidos():
    """
    Elimina productos cuyo vencimiento es anterior a la fecha actual.
    Guarda un registro en 'eliminados.txt' y actualiza el archivo de stock.
    """
    hoy = datetime.date.today()  # Obtiene la fecha actual
    eliminados_local = []  # Lista para los códigos eliminados en esta ejecución
    
    for codigo in list(productos.keys()):
        if productos[codigo]['vencimiento'] < hoy:
            p = productos[codigo]
            # Construye el registro de eliminación
            registro = f"codigo={codigo}|nombre={p['nombre']}|stock={p['stock']}|vencimiento={p['vencimiento']}|eliminado={hoy}"
            eliminados.append(registro)  # Agrega al historial
            
            with open("eliminados.txt", "a", encoding="utf-8") as f:
                f.write(registro + "\n")  # Escribe en el archivo de eliminados
            
            eliminados_local.append(codigo)  # Agrega el código a la lista local
            del productos[codigo]  # Elimina el producto del diccionario
    
    if eliminados_local:
        print("Productos vencidos eliminados:")
        for cod in eliminados_local:
            print(f" - {cod}")  # Muestra los códigos eliminados
        guardar_stock()  # Guarda los cambios
    else:
        print("No hay productos vencidos para eliminar.")

def listar_productos():
    """
    Muestra en pantalla el listado de todos los productos registrados.
    """
    if not productos:
        print("No hay productos registrados.")
        return
    
    print("\nListado de productos:")
    for codigo, p in productos.items():
        # Muestra los datos principales de cada producto
        print(f"{codigo}: {p['nombre']} - Precio: C${p['precio']} - Stock: {p['stock']} - Vence: {p['vencimiento']}")

# =========================
# FUNCIONES DE VENTAS
# =========================

def vender_producto():
    """
    Permite vender un producto, actualiza el stock y registra la venta.
    """
    codigo = input("Código: ")  # Solicita el código del producto
    if codigo not in productos:
        print("Código no encontrado.")
        return
    
    try:
        cantidad = int(input("Cantidad: "))  # Solicita la cantidad a vender
    except ValueError:
        print("Cantidad no válida.")
        return
    
    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return
    
    p = productos[codigo]  # Obtiene el producto
    if p['stock'] < cantidad:
        print("Stock insuficiente.")
        return
    
    # Actualiza el stock y calcula el total de la venta
    p['stock'] -= cantidad
    total = round(p['precio'] * cantidad, 2)  # Calcula el total
    fecha_hora = datetime.datetime.now()  # Obtiene la fecha y hora actual
    
    venta = {
        'codigo': codigo,
        'nombre': p['nombre'],
        'cantidad': cantidad,
        'total': total,
        'fecha': fecha_hora.date(),
        'hora': fecha_hora.time().strftime("%H:%M:%S")
    }
    
    ventas.append(venta)  # Agrega la venta a la lista global
    print(f"Venta: {cantidad} x {p['nombre']}. Total: C${total}.")
    guardar_venta(venta)  # Guarda la venta en el archivo
    guardar_stock()       # Guarda el stock actualizado

# =========================
# FUNCIONES DE ALERTAS Y REPORTES
# =========================

def chequear_alertas():
    """
    Verifica productos con bajo stock, agotados o vencidos y muestra alertas en pantalla.
    """
    hoy = datetime.date.today()  # Obtiene la fecha actual
    alertas = []  # Lista para las alertas
    
    for p in productos.values():
        if p['stock'] == 0:
            alertas.append(f"AGOTADO: {p['nombre']}")  # Alerta de agotado
        elif p['stock'] < 3:
            alertas.append(f"BAJO STOCK: {p['nombre']} (Quedan: {p['stock']})")  # Alerta de bajo stock
        if p['vencimiento'] < hoy:
            alertas.append(f"VENCIDO: {p['nombre']} (Vencimiento: {p['vencimiento']})")  # Alerta de vencido
    
    if alertas:
        print("\n--- ALERTAS ---")
        for alerta in alertas:
            print(alerta)  # Muestra cada alerta
    else:
        print("\nNo hay alertas en este momento.")

def resumen_ventas():
    """
    Muestra un resumen de las ventas realizadas en el día y genera un archivo de resumen.
    """
    if not ventas:
        print("No se han realizado ventas.")
        return
    
    hoy = datetime.date.today()  # Obtiene la fecha actual
    ventas_hoy = [v for v in ventas if v['fecha'] == hoy]  # Filtra ventas de hoy
    
    if not ventas_hoy:
        print("No hay ventas hoy.")
        return
    
    total = sum(v['total'] for v in ventas_hoy)  # Suma el total de ventas de hoy
    print(f"\nResumen de ventas de hoy ({hoy}):")
    print(f"Total ventas: C${round(total, 2)}")
    print("\nDetalle de ventas:")
    for v in ventas_hoy:
        print(f"- {v['cantidad']} x {v['nombre']}: C${v['total']} ({v['hora']})")  # Detalle de cada venta
    
    generar_resumen_diario()  # Genera el archivo de resumen

def generar_resumen_diario():
    """
    Genera un archivo de resumen diario con el estado de productos, ventas y alertas.
    El archivo se llama 'resumen_YYYY-MM-DD.txt'.
    """
    hoy = datetime.date.today().strftime("%Y-%m-%d")  # Obtiene la fecha en formato string
    resumen_nombre = f"resumen_{hoy}.txt"  # Nombre del archivo de resumen
    
    with open(resumen_nombre, "w", encoding="utf-8") as f:
        f.write("RESUMEN DIARIO DE VENTAS Y STOCK\n")
        f.write(f"Fecha|{hoy}\n\n")
        
        # Sección de productos
        f.write("--- PRODUCTOS ---\n")
        for c, p in productos.items():
            linea = f"codigo={c}|nombre={p['nombre']}|precio={p['precio']}|stock={p['stock']}|vencimiento={p['vencimiento']}"
            if 'lotes' in p:
                for i, lote in enumerate(p['lotes'], 1):
                    linea += f"|lote{i}_stock={lote['stock']}|lote{i}_vencimiento={lote['vencimiento']}"
            f.write(linea + "\n")
        
        # Sección de ventas del día
        f.write("\n--- VENTAS DEL DÍA ---\n")
        ventas_hoy = [v for v in ventas if v['fecha'].strftime("%Y-%m-%d") == hoy]
        if ventas_hoy:
            for v in ventas_hoy:
                f.write(f"{v['cantidad']} x {v['nombre']} - Total: C${v['total']} ({v['hora']})\n")
            total = sum(v['total'] for v in ventas_hoy)
            f.write(f"\nTOTAL VENTAS: C${round(total, 2)}\n")
        else:
            f.write("No hubo ventas hoy.\n")
        
        # Sección de alertas
        f.write("\n--- ALERTAS ---\n")
        alertas = []
        for p in productos.values():
            if p['stock'] < 3:
                alertas.append(f"BAJO STOCK: {p['nombre']} (Quedan: {p['stock']})")
            if p['vencimiento'] < datetime.date.today():
                alertas.append(f"VENCIDO: {p['nombre']} (Vencimiento: {p['vencimiento']})")
        
        if alertas:
            for alerta in alertas:
                f.write(alerta + "\n")
        else:
            f.write("No hay alertas.\n")

def mostrar_eliminados():
    """
    Muestra en pantalla los últimos 10 productos eliminados por vencimiento.
    Si hay más de 10, indica cómo ver el historial completo.
    """
    if not eliminados:
        print("\nNo hay productos eliminados en el historial.")
        return
    
    print("\nHISTORIAL DE PRODUCTOS ELIMINADOS:")
    for registro in eliminados[-10:]:
        print(f"- {registro}")  # Muestra los últimos 10 registros
    
    if len(eliminados) > 10:
        print(f"\n(Mostrando 10 de {len(eliminados)} registros. Ver 'eliminados.txt' para el historial completo)")
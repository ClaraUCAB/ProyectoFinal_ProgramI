import pickle
import sys
import os


def clear():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")


def inventario_default():
    return [
        # Código    Nombre                  Precio      Cantidad
        ["abc123",  "Poción",               "76z",      10],
        ["def456",  "Dash juice",           "1028z",    20],
        ["ghi789",  "Piedra de afilar",     "80z",      50],
        ["jkl012",  "Gema Wyvern",          "180000z",  3],
        ["mno345",  "Nargacuga",            "102000z",  5],
    ]


def guardar_binario(archivo, datos):
    with open(archivo, "wb") as file:
        pickle.dump(datos, file)


def cargar_binario(archivo):
    with open(archivo, "rb") as file:
        return pickle.load(file)


def importar_inventario() -> list[list]:
    try:
        return cargar_binario("inventario.bin")

    except FileNotFoundError:
        # Es la primera vez que se ejecuta el programa
        # Asignamos el inventario por default
        return inventario_default()


def obtener_codigo(producto):
    return producto[0]


def editar_codigo(producto, valor):
    producto[0] = valor
    return producto


def obtener_nombre(producto):
    return producto[1]


def editar_nombre(producto, valor):
    producto[1] = valor
    return producto


def obtener_precio(producto):
    return producto[2]


def editar_precio(producto, valor):
    producto[2] = valor
    return producto


def obtener_cantidad(producto):
    return producto[3]
    

def editar_cantidad(producto, valor) -> list:
    producto[3] = valor
    return producto


def busqueda_binaria(array, objetivo):
    start = 0
    end = len(array) - 1
    while start <= end:
        # Se busca la mitad del segmento
        center = (start + end) // 2

        # Vemos si encontramos el objetivo
        if array[center] == objetivo:
            return center

        # Como está ordenado pregunta si el segmento
        # superior contiene el objetivo
        elif array[center] < objetivo:
            # Selecciona la parte superior
            start = center + 1

        else:
            # Selecciona la parte inferior
            end = center - 1

    # No lo encontramos
    return -1


def busqueda_lineal(array, objetivo):
    for i in range(len(array)):
        if array[i] == objetivo:
            return i
    return -1


def ordenamiento_burbuja(array):
    # Hacemos una copia del arreglo
    array = array[:]

    d = len(array)  # Obtiene la longitud de la lista
    for k in range(d):
        swapped = False  #verificar si se realizó algún intercambio en esta iteración
        for a in range(0, d - k - 1):
            # Compara elementos adyacentes y los intercambia si están en el orden incorrecto
            if array[a] > array[a + 1]:
                array[a], array[a + 1] = array[a + 1], array[a]  # Intercambio
                swapped = True  # Marca que se realizó un intercambio
        if not swapped:
            break  # Si no hubo intercambios, la lista está ordenada y se sale del ciclo
    return array  # devuelve la lista ordenada


def ordenar_por_codigo(inventario):
    # Creamos una copia del arreglo
    inventario = inventario[:]
    return ordenamiento_burbuja(inventario)


def ordenar_por_nombre(inventario):
    # Creamos una copia del arreglo
    inventario = inventario[:]

    # Invertimos el código y el nombre ya que
    # la función de ordenamiento_burbuja tomará en cuenta el primer elemento
    for i in inventario:
        i[0], i[1] = i[1], i[0]

    inventario = ordenamiento_burbuja(inventario)

    # Los invertimos de vuelta
    for i in inventario:
        i[0], i[1] = i[1], i[0]

    return inventario


def buscar_por_codigo(inventario, codigo):
    return busqueda_lineal([i[0] for i in inventario], codigo)


def buscar_por_nombre(inventario, nombre):
    return busqueda_lineal([i[1] for i in inventario], nombre)


def buscar_producto(inventario, termino):
    index = buscar_por_codigo(inventario, termino)

    if index != -1:
        return index

    return buscar_por_nombre(inventario, termino)


def crear_producto(inventario):
    print("Para crear el producto, por favor, ingrese los siguientes datos:")

    # El código no se puede repetir
    while True:
        codigo = input("Código: ")

        if buscar_por_codigo(inventario, codigo) != -1:
            clear()
            print("[!] Un producto con ese código ya existe. Por favor, escoja un código distinto.\n")
            print("Para crear el producto, por favor, ingrese los siguientes datos:")
            continue

        break

    # El nombre tampoco se puede repetir
    while True:
        nombre = input("Nombre: ")

        if buscar_por_nombre(inventario, nombre) != -1:
            clear()
            print("[!] Un producto con ese nombre ya existe. Por favor, escoja un nombre distinto.\n")
            print("Para crear el producto, por favor, ingrese los siguientes datos:")
            continue

        break

    precio = input("Precio de venta: ") + "z"
    cantidad = int(input("Cantidad: "))

    return [codigo, nombre, precio, cantidad]


def menu():
    while True:
        print("=== Menú ===")
        print("[0] Mostrar inventario")
        print("[1] Buscar producto")
        print("[2] Ingresar producto")
        print("[3] Egresar producto")
        print("[4] Guardar cambios")
        print("[5] Salir")

        opcion = input("> ")

        # Verificamos que la opción sea válida
        if not opcion.isdigit() or not 0 <= int(opcion) <= 5:
            clear()
            print(f"[!] '{opcion}' es una opción inválida. Por favor, intente de nuevo.\n")
            continue
        opcion = int(opcion)
        
        # La opción es válida
        clear()
        return opcion


def mostrar_inventario(inventario):
    # Creamos una copia del inventario
    inventario = inventario[:]

    # Llevaremos rastro de los inventarios ya ordenados
    # una vez el usuario nos los pida para no hacer
    # las operaciones de ordenamiento multiples veces
    inventario_ordenado_codigo = []
    inventario_ordenado_nombre = []
    ordenado_por_codigo = False
    ordenado_por_nombre = False

    while True:
        # Calcular la longitud máxima de cada columna
        max_longitudes = [max(len(str(item[0])) for item in inventario),  # Longitud máxima de Código
                          max(len(item[1]) for item in inventario),      # Longitud máxima de Nombre
                          max(len(str(item[2])) for item in inventario),  # Longitud máxima de Precio (como str)
                          max(len(str(item[3])) for item in inventario)]  # Longitud máxima de Cantidad (como str)
        # Imprimir encabezado de la tabla
        header = f"{'Código':<{max_longitudes[0]}}  {'Nombre':<{max_longitudes[1]}}  {'Precio':<{max_longitudes[2]}}  {'Cantidad':<{max_longitudes[3]}}"
        print(header)
        print("-" * len(header))
        # Imprimir cada fila de la tabla
        for item in inventario:
            codigo = f"{item[0]:<{max_longitudes[0]}}"
            nombre = f"{item[1]:<{max_longitudes[1]}}"
            precio = f"{item[2]:<{max_longitudes[2]}}"
            cantidad = f"{item[3]:<{max_longitudes[3]}}"
            print(f"{codigo}  {nombre}  {precio}  {cantidad}")

        print()
        print("[0] Ordenar por código")
        print("[1] Ordenar por nombre")
        print("[2] Regresar al menú")
        opcion = input("> ")

        # Verificamos que la opcion es valida
        if not opcion.isdigit() or not 0 <= int(opcion) <= 2:
            clear()
            print(f"[!] '{opcion}' es una opción inválida. Por favor, intente de nuevo.\n")
            continue
        opcion = int(opcion)

        match opcion:
            # Ordenamiento por código
            case 0:
                # Revisamos si no hemos ya previamente ordenado
                if not ordenado_por_codigo:
                    inventario_ordenado_codigo = ordenamiento_burbuja(inventario)
                    ordenado_por_codigo = True

                inventario = inventario_ordenado_codigo
                clear()

            # Ordenamiento por nombre
            case 1:
                # Revisamos si no hemos ya previamente ordenado
                if not ordenado_por_nombre:
                    inventario_ordenado_nombre = ordenar_por_nombre(inventario)
                    ordenado_por_nombre = True

                inventario = inventario_ordenado_nombre
                clear()

            # Regresar al menú
            case 2:
                return


def buscar(inventario):
    termino = input("Ingrese el código o nombre del producto a buscar: ")
    cambios = False

    # Buscamos a ver si este producto existe
    index = buscar_producto(inventario, termino)

    if index == -1:
        # El producto no existe
        print("El producto que usted a ingresado no existe.")
        input("Presione ENTER para continuar...")
        return cambios

    producto = inventario[index]
    codigo = obtener_codigo(producto)
    nombre = obtener_nombre(producto)
    precio = obtener_precio(producto)
    cantidad = obtener_cantidad(producto)

    clear()
    while True:
        print("= Datos del producto =")
        print(f"Código: {codigo}")
        print(f"Nombre: {nombre}")
        print(f"Precio de venta: {precio}")
        print(f"Cantidad: {cantidad}")

        print("\n¿Desea actualizar alguno de estos datos?")
        print("[0] Código")
        print("[1] Nombre")
        print("[2] Precio de venta")
        print("[3] Cantidad")
        print("[4] Regresar al menú")
        opcion = input("> ")

        # Verificamos que la opcion es válida
        if not opcion.isdigit() or not 0 <= int(opcion) <= 4:
            clear()
            print(f"[!] '{opcion}' es una opción inválida. Por favor, intente de nuevo.\n")
            continue
        opcion = int(opcion)

        print()

        match opcion:
            # Modificar código
            case 0:
                print(f"Código actual: {codigo}")
                codigo = input("Ingrese un nuevo código: ")
                inventario[index] = editar_codigo(producto, codigo)
                clear()
                cambios = True

            # Modificar nombre
            case 1:
                print(f"Nombre actual: {nombre}")
                nombre = input("Ingrese un nuevo nombre: ")
                inventario[index] = editar_nombre(producto, nombre)
                clear()
                cambios = True

            # Modificar precio de venta
            case 2:
                print(f"Precio actual: {precio}")
                precio = input("Ingrese un nuevo precio: ") + "z"
                inventario[index] = editar_precio(producto, precio)
                clear()
                cambios = True

            # Modificar cantidad
            case 3:
                print(f"Cantidad actual: {cantidad}")
                cantidad = int(input("Ingrese una nueva cantidad: "))
                inventario[index] = editar_cantidad(producto, cantidad)
                clear()
                cambios = True

            # Regresar al menú
            case 4:
                return cambios


def ingresar_producto(inventario):
    # Creamos una copia del inventario
    inventario = inventario[:]

    termino = input("Ingrese el código o nombre del producto a ingresar: ")

    # Buscamos a ver si este producto existe
    index = buscar_producto(inventario, termino)

    if index == -1:
        # El producto no existe, así que lo creamos
        print("El producto ingresado no existe. Desea crearlo? [Y/n]")
        respuesta = input("> ").lower()

        if respuesta == "n":
            # El usuario no desea crear una nueva entrada
            return inventario, False

        # Creamos una nueva entrada
        producto = crear_producto(inventario)
        inventario.append(producto)
        return inventario, True

    producto = inventario[index]

    # El producto existe
    while True:
        print("¿Qué cantidad de este producto desea ingresar?")
        cantidad = int(input("> "))

        if cantidad < 0:
            clear()
            print("[!] Cantidad demasiado pequeña. Por favor, escoja una más grande.\n")
            continue

        # Le sumamos la cantidad de producto que quiere agregar el usuario
        # a la cantidad de producto ya existente
        cantidad += obtener_cantidad(producto)
        break

    producto = editar_cantidad(producto, cantidad)

    inventario[index] = producto
    return inventario, True


def egresar_producto(inventario):
    # Creamos una copia del inventario
    inventario = inventario[:]

    termino = input("Ingrese el código o nombre del producto a egresar: ")

    # Buscamos a ver si este producto existe
    index = buscar_producto(inventario, termino)

    if index == -1:
        # El producto no existe
        print("El producto que usted a ingresado no existe.")
        input("Presione ENTER para continuar...")
        return inventario, False

    producto = inventario[index]
    cantidad_disponible = obtener_cantidad(producto)

    # El producto existe
    while True:
        print(f"¿Qué cantidad de este producto desea egresar? [{cantidad_disponible} disponibles]")
        cantidad = int(input("> "))

        if cantidad < 0:
            clear()
            print("[!] Cantidad demasiado pequeña. Por favor, escoga una más grande.\n")
            continue

        # Comprobamos que el usuario no está pidiendo egresar más de los que hay
        if cantidad_disponible - cantidad < 0:
            print(f"No es posible extraer {cantidad}. Hay disponibilidad de {cantidad_disponible} productos.")
            print("Desea extraer esa cantidad? [Y/n]")
            respuesta = input("> ").lower()

            if respuesta == "n":
                # El usuario no desea egresar nada
                # Regresamos al menú
                return inventario, False
            
            # Le quitamos lo máximo posible
            cantidad = cantidad_disponible

        # Le sustraemos la cantidad de producto que quiere quitar el usuario
        # a la cantidad de producto ya existente
        cantidad = cantidad_disponible - cantidad
        break

    producto = editar_cantidad(producto, cantidad)

    inventario[index] = producto
    return inventario, True


def salir(inventario, cambios):
    # Verificamos si hay cambios sin guardar
    if not cambios:
        # No hay ningún cambio que guardar.
        # Salimos sin problema
        return True

    while True:
        print("¡Atención! Usted tiene cambios sin guardar.\n")
        print("[0] Guardar y salir")
        print("[1] Salir sin guardar")
        print("[2] Regresar al menú")

        opcion = input("> ")

        # Verificamos que la opción sea válida
        if not opcion.isdigit() or not 0 <= int(opcion) <= 2:
            clear()
            print(f"[!] '{opcion}' es una opción inválida. Por favor, intente de nuevo.\n")
            continue
        opcion = int(opcion)

        if opcion == 0:
            # Guardamos y luego salimos sin problema
            guardar_binario("inventario.bin", inventario)
            print("\n[+] Cambios guardados exitosamente.")
            return True

        if opcion == 1:
            # El usuario quiere salir sin guardar.
            # Salimos sin problema
            return True

        # Regresamos al menú
        return False


def main():
    inventario = importar_inventario()
    cambios = False

    clear()
    while True:
        match menu():
            # Mostrar inventario
            case 0:
                mostrar_inventario(inventario)
                clear()

            # Buscar producto
            case 1:
                cambio = buscar(inventario)
                clear()
                if cambio:
                    print("[*] Inventario actualizado existosamente.\n")
                    cambios = True

            # Ingresar producto
            case 2:
                inventario, cambio = ingresar_producto(inventario)
                clear()
                if cambio:
                    print("[*] Inventario actualizado existosamente.\n")
                    cambios = True

            # Egresar producto
            case 3:
                inventario, cambio = egresar_producto(inventario)
                clear()
                if cambio:
                    print("[*] Inventario actualizado existosamente.\n")
                    cambios = True

            # Guardar cambios
            case 4:
                guardar_binario("inventario.bin", inventario)
                clear()
                print("[+] Los cambios han sido guardados exitosamente.\n")
                cambios = False

            # Salir
            case 5:
                if salir(inventario, cambios):
                    return
                clear()


if __name__ == '__main__':
    main()


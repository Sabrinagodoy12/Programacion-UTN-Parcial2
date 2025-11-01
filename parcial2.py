import csv 
import os

NOMBRE_ARCHIVO = "productos.csv"

#Si existe el archivo CSV lo lee y devuelve una lista de diccionarios con título y cantidad
def obtener_catalogo(nombre_archivo):
    catalogo = []

    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                titulo = fila["TITULO"].strip()
                cantidad = int(fila["CANTIDAD"])
                catalogo.append({"TITULO": titulo, "CANTIDAD": cantidad})

    return catalogo

#Esta función guarda el catálogo en el formato de archivo csv. Sobrescribe el archivo con los datos actuales del catálogo.
def guardar_catalogo(nombre_archivo, catalogo):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        campos = ["TITULO", "CANTIDAD"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        
        for libro in catalogo:
            escritor.writerow(libro)

#Esta función normaliza el título eliminando espacios extra y convirtiéndolo a minúsculas.
def limpiar_titulo(titulo):
    partes = titulo.strip().lower().split()
    resultado = ""

    for i in range(len(partes)):
        resultado += partes[i]
        if i < len(partes) - 1:
            resultado += " "
    return resultado

#Esta función busca un libro en el catálogo evitando sensibilidades por mayúscula o espacios 
def buscar_libro(catalogo, buscar_titulo):
    titulo_sin_espacios = limpiar_titulo(buscar_titulo)
    
    for i in range(len(catalogo)):
        titulo_catalogo = limpiar_titulo(catalogo[i]["TITULO"])
        if titulo_catalogo == titulo_sin_espacios:
            return i
    return -1

#Esta función valida que la entrada sea un número entero positivo.
def pedir_entero(mensaje):
    valor = input(mensaje)

    while not valor.isdigit():
        valor = input("El número ingresado no es válido, por favor intente de nuevo con otro número: ")
    return int(valor)

#Esta función pide un nombre de libro y luego, si este no es repetido o esta en blanco, lo agrega al archivo
def ingresar_titulos(catalogo, nombre_archivo):
    #Se le solicita al usuario cuántos libros quiere ingresar
    cantidad = pedir_entero("¿Cuántos libros desea ingresar?: ")

    #Con un bucle va solicitando los títulos de los libros que desea ingresar hasta llegar a la cantidad mencionada
    for i in range(cantidad):
        print(f"\nIngresando libro {i + 1} de {cantidad}:")

        titulo = input("Ingrese el Título que desea agregar: ").strip()

        #Valida que el título no este en blanco o ya exista, si esto es así muestra un mensaje de error. Sino lo agrega al catálogo
        while titulo == "" or buscar_libro(catalogo, titulo) != -1:
            titulo = input("Título inválido o duplicado. Ingrese otro: ").strip()

        stock = pedir_entero("Cantidad de ejemplares: ")
        catalogo.append({"TITULO": titulo, "CANTIDAD": stock})

    guardar_catalogo(nombre_archivo, catalogo)
    print("\nCarga de títulos completada.\n")

#Esta función muestra el catálogo completo de libros, si esta en cero muestra un mensaje y sino muestra el catálogo con los títulos y la cantidad de cada libro.
def mostrar_catalogo(catalogo):
    #Si la longitud del catálogo es igual a 0 entonces muestra un mensaje indicando que no hay libros
    if len(catalogo) == 0:
        print("No hay libros cargados.\n")

    #Si no, muestra el catálogo completo, recorriendo el catálogo e indicando cada libro con la cantidad de ejemplares correspondientes.
    else:
        print("\n--- CATÁLOGO COMPLETO ---")

        for libro in catalogo:
            print(f"{libro['TITULO']} - {libro['CANTIDAD']} ejemplares")
        print()

#Esta función permite mostrar solo los títulos
def mostrar_titulos(catalogo):
    for libro in catalogo:
        print(f"- {libro['TITULO']}")

#Esta función permite ingresar ejemplares a los títulos que ya existen en el catálogo
def ingresar_ejemplares(catalogo, nombre_archivo):
    #Primero muestra la lista de nombres para que el usuario pueda elegir entre ellos
    print("\n--- Nuestros libros ---")
    mostrar_titulos(catalogo)

    #Solicita el título al usuario y verifica que exista
    titulo = input("\nIngrese el título del libro que desea ingresar ejemplares: ")
    indice = buscar_libro(catalogo, titulo)

    #Si el título se encuentra fuera del catálogo le muestra un mensaje al usuario indicandole que no éxiste
    if indice == -1:
        print("El título no existe.\n")
    #Si el título existe le pide la cantidad de ejemplares que desea sumar al usuario, y los suma a la cantidad actual, luego actualiza esto en el catálogo
    else:
        agregar = pedir_entero("¿Cuántos ejemplares desea sumar?: ")
        catalogo[indice]["CANTIDAD"] += agregar

        guardar_catalogo(nombre_archivo, catalogo)
        print("Ejemplares actualizados.\n")
        mostrar_catalogo(catalogo)

#Esta función consulta la disponibilidad de un libro que el usuario seleccione
def consultar_disponibilidad(catalogo):
    #Primero muestra la lista con los nombres para que el usuario pueda elegir entre ellos
    print("\n--- Nuestros libros ---")
    mostrar_titulos(catalogo)

    #Le solicita el título al usuario y verifica que exista
    titulo = input("\nIngrese el título a consultar: ")
    indice = buscar_libro(catalogo, titulo)

    #Si el título se encuentra fuera del catálogo le muestra un mensaje al usuario informandole ésto
    if indice == -1:
        print("El título no se encuentra en el catálogo.\n")
    
    #Si se encuentra el título, lo muestra con la cantidad de ejemplares correspondientes
    else:
        cantidad = catalogo[indice]["CANTIDAD"]
        print(f"'{catalogo[indice]['TITULO']}' tiene {cantidad} ejemplares disponibles.\n")

#Esta función muestra los libros que tienen cantidad de stock en 0
def listar_agotados(catalogo):
    agotados = []

    #Recorre el catálogo y si la cantidad es igual a 0 entonces se agrega a la lista de agotados
    for libro in catalogo:
        if libro["CANTIDAD"] == 0:
            agotados.append(libro)
        
    #Si la lista esta en cero le muestra un mensaje al usuario informandole ésto
    if len(agotados) == 0:
        print("No hay libros agotados.\n")

    #Si la lista tiene al menos un elemento entonces muestra su título
    else:
        print("\n--- LIBROS AGOTADOS ---")

        for libro in agotados:
            print(libro["TITULO"])
        print()

#Esta función le permite al usuario ingresar un nuevo título con la cantidad correspondiente
def agregar_titulo(catalogo, nombre_archivo):
    titulo = input("Ingrese el título: ").strip()

    #Si el usuario ingresa un título en blanco o repetido muestra un mensaje de error
    while titulo == "" or buscar_libro(catalogo, titulo) != -1:
        titulo = input("Título inválido o duplicado. Ingrese otro título: ").strip()

    #Se le solicita al usuario la cantidad de libros que desea ingresar
    cantidad = pedir_entero("Cantidad inicial: ")

    #Agrega los libros ingresados con su cantidad y los guarda. Luego muestra un mensaje de éxito
    catalogo.append({"TITULO": titulo, "CANTIDAD": cantidad})
    guardar_catalogo(nombre_archivo, catalogo)

    print("Título agregado correctamente.\n")

#Esta función le permite al usuario devolver un libro (se suma 1 al stock actual) o pedir un préstamo de un libro (se resta 1 al stock actual)
def actualizar_ejemplares(catalogo, nombre_archivo):
    #Primero se le muestra el catálogo actual con su stock para que seleccione
    mostrar_catalogo(catalogo)

    titulo = input("\nIngrese el título: ")
    indice = buscar_libro(catalogo, titulo)

    if indice == -1:
        print("El título no existe.\n")
        return
    
    opcion = input("Coloque la letra de la opción que desea: \nP. Préstamo\nD. Devolución ").lower()

    #Si elije préstamo se verifica que la cantidad sea mayor a 1 y se le resta 1 al stock actual y se actualiza en el catálogo
    if opcion == "p":
        if catalogo[indice]["CANTIDAD"] > 0:
            catalogo[indice]["CANTIDAD"] -= 1
            guardar_catalogo(nombre_archivo, catalogo)
            print("Préstamo realizado correctamente.\n")
        else:
            print("No hay ejemplares disponibles para préstamo.\n")

    #Si elije devolución se le suma uno a la cantidad actual del título seleccionado y se actualiza en el catálogo
    elif opcion == "d":
        catalogo[indice]["CANTIDAD"] += 1
        guardar_catalogo(nombre_archivo, catalogo)
        print("Devolución registrada.\n")
    
    #Si el usuario no ingresa una de las opciones propuestas
    else:
        print("Opción inválida.\n")

#Esta función muestra el menú. Contiene el bucle principal del programa con las opciones del sistema.
def mostrar_menu():
    catalogo = obtener_catalogo(NOMBRE_ARCHIVO)

    #Este bucle repite el menú hasta que el usuario elija la opción para salir
    while True:
        print("====== MENÚ DE PRODUCTOS ======")
        print("1. Ingresar títulos")
        print("2. Ingresar ejemplares")
        print("3. Mostrar catálogo")
        print("4. Consultar disponibilidad")
        print("5. Listar agotados")
        print("6. Agregar título")
        print("7. Actualizar ejemplares (Préstamo o devolución)")
        print("8. Salir del menú")
        print("="*35)

        opcion = input("Ingrese opción: ").strip()

        #Le permite al usuario seleccionar entre las opciones mencionadas
        match opcion:
            case "1":
                ingresar_titulos(catalogo, NOMBRE_ARCHIVO)
            case "2":
                ingresar_ejemplares(catalogo, NOMBRE_ARCHIVO)
            case "3":
                mostrar_catalogo(catalogo)
            case "4":
                consultar_disponibilidad(catalogo)
            case "5":
                listar_agotados(catalogo)
            case "6":
                agregar_titulo(catalogo, NOMBRE_ARCHIVO)
            case "7":
                actualizar_ejemplares(catalogo, NOMBRE_ARCHIVO)
            case "8":
                print("Muchas gracias por visitar nuestra aplicación. Vuelva pronto.\n")
                break
            case _:
                print("La opción seleccionada no no se encuentra en nuestro menú, por favor intentelo con una opción válida\n")

mostrar_menu()
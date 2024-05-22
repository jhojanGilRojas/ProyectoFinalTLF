# Pedir al usuario que ingrese el número de filas y columnas
continuar = True
num_filas = []
num_columnas = []
while continuar:
    alfabeto  = input("Ingrese una letra del alfabeto: ")
    num_filas.append(alfabeto)
    continuar = True
    nodos = input("Ingrese los nodos ")
    num_columnas.append(nodos)
    respuesta = input("¿Desea ingresar otro valor? (s/n): ")
    if respuesta.lower() != 's':
        continuar = False  # Detener el bucle si el usuario no desea continuar


    # llenar tabla
matriz = []
matriz.append(num_filas)


# Llenar la matriz con los valores ingresados por el usuario
for i in range(len(num_filas)+1):
    fila = []  # Inicializar una fila vacía
    for j in range(len(num_columnas)+1):
        valor = (input(f"Ingrese el valor para la posición ({i+1}, {j+1}): "))
        fila.append(valor)  # Agregar el valor a la fila
    matriz.append(fila)  # Agregar la fila a la matriz

# Imprimir la matriz
print("La matriz ingresada es:")
for fila in matriz:
    print(fila)

# Verificar si es un automata finito no determinista
# Obtener el número de filas y columnas de la matriz
num_filas = len(matriz)
num_columnas = len(matriz[0]) if matriz else 0

# Definir la posición en la que deseas verificar
fila_a_verificar = 0
columna_a_verificar = 0


# Verificar si hay una coma en la posición especificada
if fila_a_verificar < num_filas and columna_a_verificar < num_columnas:
    elemento = matriz[fila_a_verificar][columna_a_verificar]

    if ',' in elemento:
        print("El automata es AFND")
else:
    print("La posición especificada está fuera del rango de la matriz.")

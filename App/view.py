"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


from functools import partial
import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

fnms = ("201801-1-citibike-tripdata.csv",
        "201801-2-citibike-tripdata.csv",
        "201801-3-citibike-tripdata.csv",
        "201801-4-citibike-tripdata.csv"
        )

option = 1

filename = fnms[option - 1]

recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""


def showMenu() -> str:

    print("\n" + "*"*50)
    print("Bienvenido")
    print("1- Inicializar Estructuras")
    print("2- Cargar información de CitiBike")
    print("3- Req 1. Cantidad de Clusters de Viajes")
    print("4- Req 2. Ruta turística Circular")
    print("5- Req 3. Estaciones Críticas")
    print("6- Req 4. Ruta turística por resistencia")
    print("7- Req 5. Recomendador de Rutas")
    print("8- Req 6. Ruta de interés turístico")
    print("9- Req 7. Identificación de Estaciones para Publicidad")
    print("10- Req 8. Identificador de Bicicletas de Mantenimiento")
    print("0- Salir")
    enter = int(input("*"*50 + "\n>"))
    return enter


def opt2(citibikes, filename, recursionLimit):
    print("\nCargando información de CitiBikes....")
    controller.loadStations(citibikes, filename)
    numedges = controller.totalTrips(citibikes)
    numvertex = controller.totalStations(citibikes)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def opt3():
    1


def opt4():
    1


def opt5():
    1


def opt6():
    1


def opt7():
    1


def opt8():
    1


def opt9():
    1


def opt10():
    1


def main():
    while 1:
        enter = showMenu()
        if enter == 1:
            cbk = controller.init()
        elif enter == 2:
            time = timeit.timeit(
                partial(opt2, cbk, filename, recursionLimit), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 3:
            time = timeit.timeit(opt3, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 4:
            time = timeit.timeit(opt4, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 5:
            time = timeit.timeit(opt5, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 6:
            time = timeit.timeit(opt6, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 7:
            time = timeit.timeit(opt7, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 8:
            time = timeit.timeit(opt8, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 9:
            time = timeit.timeit(opt9, number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 10:
            time = timeit.timeit(opt10, number=1)
            print(f"Tiempo de ejecución: {time}")
        else:
            print("Hasta pronto!")
            break


main()

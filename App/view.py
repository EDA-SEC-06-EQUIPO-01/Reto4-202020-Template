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
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
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

fnms = (
    "201801-1-citibike-tripdata.csv",
    "201801-2-citibike-tripdata.csv",
    "201801-3-citibike-tripdata.csv",
    "201801-4-citibike-tripdata.csv",
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

    print("\n" + "*" * 50)
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
    enter = int(input("*" * 50 + "\n>"))
    return enter


def opt2(citibikes, filename, recursionLimit):
    print("\nCargando información de CitiBikes....")
    controller.loadStations(citibikes, filename)
    numedges = controller.totalTrips(citibikes)
    numvertex = controller.totalStations(citibikes)
    print("Numero de vertices: " + str(numvertex))
    print("Numero de arcos: " + str(numedges))
    print("El limite de recursion actual: " + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print("El limite de recursion se ajusta a: " + str(recursionLimit))


def opt3(citibikes, id1, id2):
    print(f"Los clusteres son {controller.connectedComponents(citibikes)}")
    print(
        f"Las estaciones {id1} y {id2} {'si' if controller.sameCC(citibikes, id1, id2) else 'no'} estan fuertemente conectadas"
    )


def opt4(cbk, id_init, time_available):
    res = controller.req2(cbk, id_init, time_available)

    print(f"Son en total {len(res)} trayectos circulares")
    print()

    for c1, travel in enumerate(res):
        print(f"Trayecto circular #{c1+1}")
        print()
        s = 0
        t = None
        for c2, item in enumerate(travel):
            print(f"-Viaje #{c2+1}")
            i = item[2]
            print(f"   Salida: {i[1]}")
            print(f"   Llegada: {i[2]}")
            print(f"   Duracion: {int(i[0]) // 60} minutos")
            print()
            s += int(i[0]) // 60
            t = (c2 + 1) * 20

        print(f" Duracion total: {t + s}")
        print()

    print()


def opt5(citibikes):
    rta = controller.req3(citibikes)
    print(
        f" Las 3 estaciones principales a las que mas bicicletas llegan provenientes de otras estaciones: {rta[0]} , Las 3 estaciones de las que más viajes salen hacia otras estaciones: {rta[1]} , las 3 estaciones menos utilizadas por los turistas: {rta[0]}")


def opt6(citibikes, startID, maxTime):
    lst = controller.req4(citibikes, startID, maxTime)
    iniEst = m.get(citibikes["stations"], startID)["value"]["name"]
    if lt.isEmpty(lst):
        print(f"No se encontraron caminos desde la estación {iniEst}")
    else:
        cont = 1
        print(f"Los posibles viajes son:")
        for i in controller.travel_list(lst):
            print(f"{cont}.\n\tEstación Inicial: {iniEst}")
            print(f"\tEstación Final: {i[0]}")
            print(
                f"\tDuración de viaje: {i[1]//60} minutos y {i[1]%60} segundos.")
            cont += 1


def opt7(citibikes, de):
    a = controller.req5(citibikes, de)

    print(f"Estacion de salida: {a[0]}")
    print(f"Estacion de llegada: {a[1]}")
    if a[2]:
        print("Id de estaciones recorrido:")
        for c, i in enumerate(a[2]):
            print(f"{c + 1} - {i['vertexA']}")
        print(f"{c+2} - {i['vertexB']}")
    else:
        print("No hay ruta entre ellas")


def opt8(citibikes, lati, loni, latf, lonf):
    print()
    init, final, minPath = controller.req6(citibikes, lati, loni, latf, lonf)

    print(f"La estación más cercana al punto inicial es '{init['name']}'.")
    print(f"La estación más cercana al punto final es '{final['name']}'.")
    if minPath is None:
        print("No existe un camino entre las estaciones.")
    else:
        ls_str = []
        duration = 0
        while not stack.isEmpty(minPath):
            el = stack.pop(minPath)
            ls_str.append((el["vertexA"], el["vertexB"]))
            duration += int(el["weight"])

        ls_str = "\n\t".join(
            [
                f"'{m.get(citibikes['stations'], i)['value']['name']}'"
                + f" -> '{m.get(citibikes['stations'], j)['value']['name']}'"
                for i, j in ls_str
            ]
        )

        print(f"La duración del camino más corto es de {duration}")
        print(f"Las estaciones del camino son:", end="\n\t")
        print(ls_str)


def opt9(citibikes, minAge, maxAge):
    ret = controller.req7(citibikes, minAge, maxAge)
    if lt.isEmpty(ret):
        print(
            f"No hubo ningún viaje realizado por personas entre {minAge} y {maxAge} años."
        )
    elif lt.size(ret) > 1:
        print(
            f"Los viajes más frecuentes de personas entre {minAge} y {maxAge} años, son:"
        )
        for i in controller.travel_list(ret):
            st = m.get(citibikes["stations"], i[0])["value"]["name"]
            end = m.get(citibikes["stations"], i[1])["value"]["name"]
            print(f"\t{st} -> {end}")
    else:
        print(
            f"El viaje más frecuente de personas entre {minAge} y {maxAge} es:")
        st = m.get(citibikes["stations"], lt.lastElement(ret)[0])[
            "value"]["name"]
        end = m.get(citibikes["stations"], lt.lastElement(ret)[1])[
            "value"]["name"]
        print(f"\t{st} -> {end}")


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
            id1 = input("Ingrese el id de la 1ra estacion: ")
            id2 = input("Ingrese el id de la 2da estacion: ")
            time = timeit.timeit(partial(opt3, cbk, id1, id2), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 4:
            id_init = input("Ingrese el id de la estacion de inicio: ")
            time_available = int(
                input("Ingrese el tiempo disponible(minutos): "))
            time = timeit.timeit(
                partial(opt4, cbk, id_init, time_available), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 5:
            time = timeit.timeit(partial(opt5, cbk), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 6:
            startID = input("Ingrese el ID de la estación inicial: ")
            maxTime = float(
                input("Ingrese el tiempo máximo del recorrido (en minutos): ")
            )
            time = timeit.timeit(
                partial(opt6, cbk, startID, maxTime), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 7:
            d = [
                "0-10",
                "11-20",
                "21-30",
                "31-40",
                "41-50",
                "51-60",
                "60+",
            ]
            de = [(0, 10), (11, 20), (21, 30), (31, 40),
                  (41, 50), (51, 60), (61, 100)]
            print("Opciones")
            for c, k in enumerate(d):
                print(f"{c+1}) {k}")
            print()

            ra = int(input("Seleccione una opcion: "))
            time = timeit.timeit(partial(opt7, cbk, de[ra - 1]), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 8:
            print("Punto inicial")
            lati = float(input("Digite la latitud del punto de partida: "))
            loni = float(input("Digite la longitud del punto de partida: "))
            print("Punto final")
            latf = float(input("Digite la latitud del punto de llegada: "))
            lonf = float(input("Digite la longitud del punto de llegada: "))
            time = timeit.timeit(
                partial(opt8, cbk, lati, loni, latf, lonf), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 9:
            minAge = int(input("Digite la edad mínima: "))
            maxAge = int(input("Digite la edad máxima: "))
            time = timeit.timeit(partial(opt9, cbk, minAge, maxAge), number=1)
            print(f"Tiempo de ejecución: {time}")
        elif enter == 10:
            time = timeit.timeit(opt10, number=1)
            print(f"Tiempo de ejecución: {time}")
        else:
            print("Hasta pronto!")
            break


main()

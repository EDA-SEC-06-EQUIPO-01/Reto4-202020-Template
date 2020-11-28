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
import config
import copy
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import dfs
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import map as map
from DISClib.ADT import stack
from DISClib.DataStructures import adjlist as g
import time

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def compareStations(stat, keyval):
    return 0 if stat == keyval["key"] else (1 if stat > keyval["key"] else -1)


def compare(el1, el2):
    return 0 if el1 == el2 else (1 if el1 > el2 else -1)


def newCitibike():
    try:
        citibike = {}
        citibike["stations"] = m.newMap(
            numelements=1000, maptype="PROBING", comparefunction=compareStations
        )
        citibike["graph"] = gr.newGraph(
            datastructure="ADJ_LIST",
            directed=True,
            size=1000,
            comparefunction=compareStations,
        )
        citibike["paths"] = None
        citibike["components"] = None
        citibike["tripsinfo"] = lt.newList(datastructure="ARRAY_LIST")

        return citibike
    except Exception as e:
        error.reraise(e, "model:newCitibike")


def addStation(citibike, stationID):
    if not gr.containsVertex(citibike["graph"], stationID):
        gr.insertVertex(citibike["graph"], stationID)
    return citibike


def addTrip(citibike, trip):
    addStation(citibike, trip["start station id"])
    addStation(citibike, trip["end station id"])
    addArc(
        citibike,
        trip["start station id"],
        trip["end station id"],
        int(trip["tripduration"]),
    )
    st_station = {}
    end_station = {}
    tripsinfo = {}
    for i in trip:
        if "start station" in i and not i.endswith("id"):
            key = i.replace("start station ", "")
            st_station[key] = trip[i]
            tripsinfo[i] = trip[i]
        elif "end station" in i and not i.endswith("id"):
            key = i.replace("end station ", "")
            end_station[key] = trip[i]
            tripsinfo[i] = trip[i]
        else:
            tripsinfo[i] = trip[i]
    m.put(citibike["stations"], trip["start station id"], st_station)
    m.put(citibike["stations"], trip["end station id"], end_station)
    lt.addLast(citibike["tripsinfo"], tripsinfo)


def addArc(citibike, origin, destination, duration):
    if gr.getEdge(citibike["graph"], origin, destination) is None:
        gr.addEdge(citibike["graph"], origin, destination, duration)

    return citibike


# Funciones para agregar informacion al grafo

# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(citibikes):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    citibikes["components"] = scc.KosarajuSCC(citibikes["graph"])
    return scc.connectedComponents(citibikes["components"])


def sameCC(sc, station1, station2):
    sct = scc.KosarajuSCC(sc["graph"])
    return scc.stronglyConnected(sct, station1, station2)


round_path = []


def req2(cbk, id_init, time_available):
    sct = scc.KosarajuSCC(cbk["graph"])

    print()

    search = {"source": id_init, "visited": None}

    search["visited"] = map.newMap(
        numelements=g.numVertices(cbk["graph"]),
        maptype="PROBING",
        comparefunction=cbk["graph"]["comparefunction"],
    )

    map.put(search["visited"], id_init, {"marked": True, "edgeTo": None})

    time_s = time_available * 60
    dfs_search(
        search, cbk["graph"], id_init, [], sct, id_init, cbk["tripsinfo"], time_s
    )

    global round_path
    r_path = copy.deepcopy(round_path)
    round_path = []

    return r_path


def ss(smt, init, final):
    for item in travel_lst(smt):
        if init == item["start station id"] and final == item["end station id"]:
            return (
                item["tripduration"],
                item["start station name"],
                item["end station name"],
            )


def dfs_search(search, graph, vertex, path, sct, init_v, info, times):
    path_local = copy.deepcopy(path)
    adjlst = g.adjacents(graph, vertex)
    adjslstiter = it.newIterator(adjlst)

    while it.hasNext(adjslstiter):
        w = it.next(adjslstiter)
        if scc.stronglyConnected(sct, vertex, w):
            a = ss(info, vertex, w)
            s = sum([int(item[2][0]) for item in path])
            if s + int(a[0]) <= times - (20 * 60):
                if w == init_v:
                    inf = (vertex, w, a)
                    path_local.append(inf)
                    round_path.append(path_local)

                visited = map.get(search["visited"], w)
                if visited is None:
                    map.put(search["visited"], w, {"marked": True, "edgeTo": vertex})
                    inf = (vertex, w, a)
                    path_local.append(inf)
                    dfs_search(
                        search,
                        graph,
                        w,
                        path_local,
                        sct,
                        init_v,
                        info,
                        times - (20 * 60),
                    )
                    path_local.pop()


def minimumCostPaths(citibikes, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    citibikes["paths"] = djk.Dijkstra(citibikes["graph"], initialStation)
    return citibikes


def hasPath(citibikes, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(citibikes["paths"], destStation)


def minimumCostPath(citibikes, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.pathTo(citibikes["paths"], destStation)


def totalStations(citibikes):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(citibikes["graph"])


def totalTrips(citibikes):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(citibikes["graph"])


def req4(citibikes, startID, maxTime):
    map_dfs = dfs.DepthFirstSearch(citibikes["graph"], startID)
    lista = lt.newList(cmpfunction=compare)
    minimumCostPaths(citibikes, startID)
    for i in travel_map(map_dfs["visited"]):
        estFin = i["value"]["edgeTo"]
        if estFin:
            minCost = djk.distTo(citibikes["paths"], estFin)
            if minCost / 60 < maxTime and estFin != startID:
                nomEstFin = m.get(citibikes["stations"], estFin)["value"]["name"]
                if not lt.isPresent(lista, (nomEstFin, minCost)):
                    lt.addLast(lista, (nomEstFin, minCost))
    return lista


def distance(i_lat, i_lon, f_lat, f_lon):
    return (
        (float(i_lat) - float(f_lat)) ** 2 + (float(i_lon) - float(f_lon)) ** 2
    ) ** (1 / 2)


def req5(citibikes, de):
    print()

    go = dict()
    ba = dict()

    for i in travel_lst(citibikes["tripsinfo"]):
        dff = 2020 - int(i["birth year"])
        if de[0] <= dff <= de[1]:
            c1 = go.get(i["start station name"], [0, 0])
            c1[0] += 1
            t1 = [c1[0], i["start station id"]]

            go[i["start station name"]] = t1

            c2 = ba.get(i["end station name"], [0, 0])
            c2[0] += 1
            t2 = [
                c2[0],
                i["end station id"],
            ]
            ba[i["end station name"]] = t2
    n1 = max(go, key=go.get)
    n2 = max(ba, key=ba.get)
    k1 = go[n1]
    k2 = ba[n2]

    gg = djk.Dijkstra(citibikes["graph"], k1[1])

    if djk.hasPathTo(gg, k2[1]):
        ww = djk.pathTo(gg, k2[1])
        ll = [i for i in travel_lst(ww)]
        return (n1, n2, ll)
    else:
        return (n1, n2, None)


def req6(citibike, lati, loni, latf, lonf):
    # Paso 1: Encontrar la estación más cercana a la latitud y longitud dados.
    dist_in = 10000
    dist_fn = 10000
    for i in travel_map(citibike["stations"]):
        new_dist_in = distance(
            lati, loni, i["value"]["latitude"], i["value"]["longitude"]
        )
        new_dist_fn = distance(
            latf, lonf, i["value"]["latitude"], i["value"]["longitude"]
        )

        if new_dist_in < dist_in:
            dist_in = new_dist_in
            st_id = i["key"]
        if new_dist_fn < dist_fn:
            dist_fn = new_dist_fn
            fn_id = i["key"]

    minimumCostPaths(citibike, st_id)
    minPath = djk.pathTo(citibike["paths"], fn_id)

    return (
        m.get(citibike["stations"], st_id)["value"],
        m.get(citibike["stations"], fn_id)["value"],
        minPath,
    )


def req7(citibikes, minAge, maxAge):
    counter = {}
    for i in travel_lst(citibikes["tripsinfo"]):
        # (2020 - año nacimiento)
        if (time.localtime()[0] - int(i["birth year"])) in range(minAge, maxAge):
            tuplekey = (i["start station id"], i["end station id"])
            counter[tuplekey] = counter.get(tuplekey, 0) + 1
    maxnum = 0
    ids = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compare)
    for i in counter:
        if counter[i] > maxnum:
            maxnum = counter[i]
            ids = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compare)
            lt.addLast(ids, i)
        elif counter[i] == maxnum:
            lt.addLast(ids, i)
    return ids


# ==============================
# Funciones Helper
# ==============================


def travel_iter(iter):
    while it.hasNext(iter):
        yield it.next(iter)


def travel_lst(lista, parameter=None):
    iter = it.newIterator(lista)
    while it.hasNext(iter):
        node = it.next(iter)
        if parameter:
            yield node[parameter]
        else:
            yield node


def travel_map(mapa):
    keys = m.keySet(mapa)
    for i in travel_lst(keys):
        yield m.get(mapa, i)


# ==============================
# Funciones de Comparacion
# ==============================

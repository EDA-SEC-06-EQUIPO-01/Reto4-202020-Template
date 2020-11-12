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
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

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
    path = djk.pathTo(citibikes["paths"], destStation)
    return path


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


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

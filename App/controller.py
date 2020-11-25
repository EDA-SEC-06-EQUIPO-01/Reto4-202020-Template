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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    citibike = model.newCitibike()
    return citibike


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadStations(citibike, filename: str):
    filename = cf.data_dir + filename
    file = csv.DictReader(open(filename, encoding="utf-8"), delimiter=",")
    c = 0
    for trip in file:
        c += 1
        model.addTrip(citibike, trip)

    print(f"Se cargaron {c} viajes")


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStations(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStations(analyzer)


def totalTrips(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalTrips(analyzer)


def sameCC(sc, station1, station2):
    return model.sameCC(sc, station1, station2)


def connectedComponents(citibikes):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(citibikes)


def minimumCostPaths(citibikes, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(citibikes, initialStation)


def hasPath(citibikes, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(citibikes, destStation)


def minimumCostPath(citibikes, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(citibikes, destStation)


def req6(citibikes, lati, loni, latf, lonf):
    return model.req6(citibikes, lati, loni, latf, lonf)

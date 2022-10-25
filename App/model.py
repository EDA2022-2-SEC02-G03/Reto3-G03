"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from select import select
import time
import config as cf
from datetime import datetime as dt
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'videojuegos': None,
                'plataformas': None,
                'fechaLanzamiento': None,
                'fechaRecord': None,
                'intentos': None,
                'duracion': None,
                }

    analyzer["videojuegos"] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer['plataformas'] = om.newMap(omaptype='BST')
                                      
    
    return analyzer

# Funciones para agregar informacion al catalogo

def addVideojuegos(analyzer, game): 

    lt.addLast(analyzer["videojuegos"], game)
    updatePlatforms(analyzer["plataformas"], game)
    

    return analyzer




def updatePlatforms(map, game):
    print(game)
    plataforma = game["Platforms"]
    entry = om.get(map, plataforma)
    if entry is None:
        platform_entry = newPlatformsEntry(game)
        om.put(map, plataforma, platform_entry)
    else:
        platform_entry = me.getValue(entry)
    addPlatformsIndex(platform_entry, game)
    return map


def newPlatformsEntry(game): 
    
    entry = {'categoryIndex': None, 'lstgames': None}
    entry['categoryIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
    entry['lstgames'] = lt.newList('SINGLE_LINKED', compareIds)
    return entry


def addPlatformsIndex(platform_entry, game):
    
    lst = platform_entry['lstgames']
    lt.addLast(lst, game)
    categoryIndex = platform_entry['categoryIndex']
    category = m.get(categoryIndex, game['Game_Id'])
    if (category is None):
        entry = newIDEntry(game['Game_Id'], game)
        lt.addLast(entry['lstIDs'], game)
        m.put(categoryIndex, game['Game_Id'], entry)
    else:
        entry = me.getValue(category)
        lt.addLast(entry['lstIDs'], game)
    return platform_entry


def newIDEntry(IDgrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    IDentry = {"ID": None, "lstIDs": None}
    IDentry["ID"] = IDgrp
    IDentry["lstIDs"] = lt.newList("SINGLE_LINKED", compareIds)
    lt.addLast(IDentry["lstIDs"], crime)
    return IDentry

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1



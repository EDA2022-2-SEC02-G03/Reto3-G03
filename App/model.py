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
from DISClib.Algorithms.Sorting import mergesort as ms
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
                "categorias": None, "Game By Release Date":None
                }

    analyzer["videojuegos"] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer['categorias'] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer['Game By Release Date'] = om.newMap(omaptype='RBT', comparefunction=compareDates)
    analyzer['Game By Platform'] = m.newMap(numelements=30, maptype='PROBING', comparefunction=comparePlatforms)
                                     
    
    return analyzer

# Funciones para agregar informacion al catalogo

# ============================== 
# Carga del Req 1
def addVideojuegos(analyzer, game): 

    lt.addLast(analyzer["videojuegos"], game)
    updateGame(analyzer, game)

    return analyzer

def updateGame(map, game):
    #Mete al arbol el game segun su fecha de lanzamiento #Req 1
    """
    """
    #Filtrado por plataforma 
    plataforma=game["Platforms"].split(", ")
    for i in plataforma:
        if i=="": #Para cuando no tiene plataformas 
            continue
        else:
            entry = m.get(map["Game By Platform"], i) #Busca la llave en el arbol
            if entry is None:
                datentry = newDataEntry(game)

                addDateIndex(datentry, game)
                m.put(map["Game By Platform"], i, datentry)
            else:
                datentry = me.getValue(entry)
                addDateIndex(datentry, game)


def newDataEntry(game):
    #Crea una valor para la llave en el indice por fecha #Req 1
    entry = {"omYear": None}
    entry['omYear'] = om.newMap(omaptype='RBT', comparefunction=compareDates)
    return entry

def addDateIndex(datentry, game):
    #Actualizar el valor de la llave #Req 1
    mapa_ordenado=datentry["omYear"]
    release_date = game["Release_Date"]
    release_date= dt.strptime(release_date, '%y-%m-%d')
    entry = om.get(mapa_ordenado, release_date)
    if entry is None:
        datentry = lt.newList('SINGLE_LINKED', compareIds)
        om.put(mapa_ordenado, release_date, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry, game)

def comparePlatforms(keyname, platform):
    """
    Compara dos nombres de categorias
    """
    platformentry = me.getKey(platform)
    if (keyname == platformentry):
        return 0
    elif (keyname > platformentry):
        return 1
    else:
        return -1
    # Compara plataformas #Req 1



def addCategory(analyzer, game): 

    lt.addLast(analyzer["categorias"], game)

    

    return analyzer


def updatePlatforms(map, game):
    #print(game)
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
                                     )
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

def getFirstGames(analyzer):
    games = analyzer["videojuegos"]
    firstgames= lt.newList(datastructure='ARRAY_LIST')
    if lt.size(games) > 3:
        for i in range(1,4):
            game= lt.getElement(games,i)
            lt.addLast(firstgames,game)
    else:
        for i in range (1,4):
            game= lt.getElement(games,i)
            lt.addLast(firstgames,game)
    return firstgames

def getLastGames(analyzer):
    games = analyzer["videojuegos"]
    lastgames= lt.newList(datastructure='ARRAY_LIST')
    if lt.size(games) > 3:
        for i in range(lt.size(games)-2,lt.size(games)+1):
            game= lt.getElement(games,i)
            lt.addLast(lastgames,game)
    else:
        for i in range (1,4):
            game= lt.getElement(games,i)
            lt.addLast(lastgames,game)
    return lastgames

def getFirstCategory(analyzer):
    categories = analyzer["categorias"]
    firstcategories= lt.newList(datastructure='ARRAY_LIST')
    if lt.size(categories) > 3:
        for i in range(1,4):
            category= lt.getElement(categories,i)
            lt.addLast(firstcategories,category)
    else:
        for i in range (1,4):
            category= lt.getElement(categories,i)
            lt.addLast(firstcategories,category)
    return firstcategories

def getLastCategory(analyzer):
    categories = analyzer["categorias"]
    lastcategories= lt.newList(datastructure='ARRAY_LIST')
    if lt.size(categories) > 3:
        for i in range(lt.size(categories)-2,lt.size(categories)+1):
            category= lt.getElement(categories,i)
            lt.addLast(lastcategories,category)
    else:
        for i in range (1,4):
            category= lt.getElement(categories,i)
            lt.addLast(lastcategories,category)
    return lastcategories


# Funciones para creacion de datos

# Funciones de consulta

#REQ1 
def Juegos_plataforma_rango(analyzer,plataforma_buscada,LimiteInferior,LimiteSuperior):
    abrol=m.get(analyzer["Game By Platform"],plataforma_buscada)
    LimiteInferior = dt.strptime(LimiteInferior, '%y-%m-%d')
    LimiteSuperior = dt.strptime(LimiteSuperior, '%y-%m-%d')
    if abrol is None:
        return None
    else:
        arbol=me.getValue(abrol)
        arbol=arbol["omYear"]
        lista=om.values(arbol,LimiteInferior,LimiteSuperior) #Queda guaradada una lista de listas, la información ya está ordenada
        juegos=lt.newList(datastructure='ARRAY_LIST') #Lista vacía donde se van a guardar los juegos
        for i in lt.iterator(lista):
            for j in lt.iterator(i):
                lt.addLast(juegos,j)

        juegos= ms.sort(juegos,compareYears) #Se ordena la lista de juegos por año    
        if lt.size(juegos) <5:
            final=juegos
        else:
            final=lt.subList(juegos,1,5)

        return lt.size(juegos),final










# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
#Req 1
def compareYears(game1, game2):
    release_game1= game1["Release_Date"] #Se obtiene la fecha de lanzamiento del juego 1
    release_game1= dt.strptime(release_game1, '%y-%m-%d') #Se convierte la fecha de lanzamiento del juego 1 a formato datetime
    abbreviation1= game1["Abbreviation"] #Se obtiene la abreviación del juego 1
    release_game2= game2["Release_Date"] #Se obtiene la fecha de lanzamiento del juego 2
    release_game2= dt.strptime(release_game2, '%y-%m-%d') #Se convierte la fecha de lanzamiento del juego 2 a formato datetime
    abbreviation2= game2["Abbreviation"] #Se obtiene la abreviación del juego 2

    if release_game1 < release_game2: #Se compara la fecha de lanzamiento del juego 1 con la fecha de lanzamiento del juego 2
        return True
    elif release_game1 == release_game2: #Si las fechas de lanzamiento son iguales, se compara la abreviación del juego 1 con la abreviación del juego 2
        if abbreviation1 < abbreviation2: # Si la abreviación del juego 1 es mayor que la abreviación del juego 2, se retorna True
            return True
        else:
            return False
    else:
        return False


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

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1



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

import math
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
    analyzer['Game By Player'] = om.newMap(omaptype='RBT', comparefunction=compareTimes)
    analyzer['Game By Time'] = om.newMap(omaptype='RBT', comparefunction=compareTimes)
    analyzer["Game by Id"] = m.newMap(numelements=30, maptype='PROBING', comparefunction=compareIds_hash) #Tabla de hash para el req 3 (Vacía)
    analyzer["Game By Runs"] = om.newMap(omaptype='RBT', comparefunction=compareIds) #Tabla de hash para el req 3 (Vacía)
    analyzer['Game By Record Date'] = om.newMap(omaptype='RBT', comparefunction=compareTimes)

    return analyzer

# Funciones para agregar informacion al catalogo

# ============================== 
# Carga del Req 1
def addVideojuegos(analyzer, game): 

    lt.addLast(analyzer["videojuegos"], game)
    updateGame(analyzer, game)
    addGameById(analyzer, game)

    return analyzer

def addGameById(map, game):
    #Mete al arbol el game segun su fecha de lanzamiento #Req 3
    """
    """
    id=game["Game_Id"]
    
    m.put(map["Game by Id"], id, game) 

def updateGame(map, game):
    #Mete al arbol el game segun su fecha de lanzamiento #Req 1
    """
    """
    
    #Filtrado por plataforma 
    plataforma=game["Platforms"].split(", ")
    
    for i in plataforma:
        entry = m.get(map["Game By Platform"], i) #Busca la llave en el arbol
        if entry is None:
            datentry = newDataEntry(game,i)

            addDateIndex(datentry, game)
            m.put(map["Game By Platform"], i, datentry)
        else:
            datentry = me.getValue(entry)
            addDateIndex(datentry, game)
    


def newDataEntry(game, plataforma):
    #Crea una valor para la llave en el indice por fecha #Req 1
    entry = {"omYear": None,"platform":plataforma}
    entry['omYear'] = om.newMap(omaptype='RBT', comparefunction=compareDates)
    entry["game_id"] = m.newMap(numelements=30, maptype='PROBING', comparefunction=compareIds_hash)
    return entry

def addDateIndex(datentry, game):
    #Actualizar el valor de la llave #Req 1
    mapa_ordenado=datentry["omYear"]
    hash_games=datentry["game_id"]
    
    release_date = game["Release_Date"]
    release_date= dt.strptime(release_date, '%y-%m-%d')
    entry = om.get(mapa_ordenado, release_date)
    if entry is None:
        datentry1 = lt.newList('SINGLE_LINKED', compareIds)
        om.put(mapa_ordenado, release_date, datentry1)
    else:
        datentry1 = me.getValue(entry)
    lt.addLast(datentry1, game)

    id=game["Game_Id"]
    m.put(hash_games, id, {"video":game,"registros":0})

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



#Carga del Req 2
def addCategory(analyzer, category): 

    lt.addLast(analyzer["categorias"], category)
    updateCategory(analyzer, category)
    updateDataGame(analyzer, category)

    return analyzer
def updateDataGame(analyzer, category):
    #Mete al arbol el game segun su fecha de lanzamiento #Req 2
    """
    """
    plataformas= analyzer["Game By Platform"]
    game_id=category["Game_Id"]
    entry = me.getValue(m.get(analyzer["Game by Id"], game_id))
    plataformas=entry["Platforms"].split(", ")
    # Contar registros que hay en cada juego por plataforma, primero obteniendo el juego con base al game ID que tiene el registro, 
    # luego con ese juego se actualiza el mapa que guarda información y contadores del juego por plataforma
    for i in plataformas:
        plataforma=me.getValue(m.get(analyzer["Game By Platform"], i))
        juego_=me.getValue(m.get(plataforma["game_id"], game_id))
        juego=juego_["video"]
        if not "TimeAVG" in juego:
            time0=category["Time_0"]
            time1=category["Time_1"]
            time2=category["Time_2"]
            cont=0
            promedio=0
            if time0!="":
                cont+=1
                promedio+=float(time0)
            if time1!="":
                cont+=1
                promedio+=float(time1)
            if time2!="":
                cont+=1
                promedio+=float(time2)
            juego["TimeAVG"]=promedio/cont
        juego_["registros"]+=1
        
#Carga del Req 4
def addCategoryReq4(analyzer, category): 

    lt.addLast(analyzer["categorias"], category)
    updateCategoryReq4(analyzer, category)

    return analyzer

def updateCategoryReq4(map, category):
    
    jugador = category["Record_Date_0"].split(", ")
    #print(jugador)
    
    for i in jugador:
        if i=="":  
            continue
        else:
            i=(i)
            entry = om.get(map["Game By Record Date"], i)
            if entry is None:
                datentry = newCategoryEntryReq4(category)
                addCategoryIndexReq4(datentry, category)
                om.put(map["Game By Record Date"], i, datentry)
            else:
                datentry = me.getValue(entry)
                addCategoryIndexReq4(datentry, category)

    

def newCategoryEntryReq4(category):
    entry = {"omYear": None}
    entry['omYear'] = om.newMap(omaptype='RBT', comparefunction=compareDates)
    return entry

def addCategoryIndexReq4(datentry, category):
    mapa_ordenado=datentry["omYear"]
    
   # print(category)
    
    fecha = category["Record_Date_0"]
    entry = om.get(mapa_ordenado, fecha)
    if entry is None:
        datentry = lt.newList('SINGLE_LINKED', compareTimes)
        om.put(mapa_ordenado, fecha, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry, category)

#REQ4
def reg_lentos_rango(analyzer, LimiteInferior, LimiteSuperior):

    #print(analyzer["Game By Record Date"])
    
    abrol=analyzer["Game By Record Date"]
    

        

    

def updateCategory(map, category):
    
    jugador = category["Players_0"].split(", ")
    
    for i in jugador:
        if i=="":  
            continue
        else:
            entry = om.get(map["Game By Player"], i)
            if entry is None:
                datentry = newCategoryEntry(category)
                addCategoryIndex(datentry, category)
                om.put(map["Game By Player"], i, datentry)
            else:
                datentry = me.getValue(entry)
                addCategoryIndex(datentry, category)
    

def newCategoryEntry(category):
    entry = {"omYear": None}
    entry['omYear'] = om.newMap(omaptype='RBT', comparefunction=compareDates)
    return entry

def addCategoryIndex(datentry, category):
    mapa_ordenado=datentry["omYear"]
    
    tiempo = category["Time_0"]
    entry = om.get(mapa_ordenado, tiempo)
    if entry is None:
        datentry = lt.newList('SINGLE_LINKED', compareTimes)
        om.put(mapa_ordenado, tiempo, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry, category)

#Carga del Req 3, como me piden registros, uso Category. 
def addCategoryReq3(analyzer, category): 

    updateCategoryReq3(analyzer, category)


def updateCategoryReq3(analyzer, category):# En este requerimiento se quiere conocer los registros con menor duración en un rango dado de intentos de juego. Por lo tanto, se debe ordenar la lista de menor a mayor y luego se debe recorrer la lista hasta que se encuentre el primer registro que cumpla con el rango de intentos de juego.
    jugador = category["Time_0"].split(", ") 
    entry = om.get(analyzer["Game By Runs"], int(category["Num_Runs"])) #Busca la llave en el arbol
    if entry is None:
        datentry = newCategoryEntryReq3(category) #Crea una valor para la llave en el indice por fecha #Req 3
        addCategoryIndexReq3(datentry, category, analyzer)  #Actualizar el valor de la llave #Req 3    
        om.put(analyzer["Game By Runs"], int(category["Num_Runs"]), datentry) #Mete al arbol el game segun su fecha de lanzamiento #Req 3
    else:
        datentry = me.getValue(entry)
        addCategoryIndexReq3(datentry, category, analyzer)

#NOTA: Puede que se me repitan registros de un mismo juego con el mismo registro


def newCategoryEntryReq3(category): #Req 3, se crea un nuevo entry para el arbol
    entry = {"Registros": None} #Se crea un nuevo entry para el arbol
    entry['Registros'] = lt.newList('SINGLE_LINKED') #Se crea una lista para guardar los registros
    return entry


def addCategoryIndexReq3(datentry, category, analyzer): #Req 3, se actualiza el entry
    boolean_var= True #Se crea una variable booleana para saber si el registro ya se encuentra en la lista
    for i in lt.iterator(datentry["Registros"]): #Se recorre la lista de registros
        if category["Game_Id"]==i["Game_Id"]: #Se compara el id del registro con el id de los registros de la lista
            boolean_var=False #Si el registro ya se encuentra en la lista, se cambia el valor de la variable booleana
            break #Si el registro ya se encuentra en la lista, se sale del ciclo
    if boolean_var: #Si el registro no se encuentra en la lista, se agrega
        gameId=category["Game_Id"] 
        juego = me.getValue(m.get(analyzer["Game by Id"], gameId)) #Se busca el juego en el mapa de juegos
        lt.addLast(datentry["Registros"], juego) #Se agrega el registro a la lista de registros

#Carga del Req 5
def addCategoryReq5(analyzer, category): 

    lt.addLast(analyzer["categorias"], category)
    updateCategoryReq5(analyzer, category)

    return analyzer

def updateCategoryReq5(map, category):
    
    jugador = category["Time_0"].split(", ")
    print(jugador)
    
    for i in jugador:
        if i=="":  
            continue
        else:
            i=float(i)
            entry = om.get(map["Game By Time"], i)
            if entry is None:
                datentry = newCategoryEntryReq5(category)
                addCategoryIndexReq5(datentry, category)
                om.put(map["Game By Time"], i, datentry)
            else:
                datentry = me.getValue(entry)
                addCategoryIndexReq5(datentry, category)

    

def newCategoryEntryReq5(category):
    entry = {"omYear": None}
    entry['omYear'] = om.newMap(omaptype='RBT', comparefunction=compareDates)
    return entry

def addCategoryIndexReq5(datentry, category):
    mapa_ordenado=datentry["omYear"]
    
    
    tiempo = category["Time_0"]
    entry = om.get(mapa_ordenado, tiempo)
    if entry is None:
        datentry = lt.newList('SINGLE_LINKED', compareTimes) 
        om.put(mapa_ordenado, tiempo, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry, category)


# carga de req 7 para cálculo de revenue

def addReq7(analyzer):
    tabla_hash=analyzer["Game By Platform"]
    valueset_tabla=m.valueSet(tabla_hash)
    for i in lt.iterator(valueset_tabla):
        juegos=m.valueSet(i["game_id"])
        lista=lt.newList("ARRAY_LIST")
        for j in lt.iterator(juegos):
            StreamRevenue,MarketShare,Time_AVG,total_runs=calcStreamRevenue(j,lt.size(valueset_tabla))
            j["video"]["StreamRevenue"]=round(StreamRevenue,2)
            j["video"]["MarketShare"]=MarketShare
            j["video"]["Time_AVG"]=round(Time_AVG,2)
            j["video"]["total_runs"]=total_runs
            lt.addLast(lista,j)
        lista= ms.sort(lista,sortcmp_req7)
        m.put(tabla_hash,i["platform"],lista)
    
        
            
        

def calcStreamRevenue(juego_,num_registros_plataforma):
    juego=juego_["video"]
    año_lanzamiento= dt.strptime(juego["Release_Date"],"%y-%m-%d").year
    if año_lanzamiento>=2018:
        antiguedad=año_lanzamiento-2017
    elif 1998<año_lanzamiento<2018:
        antiguedad=404.6-((1/5)*año_lanzamiento)
    else:
        antiguedad=5
    popularidad=math.log(int(juego["Total_Runs"]))
    time_avg=juego["TimeAVG"]
    revenue=(popularidad*time_avg)/antiguedad
    market_share=juego_["registros"]/num_registros_plataforma
    stream_revenue=revenue*market_share
    return stream_revenue,market_share,time_avg,juego["Total_Runs"]


# ============================== 
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
def sortcmp_req7(game1,game2):
    if (game1["video"]["StreamRevenue"] > game2["video"]["StreamRevenue"]):
        return True
    return False
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


#REQ2
def Registros_jugador(analyzer,Player_0):
    abrol=m.get(analyzer["Game By Player"],Player_0)
    
    
    
    if abrol is None:
        return None
    else:
        arbol=me.getValue(abrol)
        arbol=arbol["omYear"]
        lista=om.keySet(arbol) #Queda guaradada una lista de listas, la información ya está ordenada
        
        juegos=lt.newList(datastructure='ARRAY_LIST') #Lista vacía donde se van a guardar los juegos
        for i in lt.iterator(lista):
            nodo=m.get(arbol,i)
            valores = me.getValue(nodo)
            valores_orden= ms.sort(valores,compareTimes)
            lt.addLast(juegos,valores_orden)

         #Se ordena la lista de juegos por año    
        if lt.size(juegos) <5:
            final=juegos
        else:
            final=lt.subList(juegos,1,5)
        
        

        return lt.size(juegos),final

#REQ3
def Juegos_runs_intervalo(analyzer,limiteInferior,limiteSuperior):
    abrol=analyzer["Game By Runs"]
    lista=om.values(abrol,limiteInferior,limiteSuperior) #Queda guaradada una lista de listas, la información ya está ordenada
    return lista





#REQ5 
def mejores_tiempos(analyzer, LimiteInferior, LimiteSuperior):
    
    abrol=analyzer["Game By Time"]
    
    
    lista=om.values(abrol,LimiteInferior,LimiteSuperior) #Queda guaradada una lista de listas, la información ya está ordenada
    
    juegos=lt.newList(datastructure='ARRAY_LIST') #Lista vacía donde se van a guardar los juegos
    for i in lt.iterator(lista):

        valores = om.valueSet(i['omYear'])
       
        for j in lt.iterator(valores):
            for x in lt.iterator(j):
                
                lt.addLast(juegos,x)

    juegos= ms.sort(juegos,compareYears5) #Se ordena la lista de juegos por año    
    if lt.size(juegos) <5:
        final=juegos
    else:
        final=lt.subList(juegos,1,5)

    print(lt.size(juegos))
    
    

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

#Req 3 
def compareTimes_0(game1, game2):
    time_game1= game1["Time_0"] # Se obtiene el tiempo del juego 1
    time_game2= game2["Time_0"] # Se obtiene el tiempo del juego 2
    if time_game1 < time_game2: # Se compara el tiempo del juego 1 con el tiempo del juego 2
        return True
    else:
        return False


#Req 5
def compareYears5(game1, game2):
    release_game1= game1["Record_Date_0"] #Se obtiene la fecha de lanzamiento del juego 1
    release_game1= dt.strptime(release_game1, "%Y-%m-%dT%H:%M:%SZ") #Se convierte la fecha de lanzamiento del juego 1 a formato datetime
    
    release_game2= game2["Record_Date_0"] #Se obtiene la fecha de lanzamiento del juego 2
    release_game2= dt.strptime(release_game2, "%Y-%m-%dT%H:%M:%SZ") #Se convierte la fecha de lanzamiento del juego 2 a formato datetime
    

    if release_game1 < release_game2: #Se compara la fecha de lanzamiento del juego 1 con la fecha de lanzamiento del juego 2
        return True
    
    else:
        return False

#Req 7
def top_juegos_rentables(analyzer,plataforma,top):
    hash_=analyzer["Game By Platform"]
    juegos=me.getValue(m.get(hash_,plataforma))
    return lt.subList(juegos,1,top)
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
def compareIds_hash(id1, id2):
    llave=me.getKey(id2)
    if (id1 == llave):
        return 0
    elif id1 > llave:
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

def compareTimes(time_1, time_2):

    if (time_1 == time_2):
        return 0
    elif (time_1 > time_2):
        return 1
    else:
        return -1























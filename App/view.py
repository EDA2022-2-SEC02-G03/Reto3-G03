"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate
from textwrap import wrap


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def tabulateResults(lista):
    """
    Recibe una lista con peliculas y/o series ordenada y tabula los primeros y los ultimos
    3 elementos
    """

    if lt.size(lista) > 6:
        first3 = lt.subList(lista, 1, 3)
        last3 = lt.subList(lista, lt.size(lista) - 2, 3)
        elems = lt.newList("ARRAY_LIST")
        for elem in lt.iterator(first3):
            lt.addLast(elems, elem)
        for elem in lt.iterator(last3):
            lt.addLast(elems, elem)
        elems = elems['elements']
    else:
        
        allelem = lt.subList(lista,1,lt.size(lista))
        
        elems = lt.newList("ARRAY_LIST")
        for elem in lt.iterator(allelem):
            lt.addLast(elems, elem)
        elems = elems['elements']


    newElems = []
    for elem in elems:
        newElem = elem.copy()
        for key in newElem.keys():
            if type(newElem[key]) == list:
                newElem[key] = ', '.join(newElem[key])
            elif type(newElem[key]) == "datetime":
                newElem[key] = "datetime.strftime(newElem[key]", '%Y-%m-%d'
            if type(newElem[key]) == str:
                newElem[key] = '\n'.join(wrap(newElem[key], 16))
        newElems.append(newElem)

    print(tabulate(newElems, headers='keys', tablefmt='fancy_grid'))

    

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cargar información de videojuegos")
    print("3- Consultar 5 videojuegos más recientes de una plataforma")
    print("4- Consultar registros para un videojuego")
    print("5- Consultar registros de menor duración por rango de intentos")
    print("6- Consultar videojuegos de mayor duración por rango de fechas")
    print("7- Consultar registros más recientes por rango de tiempos récord")
    print("8- Graficar histograma de tiempos para un año de publicación")
    print("9- Consultar 5 videojuegos más rentables")
    print("0- Salir")



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1: 
        print("Cargando información de los archivos ....")

        cont = controller.init()
       
    elif int(inputs[0]) == 2:
        print("\nCargando información de videojuegos ....")
        porcentajedatos = input(
            '\nIndique el porcentaje de datos a cargar (small, 5pct, 10pct, 20pct, 30pct, 50pct, 80pct, large): ')
        control = controller.loadData(cont, porcentajedatos) #Carga los datos de los archivos
        juegos=controller.getFirstGames(cont) 
        categorias=controller.getFirstCategory(cont)
        
        
        #print(categorias)
        #print("Videojuegos cargados: " + str(controller.videojuegosSize(cont)))
        #print("Categorias cargadas: " + str(controller.categorySize(cont)))
        #print("Altura del arbol de videojuegos: " + str(controller.indexHeight(cont)))
        #print("Altura del arbol de categorias: " + str(controller.indexHeightCategory(cont)))
        #print("Elementos en el arbol de videojuegos: " + str(controller.indexSize(cont)))
        #print("Elementos en el arbol de categorias: " + str(controller.indexSizeCategory(cont)))
        #print("Tiempo [ms]: ", f"{control[0]:.3f}", "  ||  ",
              #"Memoria [kB]: ", f"{control[1]:.3f}")

    elif int(inputs[0]) == 3: # REQUERIMIENTO 1
        plataforma = input('Ingrese la plataforma: ')
        LimiteInferior = input('Ingrese el limite inferior de la fecha: ')
        LimiteSuperior = input('Ingrese el limite Superior de la fecha: ')
        a,lst = controller.Juegos_plataforma_rango(cont,plataforma,LimiteInferior,LimiteSuperior)
        #print("Los 5 juegos más recientes de la plataforma son: ")
        #print(lst)
        #tabulateResults(lst)


        
    elif int(inputs[0]) == 4: # REQUERIMIENTO 2
        Player_0 = input('Ingrese el jugador: ') 
        a,lst = controller.Registros_jugador(cont, Player_0)
        print(lst)
        tabulateResults(lst)

    elif int(inputs[0]) == 5: # REQUERIMIENTO 3
        LimiteInferiorReq3 = int(input('Ingrese el limite inferior de intentos: '))
        LimiteSuperiorReq3 = int(input('Ingrese el limite Superior de intentos: '))
        lst = controller.Juegos_runs_intervalo(cont,LimiteInferiorReq3,LimiteSuperiorReq3)
        print ("Los registros de menor duración por rango de intentos son: ")
        print(lst)
        tabulateResults(lst)


        pass

    elif int(inputs[0]) == 6: # REQUERIMIENTO 4
        LimiteInferior = (input('Ingrese el limite inferior de Tiempo: '))
        LimiteSuperior = (input('Ingrese el limite Superior de Tiempo: '))
        a,lst = controller.reg_lentos_rango(cont, LimiteInferior, LimiteSuperior)

        print(lst)#a
        tabulateResults(lst)

    elif int(inputs[0]) == 7: # REQUERIMIENTO 5
        LimiteInferior = float(input('Ingrese el limite inferior de Tiempo: '))
        LimiteSuperior = float(input('Ingrese el limite Superior de Tiempo: '))
        a,lst = controller.mejores_tiempos(cont, LimiteInferior, LimiteSuperior)

        print(lst)
        tabulateResults(lst)

    elif int(inputs[0]) == 8: # REQUERIMIENTO 6
        pass

    elif int(inputs[0]) == 9: # REQUERIMIENTO 7
        plataforma = input('Ingrese la plataforma: ')
        top = int(input('Ingrese el top: '))
        req=controller.top_juegos_rentables(cont,plataforma,top)
        tabulate_=[]
        for i in lt.iterator(req):
            juego=i["video"]
            tabulate_.append([juego["Name"],juego["Release_Date"],juego["Platforms"],juego["Genres"],juego["StreamRevenue"],juego["MarketShare"],juego["Time_AVG"],juego["total_runs"]])
        print(tabulate(tabulate_, headers=['Name','Release_Date','Platforms','Genres','StreamRevenue','MarketShare','Time_AVG','total_runs'], tablefmt='fancy_grid',maxcolwidths=[20,20,20,20,20,20,20,20]))



    else:
        sys.exit(0)
sys.exit(0)
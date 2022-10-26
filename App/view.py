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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

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
        control = controller.loadData(cont, porcentajedatos)
        juegos=controller.getFirstGames(cont)
        categorias=controller.getFirstCategory(cont)
        print("Primeros y últimos 3 juegos cargados: ")
        print(juegos)
        print("Primeras y últimas 3 categorias cargadas: ")
        print(categorias)
        print("Videojuegos cargados: " + str(controller.videojuegosSize(cont)))
        print("Categorias cargadas: " + str(controller.categorySize(cont)))
        print("Altura del arbol de videojuegos: " + str(controller.indexHeight(cont)))
        print("Altura del arbol de categorias: " + str(controller.indexHeightCategory(cont)))
        print("Elementos en el arbol de videojuegos: " + str(controller.indexSize(cont)))
        print("Elementos en el arbol de categorias: " + str(controller.indexSizeCategory(cont)))
        print("Tiempo [ms]: ", f"{control[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{control[1]:.3f}")

    elif int(inputs[0]) == 3: # REQUERIMIENTO 1
        pass
    
    elif int(inputs[0]) == 4: # REQUERIMIENTO 2
        pass

    elif int(inputs[0]) == 5: # REQUERIMIENTO 3
        pass

    elif int(inputs[0]) == 6: # REQUERIMIENTO 4
        pass

    elif int(inputs[0]) == 7: # REQUERIMIENTO 5
        pass

    elif int(inputs[0]) == 8: # REQUERIMIENTO 6
        pass

    elif int(inputs[0]) == 9: # REQUERIMIENTO 7
        pass

    else:
        sys.exit(0)
sys.exit(0)

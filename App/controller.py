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
 """

import config as cf
import model
import csv
import sys
from DISClib.ADT import list as lt

csv.field_size_limit(2147483647)

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos
def loadData(analyzer, porcentajedatos):
    
    info = [ "game", "category"]

    for x in info:
        

        if x == "game":
            file = cf.data_dir + x + "_data_utf-8-" + porcentajedatos + ".csv" #ruta archivo en una variable 
            input_file = csv.DictReader(open(file, encoding="utf-8")) #abrir archivo para leer como dict
            for game in input_file:
                model.addVideojuegos(analyzer, game)
           
        if x == "category":
            file= cf.data_dir + x + "_data_urf-8-" + porcentajedatos + ".csv" #ruta archivo en una variable
            input_file = csv.DictReader(open(file, encoding="utf-8")) #abrir archivo para leer como dict
            for category in input_file:
                model.addCategory(analyzer, category)
                model.addCategoryReq5(analyzer, category)
                model.addCategoryReq3(analyzer, category)

    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getFirstGames(analyzer):
    firstgames = model.getFirstGames(analyzer)
    lastgames = model.getLastGames(analyzer)
    return firstgames, lastgames

def getFirstCategory(analyzer):
    firstcategory = model.getFirstCategory(analyzer)
    lastcategory = model.getLastCategory(analyzer)
    return firstcategory, lastcategory

# Requerimiento 1
def Juegos_plataforma_rango(analyzer, plataforma,LimiteInferior,LimiteSuperior):
    return model.Juegos_plataforma_rango(analyzer, plataforma,LimiteInferior,LimiteSuperior)

# Requerimiento 2
def Registros_jugador(analyzer,Player_0):
    return model.Registros_jugador(analyzer,Player_0)

# Requerimiento 3
def Juegos_runs_intervalo(analyzer, LimiteInferiorReq3, LimiteSuperiorReq3):
    return model.Juegos_runs_intervalo(analyzer, LimiteInferiorReq3, LimiteSuperiorReq3)
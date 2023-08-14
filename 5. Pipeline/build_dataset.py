#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import io
import json
import sys





def request_search(site, offset_limit = 1000):
    """Se indica el sitio en el que debe buscar el termino.
    La funcion iterara por default hasta obtener los 1000 resultados que permite descargar la api a partir
    del parametro offset
    """
    
    
    if site in ['MLA', 'MLB', 'MLM']:
        list_results = []
        ##La api devuelve como maximo 1000 resultados (parametro offset) y los muestra de a 50 registros maximo por default
        for num in range(0, offset_limit, 50):
            response = requests.get(f'https://api.mercadolibre.com/sites/{site}/search?q=tv%204k&offset={num}')
            list_results.append(json.loads(response.content.decode('utf-8'))['results'])
    
        return list_results
    else:
        sys.exit('El sitio elegido no es un parametro válido. Se puede elegir MLA, MLB o MLM')




def flatten(list_of_lists):
    """Convierte una lista de listas en 1 sola lista"""
    return [item for sublist in list_of_lists for item in sublist]




def process_data(dataframe):
    """Se provee un dataframe y realiza la limpieza del mismo manteniendo solo
    los productos que son de condicion new, extrayendo la marca de una 
    """
    
    ##Filtra los que son condicion new
    
    dataframe = dataframe[dataframe['condition'] == 'new']
    
    ###Se mantienen las columnas relevantes
    
    dataframe = dataframe[['id', 'condition', 'title', 'price', 'domain_id', 'attributes']]
    
    ###Extrae marca de la columna attributes
    
    dataframe['brand'] = pd.DataFrame.from_records((dataframe['attributes'].apply(pd.Series)[0]))['value_name']
    
    ##Elimina las columnas que ya no son necesarias
    dataframe = dataframe.drop(['condition', 'attributes'], axis=1)
    
    return dataframe



if __name__ == '__main__':
    ##Capturamos el nombre del sitio al correr el script
    sitio = sys.argv[1]
    
    ##Se realiza la descarga usando la api
    respuesta = request_search(sitio)
    
    ##Se aplana la lista de listas para convertirla en dataframe
    df = pd.DataFrame(flatten(respuesta))
    
    ##Se procesa y limpia la tabla obtenida
    df = process_data(df)
    
    ##Se guarda como csv
    df.to_csv('dataset.csv', index=False)


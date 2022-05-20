# H e a d

# Librerías
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import pathlib
from datetime import datetime, timedelta


def run_ecotad(is_local: bool=False):
    # 1. Lectura de datos originales________________________________________________________________________

        # Ruta °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    if is_local: BASE_DIR = pathlib.Path('/Users/efraflores/Desktop/hub/ecobici_bot')
    else: BASE_DIR = pathlib.Path().cwd()

        # Lectura °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    ecodata = pd.read_csv(BASE_DIR.joinpath('data/csv/acum_data.csv')) 
    ecodata_coordenadas = ecodata[['id','location.lat','location.lon']]
    ecodata_coordenadas = ecodata_coordenadas.drop_duplicates(subset=['id'])
    # print(ecodata)

        # formato de fecha y hora correcto °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°


    # ecodata['date'] = ecodata['date'].dt.strftime("%Y-%m-%d")
    # ecodata['date'] =  pd.to_datetime(ecodata['date'], format='%d/%m/%Y')
    # ecodata['time'] = ecodata['time'].dt.strftime("%H:%M:%S")

    # 2. Filtro de Días a tomar _____________________________________________________________________________

    date_max = ecodata['date'].max()
    date_rest = pd.to_datetime(ecodata['date'].max())-timedelta(2)      # Descomentar estas líneas al llevarlo a git #se elige 2 dias atras para evvitar la prosibilidad media de nulos
    date_min = date_rest.strftime("%Y-%m-%d")
    # print(str(date_min),str(date_max))

    dia_in = int(date_min[8:10])
    dia_fin = int(date_max[8:10])
    # print(dia_in,dia_fin)

    ecodata =  ecodata[(ecodata['date'] <= date_max) & (ecodata['date'] >= date_min)]
    # print(ecodata)
    # 3. Creación de variables (month,day,hour) _____________________________________________________________

    ecodata['month'] = ecodata['date'].map(lambda x:int(x[5:7]))
    ecodata['day'] = ecodata['date'].map(lambda x:int(x[8:10]))
    ecodata['hour'] = ecodata['time'].map(lambda x:int(x[0:2]))

    # 4. Filtro de Horas (horario ecobici 5 a 23 hrs) ________________________________________________________

    ecodata =  ecodata[ecodata['hour'] >= 5]
    dia_max = ecodata.day.max()
    hora_max = ecodata[ecodata['day'] == dia_max].hour.max()
    # print(dia_max, hora_max)

    # 5. Pivot de Horas Dias _________________________________________________________________________________

    ecodata_pivot = pd.pivot_table(data=ecodata,values='availability.bikes',aggfunc=np.sum,columns=['hour'],index=['day','id'])
    # print(ecodata_pivot)

        # 5.1. Añadir columnas de hora en caso de error de no venir una hora especifica °°°°°°°°°°°°°°°°°°°°°°°
    columnas_nulas=[]
    if len(ecodata_pivot.columns) < 19:
        valores_esperados = [j for j in range(5,24)]
        for value in valores_esperados :
            if value not in ecodata_pivot.columns:
                columnas_nulas.append(value) 
                ecodata_pivot.insert(0,value,ecodata_pivot.mean(axis=1))
            
        ecodata_pivot = ecodata_pivot[valores_esperados]
        # print(ecodata_pivot)
        # print(columnas_nulas)



    # 6. Transformación de dataframe __________________________________________________________________________

        # 6.1. Estructura de cada cicloestacion °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

    # 1.  Estructurar cada cicloestacion 
        # 1.1 funcion que tranforma el dataframe a transpuesto correcto
        # Aqui se crea el primer dataframe que consiste en transponer los valores por hora a columna, sin perder el día y hora adecuado

    def auxiliarTransponer(df:pd.DataFrame,cicloestacion:int,dia:int)->pd.DataFrame:
        prueba1 = df.reset_index()
        prueba1 = prueba1[prueba1['id'] == cicloestacion]
        prueba1 = prueba1[prueba1['day'] < dia+1]
        prueba1 = prueba1[prueba1['day'] > dia-1]
        prueba1 = prueba1.reset_index(drop=True)
        prueba1 = pd.melt(prueba1,id_vars=['day','id'],value_vars=list(prueba1.columns[2:])).drop(columns='hour')
        prueba1['hour'] = [i for i in range(5,24)]
        return prueba1

        # 1.2 La siguiente funcion nos ayuda a estructurar los datos, solo es necesario aplicarlo a cada cicloestacion
        # Con esta concatenamos un dataframe abajo de otro(dia a dia), esta funcion debe ser aplicada a cada cicloestacion
        
    def concatDataPerStation(data:pd.DataFrame,dia_in:int,dia_fin:int,cicloestacion:int)->pd.DataFrame:
        auxiliarTransponer(data,cicloestacion,dia_in)
        j=1
        for i in range(dia_in,dia_fin+1):
            if j == 1:
                df = auxiliarTransponer(data,cicloestacion,i)
                j=j+1
            else:
                df1 = auxiliarTransponer(data,cicloestacion,i)
                df = pd.concat([df, df1], ignore_index=True)
        
        return df

    # Ahora aplicamos la funcion a cada cicloestacion, y generamos un dataframe estructurado para cada cicloestacion

    allDataFrames_structured_stations = {}
    for i in range(1,481):
        no_stations = [88, 101, 193, 440] #lista de cicloestaciones totalmente apagadas, que no deben ser contadas
        if i not in no_stations:
            allDataFrames_structured_stations[f"df_station_structured_{i}"] =  concatDataPerStation(ecodata_pivot,dia_in,dia_fin,i)
        else:
            continue


        
        # 6.2. Tratamiento de nulos por estación °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

    # Nulos en la variable 'day'

    # Lo siguiente nos dara los días en los que hay nulos en ciertas cicloestaciones

    # Esto significa que ciertas cicloestaciones solo en un cierto día fueron apagadas por lo cual se eliminará directamente esas filas
    for i in range(1,481):
        no_stations = [88, 101, 193, 440]
        if i not in no_stations:
            df_actual = allDataFrames_structured_stations[f'df_station_structured_{i}']
            nulos_dia_valor = df_actual.isnull().sum().values[0] # 0 es la variable dia
            nulos_dia_index = df_actual.isnull().sum().index[0]
            if nulos_dia_valor != 0:
                # print(i,nulos_dia_index,nulos_dia_valor)
                allDataFrames_structured_stations[f'df_station_structured_{i}'] = allDataFrames_structured_stations[f'df_station_structured_{i}'].dropna(subset=['day'])
                # en la linea de arriba se eliminan esas filas nulas (nota: no son imputables)


    # Los siguientes códigos se deben de aplicar por ciclo estacion para imputar los nulos de la variable 'value'
    for i in range(1,481):
        no_stations = [88, 101, 193, 440]
        if i not in no_stations:
            df_actual = allDataFrames_structured_stations[f'df_station_structured_{i}']
            # frame de indices donde se encuentran los nan, por estacion
            df_nan_rows = df_actual.loc[pd.isna(df_actual["value"]), :]
            # frame de las medias por hora (en los dias tomados) por estacion
            df_means_per_station = df_actual.groupby(['hour']).mean().reset_index() #medias a nivel columna
            # lista con diccionarios hora:media por estacion
            lista_hora_medias_dict = [{df_means_per_station['hour'][i]:int(df_means_per_station['value'][i])} for i in df_means_per_station.index if (df_means_per_station['hour'][i] in list(df_nan_rows['hour'].values))]

            # codigo donde sustituye los valores nulos con la media correspondiente por hora y cicloestacion
            for index in df_nan_rows.index:
                for j in range(0,len(lista_hora_medias_dict)):
                    if df_nan_rows['hour'][index] == list(lista_hora_medias_dict[j].keys())[0]:
                        df_actual['value'][index] = lista_hora_medias_dict[j][df_nan_rows['hour'][index]]

        # 6.3. Aplicar shift por estacion °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

    # Primero  haremos una copia de los dataframes para poder modificar sin ningun problema

    # Copia de cada allDataFrames_structured_stations
    all_shifted_structured_stations = allDataFrames_structured_stations

    # Ahora editamos esas copias a la forma multi shift (nos dara 476 nuevos frames)
    for i in range(1,481):
        no_stations = [88, 101, 193, 440] 
        if i not in no_stations:
            for j in range(1, 20):
                shifted_data_station = all_shifted_structured_stations[f"df_station_structured_{i}"]
                shifted_data_station[f"{'value'}(t-{j})"] = shifted_data_station['value'].shift(j)
            all_shifted_structured_stations[f"df_station_structured_{i}"] = shifted_data_station.dropna()

        # 6.4. Concat all_shifted_treated_structed_dataframes °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

    def concatAllFrames(dict:dict,cicloestacion_ini:int,cicloestacion_fin:int):
        j=1 
        for i in range(cicloestacion_ini,cicloestacion_fin+1):
            no_stations = [88, 101, 193, 440]
            if i not in no_stations:
                if j == 1:
                    df_stations = dict[f'df_station_structured_{i}']
                    j=j+1
                else:
                    df_stations_2 = dict[f'df_station_structured_{i}']
                    df_stations = pd.concat([df_stations,df_stations_2],ignore_index=True) # logica 1+2 -> 1+2+3 -> 1+2+3

        return df_stations


    df_allStations_shifted_structured = concatAllFrames(all_shifted_structured_stations,1,480)

    # 7. Filtro MAX __________________________________________________________________________________


    df_allStations_shifted_structured = df_allStations_shifted_structured[df_allStations_shifted_structured['day'] == dia_max]
    df_allStations_shifted_structured = df_allStations_shifted_structured[df_allStations_shifted_structured['hour'] == hora_max]

    # 8. Guardar TAD ___________________________________________________________________________________

    tad =  df_allStations_shifted_structured

    tad.to_pickle(pathlib.Path().joinpath(BASE_DIR,'data/tad/tad_for_prediction.pkl')) #sustituir por ruta git*

    # 9. Guardamos frame de coordenadas que nos ayudara despues a map _____________________________________________________________________

    ecodata_coordenadas.to_pickle(pathlib.Path().joinpath(BASE_DIR,'data/for_map/coordinates_frame_for_map.pkl')) #sustituir por ruta git*

    # print(tad.head())

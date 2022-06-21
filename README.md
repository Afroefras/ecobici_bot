[![Ecobici bot](https://github.com/Afroefras/ecobici_bot/actions/workflows/run_getmap.yml/badge.svg)](https://github.com/Afroefras/ecobici_bot/actions/workflows/run_getmap.yml)

# ecobici_bot
Sigue a [@EcobiciMapBot](https://twitter.com/EcobiciMapBot) en Twitter para mostrar disponibilidad de estaciones Ecobici cada 30min 🚴🏽‍♂️
 
 
 <br>


![Alt text](media/map/map.png?raw=true "Ecobici Map")


<br>

### Estructura del repositorio:
    .
    ├── .github/workflows
    │   └── run_getmap.yml            # Crea una MV, obtiene credenciales desde Secrets, corre el script cada 30min y hace el commit -> push
    │
    ├── data
    │   └── csv
    │   │   └── acum_data.csv         # Datos acumulados de los últimos N días, se usan para modelo de pronóstico
    │   │   └── coordinates.csv       # Coordenadas de cada estación Ecobici, para el mapa de predicción
    │   │   └── df_for_map.csv        # Predicción de bicicletas disponibles para cada estación
    │   └── model
    │   │   └── model.xz              # Diccionario con modelo y objetos para escalar
    │   │   └── tad_for_pred.xz       # Función para re-estrucutar nuevos datos como el modelo lo necesita
    │   └── shp
    │       └── ...                   # Archivos necesarios para desplegar los límites por Código Postal en CDMX
    │
    ├── media
    │   └── map
    │       └── future_map.png        # Imagen del mapa de disponibilidad dentro de una hora, utiliza los datos actuales para predecir
    │       └── map.png               # Imagen del mapa de disponibilidad, se actualiza automáticamente cada 30min
    │
    ├── scripts
    │   ├── __init__.py               # Para que el directorio se trabaje de forma modular
    │   ├── map.py                    # Clase con métodos como importar datos desde API, creación de variables, reestructuración de datos, etc
    │   └── run_getmap.py             # Llama a la clase de "map.py" y las credenciales desde GitHub Secrets para correr el proceso
    │
    └── requirements.txt              # Instalar las librerías necesarias con el comando: pip install -r requirements.txt
    
    

<br>

## Work In Progress..

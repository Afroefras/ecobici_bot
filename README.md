[![Ecobici bot](https://github.com/Afroefras/ecobici_bot/actions/workflows/run_getmap.yml/badge.svg)](https://github.com/Afroefras/ecobici_bot/actions/workflows/run_getmap.yml)


# Ecobici Twitter bot 🚴🏾‍♀️🚴🏾‍♂️
Sigue a [@EcobiciMapBot](https://twitter.com/EcobiciMapBot) en Twitter para mostrar disponibilidad de estaciones Ecobici CDMX cada 30min

Lo mejor es que muestra la disponibilidad para la siguiente hora, así que seguramente alcanzas tu Ecobici 😉

<br>

Colaboración con [@DiegoFores](https://github.com/DiegoFores). Gracias, hermanito!
Orientación de [@fferegrino](https://github.com/fferegrino/) a través de un [gran artículo](https://feregri.no/lambda-tweet-parte-1-github-aws-twitter/) (uno de muchos) para crear [@CyclesLondon](https://twitter.com/CyclesLondon) un Twitter bot que actualiza la disponibilidad de la Red de Bicicletas en Londres.
 
 
 <br>

Mapa actual            |  Mapa para la siguiente hora
:-------------------------:|:-------------------------:
![](media/map/map.png?raw=true "Ecobici Map")  |  ![](media/map/future_map.png?raw=true "Ecobici Future Map")

*Actualizado al momento, cada 30min que corre el script automáticamente


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
    │   ├── ecoPredict.py             # Recibe los datos transformados desde ecoTad.py para aplicar el modelo de predicción
    │   ├── ecoTad.py                 # Re-estructura los datos tal que el modelo prediga la demanda futura
    │   ├── map.py                    # Clase con métodos como importar datos desde API, creación de variables, reestructuración de datos, etc
    │   └── run_getmap.py             # Llama a la clase de "map.py" y las credenciales desde GitHub Secrets para correr el proceso
    │
    └── requirements.txt              # Instalar las librerías necesarias con el comando: pip install -r requirements.txt

<br>


## Consulta desde la API de Ecobici CDMX

1. Es muy fácil hacer uso de la API, el primer paso es registrarte [aquí](https://www.ecobici.cdmx.gob.mx/es/informacion-del-servicio/open-data) para recibir por correo tus credenciales: 

CLIENT_ID y CLIENT_SECRET (guárdalas muy bien, donde nadie las encuentre) 
([este](https://canovasjm.netlify.app/2021/01/12/github-secrets-from-python-and-r/) artículo me ayudó mucho a entender GitHub Secrets, para guardar y usar credenciales donde ni siquiera tú las consultes)

2. Es posible consultar la información desde tu explorador entrando al siguiente link (con tus credenciales)
`https://pubsbapi-latam.smartbike.com/oauth/v2/token?client_id={CLIENT_ID}&client_secret={CLIE
NT_SECRET}&grant_type=client_credentials`


## Work In Progress..

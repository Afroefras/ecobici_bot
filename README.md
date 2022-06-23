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


2. Instanciar la clase para obtener los datos al momento
```python
from map import EcoBiciMap

ebm = EcoBiciMap(CLIENT_ID, CLIENT_SECRET)

# Con las credenciales se inicia la sesión y se obtiene el token de acceso
ebm.get_token(first_time=True)
```


3. Información respecto a las estaciones, incluyendo coordenadas
```python
ebm.get_data()
```
|id|name|address|addressNumber|zipCode|districtCode|districtName|altitude|nearbyStations|stationType|location.lat|location.lon|
|---|---|---|---|---|---|---|---|
|55|55 5 DE MAYO-BOLIVAR|055 - 5 de Mayo - Bolívar|S/N|6700|1|Ampliación Granada|None|[65, 87]|BIKE,TPV|19.434356|-99.138064|
|124|124 CLAUDIO BERNARD-DR. LICEAGA|124 - Claudio Bernard-Dr. Liceaga|S/N|6500|1|Ampliación Granada|None|[119, 123, 133]|BIKE|19.422392|-99.150358|
|159|159 HUATABAMPO-EJE 1 PTE. AV. CUAUHTÉMOC|159 - Huatabampo-Eje 1 Pte. Av. Cuauhtémoc|S/N|6760|1|Ampliación Granada|None|[155, 158, 163]|BIKE|19.407517|-99.155373|
|241|E241 EJERCITO NAL-JUAN VAZQUEZ DE LA MELLA|241 - Ejercito Nacional-Juan Vazquez de la Mella|S/N|11520|1|Ampliación Granada|None|[222, 460]|ELECTRIC_BIKE|19.43862|-99.20758|
|243|243 MIGUEL DE CERVANTES SAAVEDRA-LAGO FILT|243 - Miguel de Cervantes Saavedra-Lago Filt|S/N|11510|1|Ampliación Granada|None|[199, 242, 244]|BIKE|19.440839|-99.196712|




## Work In Progress..

# Control de datos
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from json import loads as loads_json
from requests import get as get_request

# Ingeniería de variables
from pandas import json_normalize
from geopandas import read_file

# Gráficas
from seaborn import scatterplot
from matplotlib.lines import Line2D
from matplotlib.pyplot import Axes, Figure, get_cmap


class EcoBiciMap:
    def __init__(self, client_id: str, client_secret: str) -> None:
        # Obtiene el directorio actual
        self.base_dir = Path().cwd()
        # Dominio web base, de donde se anexarán rutas y parámetros
        self.base_url = "https://pubsbapi-latam.smartbike.com"
        # Ruta con las credenciales de acceso
        self.user_credentials = f"oauth/v2/token?client_id={client_id}&client_secret={client_secret}"
    

    def get_token(self, first_time: bool=False) -> None:
        # URL completa para recibir el token de acceso y el token de actualización (se ocupa si la sesión dura más de 60min)
        if first_time: URL = f"{self.base_url}/{self.user_credentials}&grant_type=client_credentials"
        # En el caso que se accese por 2a ocasión o más, se llama al token de actualización
        else: URL = f"{self.base_url}/{self.user_credentials}&grant_type=refresh_token&refresh_token={self.REFRESH_TOKEN}"

        # Obtiene la respuesta a la solicitud de la URL
        req_text = get_request(URL).text
        # Lee el formato json para guardar los tokens
        data = loads_json(req_text)

        # Guarda los tokens
        self.ACCESS_TOKEN = data['access_token']
        self.REFRESH_TOKEN = data['refresh_token']


    def get_data(self, availability: bool=False) -> None:
        # URL para obtener la información en tiempo real, ya sea la info de las estaciones y/o la disponibilidad de las mismas
        stations_url = f"{self.base_url}/api/v1/stations{'/status' if availability else ''}.json?access_token={self.ACCESS_TOKEN}"
        req_text = get_request(stations_url).text
        data = loads_json(req_text)

        # El json resultado tiene la data encapsulada en la primer llave
        first_key = list(data.keys())[0]
        # Se estructura como tabla 
        df = json_normalize(data[first_key])
        return df


    def get_shapefile(self, shapefile_url: str='https://datos.cdmx.gob.mx/dataset/7abff432-81a0-4956-8691-0865e2722423/resource/8ee17d1b-2d65-4f23-873e-fefc9e418977/download/cp_cdmx.zip') -> None:
        req_data = get_request(shapefile_url).content
        zip_file = ZipFile(BytesIO(req_data))
        shapefile_dir = self.base_dir.joinpath('data','shp')
        zip_file.extractall(shapefile_dir)
        self.gdf = read_file(shapefile_dir).to_crs(epsg=4326)


    def transform(self, station_cols: list=['id','zipCode','location.lat','location.lon'], id_col: str='id', status_col: str='status', bikes_col: str='availability.bikes', slots_col: str='availability.slots') -> None:
        self.df = self.st[station_cols].merge(self.av, on=id_col)
        self.df = self.df[self.df[status_col]=='OPN'].copy()
        self.df['slots_proportion'] = self.df[slots_col] / (self.df[slots_col] + self.df[bikes_col])
        self.df['bikes_proportion'] = 1 - self.df['slots_proportion']


    def set_custom_legend(self, ax, cmap, values: list) -> None:
        legend_elements = []
        for gradient, label in values:
            color = cmap(gradient)
            legend_elements.append(Line2D([0], [0], marker="o", color="w", label=label, markerfacecolor=color, markeredgewidth=0.5, markeredgecolor="k"))
        ax.legend(handles=legend_elements, loc="lower right", prop={"size": 6}, ncol=len(values))


    def plot_map(self, lat_col: str='location.lat', lon_col: str='location.lon', padding: float=0.007, points_palette: str='mako', **kwargs) -> None:
        fig = Figure(figsize=(5, 4), dpi=200, frameon=False)
        ax = Axes(fig, [0.0, 0.0, 1.0, 1.0])
        fig.add_axes(ax)
        ax.set_axis_off()
        ax.set_ylim((self.df[lat_col].min() - padding, self.df[lat_col].max() + padding))
        ax.set_xlim((self.df[lon_col].min() - padding, self.df[lon_col].max() + padding))

        self.gdf.plot(ax=ax, linewidth=0.5, **kwargs)

        cmap = get_cmap(points_palette)
        scatterplot(y=lat_col, x=lon_col, hue='slots_proportion', data=self.df, ax=ax, palette=cmap)

        self.set_custom_legend(ax, cmap, values=[(0.0, 'Hay bicis'), (0.5, 'Puede haber'), (1.0, 'No hay bicis')])
        fig.savefig(self.base_dir.joinpath('media','map','map.png'))


    def get_map(self, **kwargs) -> None:
        self.get_token(first_time=True)
        self.st = self.get_data()
        self.av = self.get_data(availability=True)
        self.get_shapefile()
        self.transform()
        now = datetime.now().strftime(r"%Y-%m-%dT%H_%M")
        self.plot_map(**kwargs)
        self.df.to_csv(self.base_dir.joinpath('data', 'csv', f'data_{now}.csv'), index=False)



### CHECAR FUNCIÓN PARA CREAR TWEET
   
# import os
# from datetime import datetime

# from twython import Twython


# def tweet(image_path: str) -> None:

#     app_key = os.environ["API_KEY"]
#     app_secret = os.environ["API_SECRET"]
#     oauth_token = os.environ["ACCESS_TOKEN"]
#     oauth_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
#     twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

#     now = datetime.now().strftime("%m/%d/%Y, %H:%M")

#     with open(image_path, "rb") as cycles_png:
#         image = twitter.upload_media(media=cycles_png)

#     twitter.update_status(status=f"London Cycles update at {now}", media_ids=[image["media_id"]])
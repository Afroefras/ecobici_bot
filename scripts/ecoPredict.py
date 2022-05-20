# dependencies ___________________________________________________________________________________________________________________________________________________________
from operator import index
import pandas as pd
import pathlib
import pickle

# import data_____________________________________________________________________________________________________________________________________________________________

BASE_DIR = pathlib.Path().cwd() #sustituir por ruta git*
# BASE_DIR = pathlib.Path('/Users/efraflores/Desktop/hub/ecobici_bot')

df_prueba = pd.read_pickle(BASE_DIR.joinpath('data/tad/tad_for_prediction.pkl')) # debe ser el nombre correcto en Git para el dir y el pkl
df_coordenadas = pd.read_pickle(BASE_DIR.joinpath('data/for_map/coordinates_frame_for_map.pkl')) #sustituir por ruta git*

# import model_____________________________________________________________________________________________________________________________________________________________

filename = BASE_DIR.joinpath('data/model/model_hour.xz')
loaded_model = pickle.load(open(filename, 'rb'))

filename_scaler = BASE_DIR.joinpath('data/model/scaler.pkl')
scaler_model = pickle.load(open(filename_scaler, 'rb'))

filename_scaler_y = BASE_DIR.joinpath('data/model/scaler_y.pkl')
scaler_model_y = pickle.load(open(filename_scaler_y, 'rb'))

# prediction  _____________________________________________________________________________________________________________________________________________________________

X_validation = df_prueba.iloc[:,:-1].set_index(['day','id'])
X_validation.drop(columns=['hour'],inplace=True)
variables_t = X_validation.columns
Xs = pd.DataFrame(scaler_model.transform(X_validation),columns=variables_t)
#Xs['prediction'] =
result = loaded_model.predict(Xs)

# dataframe of prediction __________________________________________________________________________________________________________________________________________________

df_prediction = pd.DataFrame(scaler_model_y.inverse_transform(result.reshape(-1,1)).astype(int))
print(df_prediction)

# dataframe for map (id,prediction,coordinates)_____________________________________________________________________________________________________________________________

df_for_map = X_validation.reset_index()
df_for_map['prediction'] = df_prediction
df_for_map = df_for_map[['id','prediction']]
df_for_map = df_for_map.merge(df_coordenadas, on='id', how='left')
# df_for_map['bikes_proportion'] = 
print(df_for_map)

# export dataframe for map _________________________________________________________________________________________________________________________________________________

# df_for_map.to_pickle(BASE_DIR.joinpath('data/for_map/df_for_map.xz')) #sustituir por ruta git*
df_for_map.to_csv(BASE_DIR.joinpath('data/for_map/df_for_map.csv'), index=False) #sustituir por ruta git*

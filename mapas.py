import geopandas as gpd
from pymongo import MongoClient
from math import radians, sin, cos, asin, sqrt

from shapely.wkt import loads as wkt_loads, dumps
from shapely.geometry import Point, Polygon, mapping
import geojson
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, Point
from matplotlib.patches import Polygon as PolygonPatch
import io
import os


def connect_to_mongodb():
    username = "insomnesoul"
    password = "hHR4c1WmJO37GlEA"
    client = MongoClient(f'mongodb+srv://{username}:{password}@realstatecolombia.hhtn5cb.mongodb.net')
    db = client['Adicionales']
    return db



shp_path = 'C://Users//neylp//OneDrive//Escritorio//LineMeUp//transporte//sector.shp.03.24'

# Lectura archivos SHP y geojson (SHP se lee la carpeta) -> se debe hacer con docker la descarga
gdf_barrios = gpd.read_file(shp_path)
gdf_localidades=gpd.read_file("C://Users//neylp//OneDrive//Escritorio//LineMeUp//transporte//poligonos-localidades.geojson")
gdf_sitp=gpd.read_file("C://Users//neylp//OneDrive//Escritorio//LineMeUp//transporte//psitp")
gdf_trasmi=gpd.read_file("C://Users//neylp//OneDrive//Escritorio//LineMeUp//transporte//Estaciones_Troncales_de_TRANSMILENIO.geojson")

gdf=gdf_barrios


db = connect_to_mongodb()

gdf_barrios['SCANOMBRE'] = gdf_barrios['SCANOMBRE'].apply(lambda x: x.lower())
poligonos = gdf_barrios["geometry"]
gdf_barrios["centroid"] = poligonos.apply(lambda x: x.centroid)
gdf_barrios["centroid_x"] = gdf_barrios["centroid"].apply(lambda p: p.x)
gdf_barrios["centroid_y"] = gdf_barrios["centroid"].apply(lambda p: p.y)
df_copy=gdf_barrios.copy()
df_copy['geometry'] = df_copy['geometry'].astype(str)
primeras_palabras = df_copy['geometry'].str.split('(').str[0]
filtro = df_copy['geometry'].str.contains("multipolygon", case=False)
result=df_copy[filtro]
res=result['geometry'].to_dict()
valores_unicos = primeras_palabras.unique()


data_dict = gdf_barrios.to_dict(orient='records')

for item in data_dict:
    # Convertir el punto a un diccionario de coordenadas
    centroid_coords = str(item['centroid']).replace('POINT (', '').replace(')', '').split()
    centroid = {
        "centroid": {
            "type": "Point",
            "coordinates": [float(centroid_coords[0]), float(centroid_coords[1])]
        }
    }

    # Convertir el polígono a un diccionario de coordenadas
    polygon_str = dumps(item['geometry'])
    indice = polygon_str.find("mundo")

    # Verificar si se encontró la subcadena
    if indice != -1:
            multipolygon_str = dumps(item['geometry'])
            multipolygon_coords = multipolygon_str.replace('MULTIPOLYGON ((((', '').replace('))))', '').split('), ((')
            multipolygon_coords = [[list(map(float, coord.split())) for coord in polygon.split(', ')] for polygon in multipolygon_coords]
            multipolygon = {
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": multipolygon_coords
                }
            }
    else:
        polygon_coords = polygon_str.replace('POLYGON', '').replace('MULTI', '').replace('(', '').replace(')', '').split(', ')
        polygon_coords = [list(map(float, coord.split())) for coord in polygon_coords]
        polygon = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon_coords]
            }
        }

    # Actualizar el diccionario con los nuevos valores
    item.update(centroid)
    item.update(polygon)

print(data_dict)


#collection_name = 'barrios'
#collection = db[collection_name]
#collection.insert_many(data_dict)

"""
estaciones_por_localidad = {}
for i,localida in enumerate(gdf_localidades["geometry"]):
    lista_aux=[]
    for j,point in enumerate(gdf_sitp["geometry"]):
        if point.intersects(localida):
            lista_aux.append(gdf_sitp.loc[j,"cenefa"])
    estaciones_por_localidad[gdf_localidades.loc[i,"Nombre de la localidad"]]=lista_aux

#collection_name = 'localidad_sitp'
#collection = db[collection_name]
#collection.insert_one(estaciones_por_localidad)


estaciones_por_barrio = {}
for i,barrio in enumerate(gdf_barrios["geometry"]):
    lista_aux=[]
    for j,point in enumerate(gdf_sitp["geometry"]):
        if point.intersects(barrio):
            lista_aux.append(gdf_sitp.loc[j,"cenefa"])
    estaciones_por_barrio[gdf_barrios.loc[i,'SCANOMBRE']]=lista_aux
print(estaciones_por_barrio)

# Nombre de la colección
#collection_name = 'barrio_sitp'
#collection = db[collection_name]
#collection.insert_one(estaciones_por_barrio)


pip_localidades = gdf_sitp.within(gdf_localidades.loc[0, 'geometry'])
gdf_sitps_transformed = gdf_sitp.loc[pip_localidades].copy()
gdf_sitps_transformed['Localidad'] = gdf_localidades["Nombre de la localidad"][0]

pip_barrios = gdf_sitp.within(gdf_barrios.loc[0, 'geometry'])
gdf_sitps_transformed.loc[pip_barrios, 'Barrio'] = gdf_barrios["SCANOMBRE"][0]
dict_sitp_con_loco = gdf_sitps_transformed.to_dict(orient='records')

#collection_name = 'localidad_sitp'
#collection = db[collection_name]
#collection.insert_one(estaciones_por_localidad)

print(gdf_sitps_transformed.head(),"\n", gdf_sitps_transformed.columns)


pip_localidades = gdf_trasmi.within(gdf_localidades.loc[0, 'geometry'])
gdf_sitps_transformed = gdf_trasmi.loc[pip_localidades].copy()
gdf_sitps_transformed['Localidad'] = gdf_localidades["Nombre de la localidad"][0]



trasmi_por_localidad = {}
for i,localidad in enumerate(gdf_localidades["geometry"]):
    lista_aux=[]
    for j,point in enumerate(gdf_trasmi["geometry"]):
        if point.intersects(localidad):
            lista_aux.append(gdf_trasmi.loc[j,"nombre_estacion"])
    trasmi_por_localidad[gdf_localidades.loc[i,'Nombre de la localidad']]=lista_aux
#print(estaciones_por_barrio)

# Nombre de la colección
collection_name = 'trasmi_localidad'
collection = db[collection_name]
collection.insert_one(trasmi_por_localidad)
"""

"""
trasmi_por_barrio= {}
for i,localidad in enumerate(gdf_localidades["geometry"]):
    lista_aux=[]
    for j,point in enumerate(gdf_trasmi["geometry"]):
        if point.intersects(localidad):
            lista_aux.append(gdf_trasmi.loc[j,"nombre_estacion"])
    trasmi_por_barrio[gdf_localidades.loc[i,'SCANOMBRE']]=lista_aux
print(trasmi_por_barrio)

collection_name = 'localidad_trasmi'
collection = db[collection_name]
collection.insert_one(trasmi_localidad)
"""
# Crear un diccionario para almacenar los puntos por localidad

"""


# Assuming your DataFrames are named gdf_localidades and gdf_trasmi
def calculate_nearest_distance(multipolygon, point):
  
  Calculates the distance from a point to the nearest point on a multipolygon.
  
  # Convert geometries to shapely objects for easier calculations
  multipolygon_geom = polygon.to_shape(ndim=2)
  point_geom = point.to_shape(ndim=2)

  nearest_point = polygon_geom.exterior.project(point_geom)

  # Calculate the distance using the Haversine formula (assuming spherical Earth)
  lon1, lat1 = radians(point.x), radians(point.y)
  lon2, lat2 = radians(nearest_point[0]), radians(nearest_point[1])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a))
  r = 6371  # Earth's radius in kilometers (or use 3956 for miles)
  distance = c * r
  return distance

# Add a new column named "nearest_distance" to gdf_trasmi
gdf_trasmi["nearest_distance"] = gdf_trasmi.apply(lambda row: 
                                                  calculate_nearest_distance(gdf_localidades.geometry[0], row.geometry), axis=1)
"""
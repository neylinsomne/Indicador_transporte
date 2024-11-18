from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
import pandas as pd
import geopandas as gpd

shp_path = 'C://Users//neylp//OneDrive//Escritorio//LineUp//transporte//sector.shp.03.24'
gdf_barrios = gpd.read_file(shp_path)

shp_path = 'C://Users//neylp//OneDrive//Escritorio//LineUp//transporte//sector.shp.03.24'
gdf_barrios = gpd.read_file(shp_path)
# Configura la conexión a tu base de datos PostgreSQL

# Convierte las geometrías a WKTElements
gdf_barrios['geometry'] = gdf_barrios['geometry'].apply(lambda geom: WKTElement(geom.wkt, srid=4326))

# Guarda el GeoDataFrame en la base de datos
gdf_barrios.to_sql('base2024', con=db, if_exists='replace', index=False, dtype={'geometry': Geometry('GEOMETRY', srid=4326)})

import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from pymongo import MongoClient
from mapas import data_dict

client = MongoClient('mongodb+srv://insomnesoul:hHR4c1WmJO37GlEA@realstatecolombia.hhtn5cb.mongodb.net/')
#df = pd.read_csv('C:\Users\neylp\Downloads\archive (4)\data\processed/apartments.csv')
db=client['Adicionales']
collection = db['barrios']
documentos = collection.find()


print(data_dict)
def plotmongo():
# Crear figuras de matplotlib
    fig, ax = plt.subplots()

    # Plotear los polígonos y los centroides
    for documento in documentos:
        # Crear polígono
        polygon_coords = documento['geometry']['coordinates'][0]
        polygon = Polygon(polygon_coords)
        poly_patch = plt.Polygon(polygon.exterior.coords, edgecolor='black', facecolor='none')
        ax.add_patch(poly_patch)

        # Crear centroide
        centroid_coords = documento['centroid']['coordinates']
        centroid = Point(centroid_coords)
        ax.plot(centroid.x, centroid.y, 'ro')

    # Configurar el aspecto del gráfico
    ax.axis('equal')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Mapa de polígonos y centroides')

    # Mostrar el gráfico
    plt.show()
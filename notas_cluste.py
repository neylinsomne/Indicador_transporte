from sklearn.cluster import DBSCAN
import numpy as np

# Seleccionar la columna y convertirla en un array de una dimensión
X = xd[["Troncales_cant",'Trasmi_dist_menor_estandarizada']]

# Aplicar DBSCAN
#el 10 al
clust= DBSCAN(eps=1.2, min_samples=6)
db=clust.fit(X)
labels = db.labels_

from sklearn import metrics

#identifying the points which makes up our core points
sample_cores=np.zeros_like(labels,dtype=bool)

sample_cores[clust.core_sample_indices_]=True

#Calculating the number of clusters

n_clusters=len(set(labels))- (1 if -1 in labels else 0)
no_noise = np.sum(np.array(labels) == -1, axis=0)


print(metrics.silhouette_score(X,labels))

print('Estimated no. of clusters: %d' % n_clusters)
print('Estimated no. of noise points: %d' % no_noise)


import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
colors = ['#3b4cc0', '#b40426']  # Puedes agregar más colores si necesitas más clusters
plt.scatter(X["Troncales_cant"], X["Trasmi_dist_menor"],  marker="o", picker=True)
plt.title('Two clusters with data')
plt.xlabel('Troncales_cant')
plt.ylabel('Trasmi_dist_menor')
plt.show()


X['Cluster'] = labels

# Asignar etiquetas específicas para los puntos ruidosos
X.loc[X['Cluster'] == -1, 'Cluster'] = 'Noise'

# Asignar etiquetas para los puntos que pertenecen a clusters
for i in range(n_clusters):
    X.loc[X['Cluster'] == i, 'Cluster'] = 'Cluster#' + str(i + 1)

# Mostrar el DataFrame actualizado
print(X)





import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
colors = ['#3b4cc0', '#b40426']  # Puedes agregar más colores si necesitas más clusters


plt.scatter(X["Troncales_cant"], X["Trasmi_dist_menor"],  marker="o", picker=True)
plt.title('Two clusters with data')
plt.xlabel('Troncales_cant')
plt.ylabel('Trasmi_dist_menor')
plt.show()






X['Cluster'] = labels

# Asignar etiquetas específicas para los puntos ruidosos
X.loc[X['Cluster'] == -1, 'Cluster'] = 'Noise'

# Asignar etiquetas para los puntos que pertenecen a clusters
for i in range(n_clusters):
    X.loc[X['Cluster'] == i, 'Cluster'] = 'Cluster#' + str(i + 1)

# Mostrar el DataFrame actualizado
print(X)
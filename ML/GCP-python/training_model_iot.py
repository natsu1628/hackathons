from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import numpy as np

data = []
data1 = []

def dataset():
	'''
	with open("dataset1.csv","r") as file:
		reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			data.append(row)
	'''
	with open("total_dataset.csv","r") as file:
		reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			data1.append(row)
	#data = np.array(data1)
	#print(data)

def distance_severity():

	data = np.array(data1)		#convert to array using numpy
	#print(data)
	model = KMeans(n_clusters=3)
	model.fit(data)
	all_predictions = model.predict(data)
	centroids = model.cluster_centers_
	print("\n\nCentroids: ")
	print(centroids)		#type of centroids is <class 'numpy.ndarray'>

	distance_severity_values = centroids[:, 0].tolist()	#converting to list using numpy
	#print(distance_severity_values)
	distance_severity_values.sort()	#sort in ascending order
	#distance_severity_values.sort(reverse = True)	#sort in descending order
	print(distance_severity_values)
	#write to a table to store the threshold values according to the descending or ascending order in 3 columns
	

	#plot 3d figure of dataset
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	#label = {0: 'red', 1:'blue', 2:'green'}#
	x_axis = data[:, 0]
	y_axis = data[:, 1]
	z_axis = data[:, 2]
	
	ax.scatter(x_axis, y_axis, z_axis, c = 'g', marker='o')
	ax.set_xlabel('Distance')
	ax.set_ylabel('Vehicle type')
	ax.set_zlabel('Traffic condition')
	
	plt.show()

	label = {0: 'red', 1:'blue', 2:'green'}
	#x_axis = data[:, 0]
	#y_axis = data[:, 2]
	#plt.scatter(x_axis, y_axis)
	#plt.show()

	num_elements = len(x_axis)
	zpos = np.zeros(num_elements)
	dx = np.ones(num_elements)
	dy = np.ones(num_elements)
	dz = z_axis
	ax1 = fig.add_subplot(111, projection='3d')
	#ax1.bar3d(x_axis, y_axis, zpos, dx, dy, dz, color='#00ceaa')
	#plt.show()


if __name__ == '__main__':
	dataset()
	distance_severity()

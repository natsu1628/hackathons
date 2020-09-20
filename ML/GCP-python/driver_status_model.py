from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import numpy as np

def plot_data(data):
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

def read_dataset(filename):
	data = []
	with open(filename,"r") as file:
		reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			data.append(row)
	data = np.array(data)		#convert to array using numpy
	return data

def model_set():
	data = read_dataset("total_dataset.csv")
	model = KMeans(n_clusters = 3)
	model.fit(data)
	threshold = model.cluster_centers_		#type of centroids is <class 'numpy.ndarray'>
	#print("Threshold: " + threshold)

	threshold_values = threshold[:, 0].tolist()		#converting to list using numpy
	threshold_values.sort()		#threshold distance values in ascending order
	print("Sorted Threshold values: " + str(threshold_values))

	#plot dataset points of all 10,000 points
	#plot_data(data)
	return threshold_values
	#return model

'''
if __name__ == '__main__':
	model_set()
'''

import random
import csv
import numpy as np

file_name = []

def dataset_read(filename):
	data = []
	with open(filename,"r") as file:
		reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			data.append(row)
	data = np.array(data)
	return data

def filename_generate():
	file = ["device"+str(i) for i in range(1,11)]
	global file_name
	file_name = file
	
def dataset_generate(filename):
	filename = filename+".csv"
	with open(filename,"w", newline='') as file:
		for i in range(1000):
			#distance = round(random.uniform(0,1001),2)
			distance = random.randrange(0,1001)
			vehicle_type = random.randrange(0,10)
			traffic_type = random.randrange(0,10)
			writer = csv.writer(file, quoting = csv.QUOTE_NONNUMERIC)
			writer.writerows([[distance, vehicle_type, traffic_type]]) # ex: [[109.87,4,2]]
	print("Dataset of {} created...".format(filename[:-4]))
	#print(dataset_read(filename))

def dataset():
	#print(file_name)
	for i in range(10):
		filename = file_name[i]
		dataset_generate(filename)

if __name__ == '__main__':
    filename_generate()
    dataset()
'''
[[21.32,2,4], [12.56,2,3], ...., [11.43,1,2]]

'''

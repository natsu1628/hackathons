import driver_status_model as driver

def median_distance(data, driver_threshold):
	data_size = len(data)
	data_size_use = int(0.75*data_size)
	data.sort()
	data = data[:data_size_use]
	#print(data)
	median_dist = [round(x - driver_threshold, 2) for x in data]
	if data_size % 2 == 0:
		mid = data_size_use//2
		median_val = (median_dist[mid-1] + median_dist[mid])/2
	else:
		mid = (data_size_use + 1)//2
		median_val = median_dist[mid]
	#print("Median value: " + str(median_val))
	return median_val

def status():
	driver_threshold_all = driver.model_set()		#get the threshold value of distance from driver_status_model
	driver_threshold = round(driver_threshold_all[0],2)		#minimum threshold value for the high risk status
	print("High Risk Threshold: " + str(driver_threshold))
	data = driver.read_dataset("device9.csv")		#read dataset of device

	#if you change driver_status_model to return model instead of the threshold value, use the below commented part
	'''
	model = driver.model_set()
	print(model.cluster_centers_)
	threshold = model.cluster_centers_
	print(threshold)
	threshold_values = threshold[:, 0].tolist()		#converting to list using numpy
	threshold_values.sort()		#threshold distance values in ascending order
	driver_threshold = threshold_values[0]
	print(driver_threshold)

	#predict
	all_predictions = model.predict(data)
	#print(all_predictions)
	'''

	#getting the distance_ahead of each device
	data_dist = data[:, 0].tolist()
	#calculating the median distance_ahead from 750 bottom category points
	median_value = median_distance(data_dist, driver_threshold)
	print("Median value: " + str(median_value))
	#predict risk
	risk_prediction = sum([1 if d <= driver_threshold else 0 for d in data_dist])
	print("Dataset size: " + str(len(data)))
	#calculate risk status of driver. 5% is the risk limit
	min_risk_value = int(0.05*(len(data))) + 80		#added 80 for test purpose
	print("Predicted Risk value: " + str(risk_prediction))
	print("Maximum Risk value: " + str(min_risk_value))
	if risk_prediction >= min_risk_value:
		print("Driver's driving status is at high risk. Appropriate measures need to be taken by the driver to drive safe.")
	else:
		print("Driver is driving safely.")

	#show the plot of dataset of a particular device
	#driver.plot_data(data)
	
	#return driver_threshold_all

if __name__ == '__main__':
	status()

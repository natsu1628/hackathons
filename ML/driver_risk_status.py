import base64
import json
import urllib.request
from google.cloud import bigquery
from google.oauth2 import service_account
import random
import requests
from google.cloud import automl_v1beta1
from google.protobuf.json_format import MessageToJson
import time
import driver_status as d_status

# Distance details from KMeans algo
prev_time = int(time.time())
low_risk_d = 500
medium_risk_d = 300
high_risk_d = 100

#Project details
project_id = '<gcp_project_id>'
model_id = '<model_id>'
client = bigquery.Client(project_id)
job_config = bigquery.QueryJobConfig()
job_config1 = bigquery.QueryJobConfig()

#Integer representation of vehicles
vehicle_rep = {"car": 0, "truck": 1}

# Function to check the image:
def get_prediction(content):
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = '<gcp_project_name>'
    payload = {'image': {'image_bytes': content }}
    params = {}
    #result = json.loads(MessageToJson(prediction_client.predict(name, payload, params)))
    result = json.loads(MessageToJson(prediction_client.predict(name, payload, params), preserving_proto_field_name = True))
    vehicle = result['payload'][0]['display_name']
    return vehicle_rep[vehicle]
    #return request  # waits till request is returned


# Function to check vehicle & traffic severity:
def check_severity(a, b):
    return a + (a*b)

# Function to check traffic status:
def check_traffic(lat, long, time):
    lat_start = lat[0]
    lat_end = lat[1]+0.32
    long_start = long[0]
    long_end = long[1]+0.12
    time_start = time[0]
    time_end = time[1]
    
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="\
          + str(lat_start) + "," + str(long_start) + "&destinations=" + str(lat_end) + "," \
          + str(long_end) + "&key=" + API_KEY											    #insert your Google API_KEY in the API_KEY placeholder
    
    req = requests.get(url)
    response = json.loads(req.text)
    
    google_dis = (response["rows"][0]["elements"][0]["distance"]["value"])
    google_time = (response["rows"][0]["elements"][0]["duration"]["value"])
    
    driver_time = time_end - time_start
    
    driver_speed = google_dis/driver_time
    
    if(driver_speed > 0):
        time_per_km = 1000/driver_speed
        if time_per_km < 180:
            return 2
        elif time_per_km > 180 and time_per_km < 420:
            return 1
        elif time_per_km > 420:
            return 0
    else:
        return 1


def insert_query(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_message = json.loads(pubsub_message)
    print(pubsub_message)
    
    
    ser_no = pubsub_message['ser_no']
    device_id = pubsub_message['device_id']
    timestamp = pubsub_message['timestamp']
    gps_loc_lat = pubsub_message['gps_loc_lat']
    gps_loc_long = pubsub_message['gps_loc_long']
    distance_ahead = pubsub_message['distance_ahead']
    vehicle_img_url = pubsub_message['vehicle_img_url']
    
    vehicle_type = None
    with urllib.request.urlopen(vehicle_img_url) as url:
        content = url.read()
        #print(get_prediction(content))
        vehicle_type = get_prediction(content)
        print("vehicle Representation: " + str(vehicle_type))
        
    #veh_list = [0,1]
    #vehicle_type = random.choice(veh_list)
    
    check_query = ''' SELECT `gps_loc_lat`, `gps_loc_long`, `timestamp` FROM `IOT_DEMO.Demo_Test` WHERE `timestamp` < @time AND `timestamp` >= @time - 120 AND `device_id` = @device
    					LIMIT 2'''
    query_params = [
        bigquery.ScalarQueryParameter('time', 'INT64', timestamp),
        bigquery.ScalarQueryParameter('device', 'STRING', device_id)
    ]
    
    job_config.query_parameters = query_params
    query_job = client.query(check_query, location='<location>', job_config=job_config)
    rows = query_job.result()
    
    lat=[]
    long=[]
    time=[]
    
    for row in rows:
        lat.append(row.gps_loc_lat)
        long.append(row.gps_loc_long)
        time.append(row.timestamp)
        
    #print(lat)
    #print(long)
    #print(time)
    
    if(len(lat) == 2 and len(long) == 2):
        traffic_status = check_traffic(lat, long, time)
    else:
        traffic_status = 1
        
    # Check distance severity(0 being the lowest and 3 being the highest)
    if distance_ahead > low_risk_d:
        distance_severity = 0
    elif distance_ahead > medium_risk_d:
        distance_severity = 1
    elif distance_ahead > high_risk_d:
        distance_severity = 2
    else:
        distance_severity = 3
    
    vehicle_severity = check_severity(distance_severity, vehicle_type)
    
    traffic_severity = check_severity(vehicle_severity, traffic_status)
    
    insert_query = '''INSERT INTO `IOT_DEMO.Demo_Test` (`ser_no`,`device_id`, `timestamp`, `gps_loc_lat`, `gps_loc_long`, `distance_ahead`,`vehicle_img_url`,`disntance_severity`,
										   `vehicle_type`, `vehicle_severity`, `traffic_status`, `traffice_severity`) VALUES
                                          (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    #Insert Query Parameters
    query_params1 = [
        bigquery.ScalarQueryParameter(None, 'INT64', ser_no),
        bigquery.ScalarQueryParameter(None, 'STRING', device_id),
        bigquery.ScalarQueryParameter(None, 'INT64', timestamp),
        bigquery.ScalarQueryParameter(None, 'FLOAT64', gps_loc_lat),
        bigquery.ScalarQueryParameter(None, 'FLOAT64', gps_loc_long),
        bigquery.ScalarQueryParameter(None, 'INT64', distance_ahead),
        bigquery.ScalarQueryParameter(None, 'STRING', vehicle_img_url),
        bigquery.ScalarQueryParameter(None, 'INT64', distance_severity),
        bigquery.ScalarQueryParameter(None, 'INT64', vehicle_type),
		bigquery.ScalarQueryParameter(None, 'INT64', vehicle_severity),
        bigquery.ScalarQueryParameter(None, 'INT64', traffic_status),
		bigquery.ScalarQueryParameter(None, 'INT64', traffic_severity)
    ]
    
    job_config1.query_parameters = query_params1
    
    print(insert_query)
    query_job1 = client.query(insert_query, location='<location>', job_config=job_config1)
    print("Check1")
    query_job1.result()
    print("query inserted")

def main(event, context):
    cur_time = int(time.time())
    global prev_time
    global low_risk_d
    global medium_risk_d
    global high_risk_d
    if (cur_time - prev_time) > (24*3600):
        print("Current time: " + str(cur_time) + "\tPrevious time: " + str(prev_time))
        print("Time difference greater than 24 hours!")
        dist_threshold = d_status.status()        #get the three distance threshold values from driver_status.py
        high_risk_d = int(dist_threshold[0])
        medium_risk_d = int(dist_threshold[1])
        low_risk_d = int(dist_threshold[2])
        prev_time = cur_time
    else:
        print("Current time: " + str(cur_time) + "\tPrevious time: " + str(prev_time))
        print("Time difference less than 24 hours!")
    insert_query(event, context)    #call the function to insert into bigquery

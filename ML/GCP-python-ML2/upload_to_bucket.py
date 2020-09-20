import pandas
from google.cloud import storage
from google.oauth2 import service_account
#import cloudstorage as gcs
#from google.cloud import storage as gcs
#import gcs_client as gcs

project_id = "<gcp_project_id>"

credentials = service_account.Credentials.from_service_account_file("<gcp_service_account_file_path>")

class Load:
	def __init__(self):
		pass

	def put_to_bucket(self, bucket_name):
		storage_client = storage.Client(project=project_id, credentials=credentials)
		bucket = storage_client.bucket(bucket_name)
		#creating bucket if it does not exist
		'''
		if(not bucket.exists()):
			bucket = storage_client.create_bucket(bucket_name)
			print("Bucket: {} created".format(bucket.name))
		else:
			print("Bucket: {} already exists".format(bucket.name))
		'''
		err = 1
		try:
			blob = bucket.blob('input/input.jpg')
			blob.upload_from_filename('15.jpg')
			print("Metric data is uploaded to bucket {}".format(bucket_name+"input/input.jpg"))
			err = 0
		except Exception as ex:
			print("Error during upload into Bucket. \n{}".format(ex))

		return err



if __name__ == '__main__':
	bu = Load()
	bu.put_to_bucket("<bucket_name>")

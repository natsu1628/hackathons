from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from google.protobuf.json_format import MessageToDict
from google.oauth2 import service_account
from google.cloud import storage
import gcs_client

# credentials = gcs_client.Credentials("<gcp service account file path>")
credentials = service_account.Credentials.from_service_account_file("<gcp service account file path>")

def get_prediction(content):
	project_id = "<project_id>"
	model_id = "<model_id>"
	prediction_client = automl_v1beta1.PredictionServiceClient(credentials=credentials)
	name = '<project_name>'
	payload = {'image': {'image_bytes': content }}
	params = {}
	result = MessageToDict(prediction_client.predict(name, payload, params), preserving_proto_field_name = True)
	print("Result: {} type: {}".format(result, type(result)))
	print(payload)
	prediction = result["payload"][0]["classification"]
	return prediction

def main():
	client = storage.Client(project='<gcp_project_id>', credentials=credentials)
	print("before get_bucket")
	bucket = client.get_bucket('<bucket_name>')
	blob = bucket.get_blob("input/input.jpg")
	image = blob.download_as_string()
	print(type(image))
	prediction = get_prediction(image)
	if prediction == "accident":
		blob_acc = bucket.blob("accident/acc1.jpg")
		blob_acc.upload_from_string(image, content_type='image/jpeg')
		print("Uploaded to `accident` directory in bucket `<bucket_name>`")
	else:
		blob_no_acc = bucket.blob("no_accident/no_acc1.jpg")
		blob_no_acc.upload_from_string(image, content_type='image/jpeg')
		print("Uploaded to `no_accident` directory in bucket `<bucket_name>`")

if __name__ == '__main__':
	main()

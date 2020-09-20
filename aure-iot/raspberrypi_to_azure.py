# raspberry pi camera code
# pip install picamera
# or run the following commands in raspberry pi command line
# sudo apt-get update
# sudo apt-get install python-picamera python3-picamera

from picamera import PiCamera
from time import sleep

img_file_nm = 'img.jpeg'
camera = PiCamera()
camera.start_preview()
sleep(2)
camera.capture(img_file_nm)
camera.stop_preview()



# upload an image captured from raspberry pi into Azure storage

from azure.storage.blob import BlobServiceClient, BlobClient

# the connection string to your storage account.
connect_str = '<azure_connect_str>'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = '<storage_container>'    # name of storage container in Azure storage

# list down all blobs in the container to determine the next image name
container_client = blob_service_client.get_container_client(container_name)
blob_list = container_client.list_blobs()
blob_name_list = []
for blob in blob_list:
    blob_name_list.append(blob.name.rsplit('.', 1)[0])
blob_name_list_sorted = sorted(blob_name_list)

# number to be attached after 'img' denoting the number of image
num = blob_name_list_sorted[-1][3:]
if len(num) > 0:
	new_num = int(num) + 1
else:
	new_num = 1
blob_file_name = 'img' + str(new_num) + ".jpeg"

# Create a blob client
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file_name)

print("Uploading {} to Azure storage as: {}".format(img_file_nm, blob_file_name))

# Upload the image file
with open(img_file_nm, "rb") as img:
    blob_client.upload_blob(img)

print("Upload to Azure Storage completed!!")

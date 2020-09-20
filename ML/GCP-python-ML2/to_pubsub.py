import time
import base64
from google.cloud import pubsub_v1
from google.oauth2 import service_account

project_id = "<gcp_project_id>"
topic_name = "<topic_name>"

credentials = service_account.Credentials.from_service_account_file("<gcp_Service_account_file_path>")
print(credentials)

publisher = pubsub_v1.PublisherClient(credentials = credentials)

topic_path = publisher.topic_path(project_id, topic_name)

def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    print("1")
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print(message_future.result())


with open("15.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
#print(str)

data = "sample data"
# Data must be a bytestring
data = data.encode('utf-8')
# When you publish a message, the client returns a Future.
message_future = publisher.publish(topic_path, data=str)
message_future.add_done_callback(callback)
print(data)
print('Published message IDs:')

##############################################################################################


subscriber = pubsub_v1.SubscriberClient(credentials = credentials)
subscription_path = subscriber.subscription_path(
    project_id, "subscribe")

def callback1(message):
    print('Received message: {}'.format(message))
    message.ack()

subscriber.subscribe(subscription_path, callback=callback1)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))

while True:
    time.sleep(60)

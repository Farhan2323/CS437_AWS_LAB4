# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np
import os

# TODO 1: modify the following parameters
# Starting and end index, modify this
device_st = 1
device_end = 6  # To include devices 1-5

# Path to the dataset, modify this (not used in this updated version)
data_path = "data/vehicle{}.csv"

# Path to your certificates, modify this
cert_directory = "iot-certs/"
certificate_formatter = cert_directory + "RaspberryPi_{}.cert.pem"
key_formatter = cert_directory + "RaspberryPi_{}.private.key"

class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        
        # TODO 2: modify your broker address
        # Replace with your endpoint from AWS IoT Core settings
        self.client.configureEndpoint("athd1uvswb1ik-ats.iot.us-east-1.amazonaws.com", 8883)
        
        # Configure credentials
        self.client.configureCredentials(
            cert_directory + "AmazonRootCA1.pem",  # Make sure this file exists
            key, 
            cert
        )
        
        # Configure MQTT client settings
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec





        def on_message(client, userdata, message):
        self.client.onMessage = on_message} received payload: {message.payload.decode()} from topic: {message.topic}")
        
    # Callback for when a subscription is acknowledged
    def customSubackCallback(self, mid, data):
        print(f"Device {self.device_id} subscription confirmed")
    
    # Callback for when a publish is acknowledged
    def customPubackCallback(self, mid):
        print(f"Device {self.device_id} publish confirmed")
    
    # Putry:h a message
    def pub # Generate dummy data since we don't have CSV files
            payload = json.dumps({
                'device_id': self.device_id,
                'timestamp': int(time.time()),
                'data': {
                    'speed': 60 + int(self.device_id) * 5,
                    'rpm': 1200 + int(self.device_id) * 100,
            })      'fuel_level': 75 - int(self.device_id) * 5
                }
            self.client.publishAsync(topic, payload, 0, ackCallback=self.customPubackCallback)
                t(f"Device {self.device_id} publishing data to {topic}")
        except Exception as e:
            print(f"Error publishing for device {self.device_id}: {e}")

# Initialize clients
print("Initializing MQTTClients...")
clients = []

for device_id in range(device_st, device_end):
    # Format the certificate and key paths correctly
    cert_path = certificate_formatter.format(device_id)
    key_path = key_formatter.format(device_id)
    
    print(f"Connecting device {device_id} with cert: {cert_path}")
    
    # Create and connect the client
    client = MQTTClient(device_id, cert_path, key_path)
    
    try:
        client.client.connect()
        print(f"Device {device_id} connected successfully")
        
        # Subscribe to the same topic
        topic = f"vehicle/emission/data"
        client.client.subscribe(topic, 1, client.customSubackCallback)
        print(f"Device {device_id} subscribed to {topic}")
                clients.append(client)
    except Exception as e:
        print(f"Failed to connect device {device_id}: {e}")

print(f"Successfully connected {len(clients)} devices")

# Main interaction loop
while True:
    print("\nOptions:")
    print("s - Send one message from each device")
    print("d - Disconnect all devices and exit")
    
    x = input("Enter command: ")
    
    if x == "s":
        print("Sending messages from all devices...")
        for i, c in enumerate(clients):
            c.publish()
        print("Messages sent!")

    elif x == "d":
        print("Disconnecting all devices...")
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("Wrong key pressed. Use 's' to send or 'd' to disconnect.")

    time.sleep(1)

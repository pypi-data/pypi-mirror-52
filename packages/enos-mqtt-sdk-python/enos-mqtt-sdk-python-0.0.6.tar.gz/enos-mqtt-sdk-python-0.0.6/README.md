# Using EnOS Device SDK for MQTT for Python (Preview Edition)

This repo contains the preview edition of EnOS Device SDK for MQTT for Python. This article instructs how to prepare your development environment to use the EnOS Device SDK for MQTT for Python.

* [Installing Python](#python)
* [Obtaining EnOS Device SDK for MQTT for Python](#obtaining)
* [Key Features](#keyfeatures)
* [Sample Code](#samplecode)

<a name="python"></a>
## Installing Python
To use the EnOS Device SDK for MQTT for Python, you will need Python 2.7.13+ or 3.5.3+, and `pip` is required.

<a name="obtaining"></a>
## Obtaining EnOS Device SDK for MQTT for Python
You can obtain the SDK through the following methods:

- Install from pip
- Download the source code by cloning this repo and build on your machine

### Installing from PIP

Use the following command to install EnOS Device SDK for MQTT for Python from PIP.

```bash 
pip install enos-mqtt-sdk-python
```

### Building from Source Code
1. Obtain the EnOS Device SDK for MQTT for Python source code.
   - From GitHub:
    ```
    git clone https://github.com/EnvisionIot/enos-mqtt-sdk-python.git
    ```
   - From EnOS SDK Center. Click **SDK Center** from the left navigation of EnOS Console, and obtain the SDK source code.

2. From the directory where the source code is stored, run the following command:

   ```
   python setup.py install
   ```
<a name="keyfeatures"></a>
## Key Features

As the preview edition, the EnOS Device SDK for MQTT for Python currently contains only partial of the EnOS connection features as listed below:

- MQTT over TCP based on username and password and MQTT over TLS 1.2 with X.509 certificate-based mutual authentication supported
- Create, read, update and delete (CRUD) gateway device topology
- Publish measure point data

<a name="samplecode"></a>
## Sample Code

### Preparation (Cloud Configuration and Certificate Generation)
1. Create device models (including gateway and sub-device), products, devices, and applications in the EnOS Console, and get the corresponding product key-secret and device key-secret pair. For more information, see [Cloud Configuration](https://docs.envisioniot.com/docs/device-connection/en/latest/cloud/index.html) in EnOS Documentation Center.

2. Get the CA root certificate, and generate the local RSA private key and csr file, and apply a certificate from EnOS via the EnOS cert tool (available in EnOS SDK Center).

3. Update the CA root certificate.
    - Enter python shell, input the codes and run:
    ```python
    >>>import certifi
    >>>certifi.where()
    ```
    And then one path will be printed on the console, copy it.
    - Quit the python shell, enter the directory where the CA file in step.2 was generated.
    - Run the following command:
    ```
    cat edge_ca.pem {the path generated in previous step} > all_ca.pem
    ```
    We will use the all_ca.pem in the next steps.
### Establishing Connection

1. Initialize the MQTT client and load the certificate files.
  ```python
  client = MqttClient(enos_mqtt_url, gateway_product_key, gateway_device_key, gateway_device_secret)
  client.getProfile().setSSLContext(ca_file, cer_file, key_file, key_file_password)
  client.getProfile().setAutoReconnect(True)       # if connection interrupted, the client can automaticlly reconnect
  ```

2. Set the online and offline callback method.
  ```python
  client.onOnline = onOnline
  client.onOffline = onOffine
  client.onConnectFailed = onConnectFailed
  ```

3. Connect in synchronous mode.
  ```python
  client.connect()
  ```
  
### Register a handle_msg to handle the downstream received measurepoint
  ```python
  client.onMessage(handle_msg)
  ```

### Sending Telemetries
1. Add topology for the sub-devices
  ```python
  topo_req = TopoAddRequest.builder().addSubDevice(SubDeviceInfo(sub_product_key, sub_device_key, sub_device_secret)).build()
  topo_res = client.publish(topo_req)
  ```

2. Login the sub-devices
  ```python
  login_req = SubDeviceLoginRequest.builder().setSubDeviceInfo(sub_product_key, sub_device_key, sub_device_secret).build()
  login_res = client.publish(login_req)
  ```

3. Send telemetries from the MQTT client
  ```python
  meapt_req = MeasurepointPostRequest.builder() \
          .setProductKey(sub_product_key).setDeviceKey(sub_device_key) \
          .addMeasurePoint('MeasurePoint1', value1) \      # the measure point identity
          .addMeasurePoint('MeasurePoint2', value2) \
          .setTimestamp(timestamp) \
          .build()
  meapt_res = client.publish(meapt_req)
  ```

### End-to-End Sample

```python
from core.MqttClient import MqttClient
from message.downstream.ota.OtaUpgradeCommand import OtaUpgradeCommand
from message.upstream.status.SubDeviceLoginRequest import SubDeviceLoginRequest
from message.upstream.topo.TopoAddRequest import TopoAddRequest
from message.upstream.topo.SubDeviceInfo import SubDeviceInfo
from message.upstream.ota.OtaVersionReportRequest import OtaVersionReportRequest
from message.upstream.ota.OtaProgressReportRequest import OtaProgressReportRequest
from message.upstream.topo.TopoGetRequest import TopoGetRequest
from message.upstream.topo.TopoDeleteRequest import TopoDeleteRequest
from message.downstream.tsl.MeasurepointSetCommand import MeasurepointSetCommand
from message.upstream.tsl.MeasurepointPostRequest import MeasurepointPostRequest
import random
import time

# mqtt broker url
enos_mqtt_url = "tcp://{HOST}:11883" # for tcp connection
# enos_mqtt_url = "ssl://{HOST}:18883" # for ssl connection

# gateway parameters
gateway_product_key = "GATEWAY_PRODUCT_KEY"
gateway_product_secret = 'GATEWAY_PRODUCT_SECRET'
gateway_device_key = "GATEWAY_DEVICE_KEY"
gateway_device_secret = "GATEWAY_DEVICE_SECRET"

# sub-device parameters
sub_product_key = 'SUB_PRODUCT_KEY'
sub_device_key = "SUB_DEVICE_KEY"
sub_device_secret = "SUB_DEVICE_SECRET"

# these file are generated by get_cert.py via EnOS cert tool, for tls connection
ca_file = 'edge_ca.pem'
key_file = 'edge.key'
cer_file = 'edge.pem'
key_file_password = 'PRIVATE_KEY_PASSWORD'


def onConnectFailed():
	print('connect failed...')
	time.sleep(10)
	client.connect()

def onOnline():
	login_sub_device(client)                          # login the sub-device if exists sub-device
	print('connected...')

def onOffine():
	print('disconnected...')

def get_topo(mqtt_client):
	topo_get_req = TopoGetRequest.builder().build()
	topo_get_res = mqtt_client.publish(topo_get_req)
	if topo_get_res:
		print('topo_response: code: %s' % topo_get_res.getCode())
		print(topo_get_res.getData())


def add_topo(mqtt_client):
	topo_req = TopoAddRequest.builder().addSubDevice(SubDeviceInfo(sub_product_key, sub_device_key, sub_device_secret)).build()
	topo_res = mqtt_client.publish(topo_req)
	if topo_res:
		print('topo_response: code: %s' % topo_res.getCode())
		print('topo_response: message: %s' % topo_res.getMessage())


def delete_topo(mqtt_client):
	topo_del_req = TopoDeleteRequest.builder().addSubDevice(sub_product_key, sub_device_key).build()
	topo_del_res = mqtt_client.publish(topo_del_req)
	if topo_del_res:
		print('topo_delete_response: %s' % topo_del_res.getCode())


def login_sub_device(mqtt_client):
	login_req = SubDeviceLoginRequest.builder().setSubDeviceInfo(sub_product_key, sub_device_key, sub_device_secret).build()
	login_res = mqtt_client.publish(login_req)
	if login_res:
		print('login_response: code: %s' % login_res.getCode())
		print('login_response: message: %s' % login_res.getMessage())


# post measure points data via MQTT
def post_measure_points(mqtt_client, timestamp):
	meapt_req = MeasurepointPostRequest.builder() \
		.setProductKey(sub_product_key).setDeviceKey(sub_device_key) \
		.addMeasurePoint('MeasurePoint1', random.randint(100, 200)) \
		.addMeasurePoint('MeasurePoint2', random.randint(100, 200)) \
		.setTimestamp(timestamp) \
		.build()
	meapt_res = mqtt_client.publish(meapt_req)
	if meapt_res:
		print('measurepointPost_response: %s' % meapt_res.getCode())

# handle the received downstream message and implement your logic
def handle_msg(arrivedMessage, replyHandler):
	'''
	:param arrivedMessage: <attributes:deviceKey,prodectKey,id,messageTopic,method,params,version>
	:param replyHandler: <method:replyWithPayload>
	'''
	# handle logic
	success = 1
	print(arrivedMessage.params)
	# set reply payload
	if success:
		code = 200
		message = 'test'
		data = 0
	else:
		code = 2000
		message = 'test'
		data = 1
	replyHandler.reply_with_payload(code=code, message=message, data=data)

def report_version(mqtt_client, version):
	meapt_req = OtaVersionReportRequest.builder() \
		.setProductKey(gateway_product_key).setDeviceKey(gateway_device_key) \
		.setVersion(version) \
		.build()
	meapt_res = mqtt_client.publish(meapt_req)
	if meapt_res:
		print('OtaVersionReport_response: %s' % meapt_res.getCode())

def report_progress(mqtt_client, progress, desc):
	meapt_req = OtaProgressReportRequest.builder() \
		.setProductKey(gateway_product_key).setDeviceKey(gateway_device_key) \
		.setStep(progress) \
		.setDesc(desc) \
		.build()
	meapt_res = mqtt_client.publish(meapt_req)
	if meapt_res:
		print('OtaProgressReport_response: %s' % meapt_res.getCode())

def upgrade_firmware(arrivedMessage, replyHandler):
	OtaUpgradeCommand = arrivedMessage
	firmware = OtaUpgradeCommand.getFirmwareInfo()
	print("receive command: ", firmware.fileUrl, firmware.version)

	# TODO: download firmware from firmware.fileUrl

	# mock reporting progress
	report_progress(client, '35', 'downloading firmware finished')

	report_progress(client, '70', 'decompressing firmware finished')

	report_progress(client, '90', 'running firmware finished')

	report_progress(client, '100', 'upgrading firmware finished')

	# firmware upgrade success, report new version
	report_version(client, firmware.version)

if __name__ == "__main__":

	client = MqttClient(enos_mqtt_url, gateway_product_key, gateway_device_key, gateway_device_secret)
	client.getProfile().setAutoReconnect(True)       # if connection interrupted, the client can automaticlly reconnect
	# set the certificate files for bi-directional certification
	client.getProfile().setSSLContext(ca_file, cer_file, key_file, key_file_password)
	client.setupBasicLogger('INFO')
	client.onOnline = onOnline
	client.onOffline = onOffine
	client.onConnectFailed = onConnectFailed

	client.connect()                                 # connect in sync

	# register a handle_msg to handle the downstream received measurepoint
	client.onMessage(MeasurepointSetCommand().getClass(), handle_msg)
	# register a handle_msg to implement the ota function, e.g: upgrade firmware
	client.onMessage(OtaUpgradeCommand().getClass(), upgrade_firmware)
	add_topo(client)                                 # add the device to the gateway as sub-device if exists sub-device
	report_version(client, '1.0.0')                  # report the version number before upgrading firmware
	while True:
		timestamp = int(time.time() * 1000)          # timestamp in milliseconds
		post_measure_points(client, timestamp)       # publish measure points data
		time.sleep(10)

```


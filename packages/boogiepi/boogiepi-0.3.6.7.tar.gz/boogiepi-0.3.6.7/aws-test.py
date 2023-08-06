# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def do_cpu_temp(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# For certificate based connection
#myMQTTClient = AWSIoTMQTTClient("Odroid")
# For Websocket connection
myMQTTClient = AWSIoTMQTTClient("Odroid", useWebsocket=True)
# Configurations
# For TLS mutual authentication
#myMQTTClient.configureEndpoint("aw2j4vtnh9bs8-ats.iot.us-east-2.amazonaws.com", 8883)
# For Websocket
myMQTTClient.configureEndpoint(
    "aw2j4vtnh9bs8-ats.iot.us-east-2.amazonaws.com", 443)
# For TLS mutual authentication with TLS ALPN extension
#myMQTTClient.configureEndpoint("aw2j4vtnh9bs8-ats.iot.us-east-2.amazonaws.com", 443)
#myMQTTClient.configureCredentials("/home/pi/.aws/credentials/AmazonRootCA1.pem", "/home/pi/.aws/credentials/6c6823e552-private.pem.key", "/home/pi/.aws/credentials/6c6823e552-certificate.pem.crt")
# For Websocket, we only need to configure the root CA
myMQTTClient.configureCredentials("/home/pi/.aws/AmazonRootCA1.pem")
# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(20)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
while True:
    myMQTTClient.connect()
    myMQTTClient.publish("myCPUtemp", "0C", 0)
    myMQTTClient.subscribe("myCPUtemp", 1, do_cpu_temp)
    myMQTTClient.unsubscribe("myCPUtemp")
    myMQTTClient.disconnect()
    time.sleep(3)

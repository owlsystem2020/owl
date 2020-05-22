#!/usr/bin/env python3
import paho.mqtt.client as mqtt #import the client1
import owl_database
import owl_settings
import time

# callback - on_message
def on_message(client, userdata, message):
    # message is received
    print('- MQTT - message is received')

    # extract data
    payload = str(message.payload.decode("utf-8"))
    topic = message.topic
    data = {'topic':topic, 'payload':payload}
    # send data to writer
    userdata(data)


# callback - on_connect
def on_connect(client, userdata, flags, reasonCode):
    # connected
    print('- MQTT - connected')

    # get subscribes from DB
    subscribes = owl_database.get_mqtt_subscribes()
    set_subscribes(client, subscribes)


# callback - on_subscribe
def on_subscribe(client, userdata, mid, granted_qos):
    print('- MQTT - subscribed')
    print('Granted QoS:')
    print(granted_qos)


# callback - on_publish
def on_publish(client, userdata, mid):
    print('- MQTT - published')


# callback - on_disconnect
def on_disconnect(client, userdata, rc):
    print('- MQTT - disconnected')
    if(rc != 0):
        print('Unexpected disconnection.')


# run MQTT client
def run_client(callback_f):
    # config
    cfg = owl_settings.load(owl_settings.CFG_FILE)
    MQTT_cfg = owl_settings.MQTT(cfg)
    # create new instance
    print('- MQTT - creating new instance')
    client = mqtt.Client('P1')

    # set callbacks
    client.on_message = on_message
    #
    client.user_data_set(callback_f)
    #
    client.on_connect = on_connect
    #
    client.on_publish = on_publish
    #
    client.on_subscribe = on_subscribe
    #
    client.on_disconnect = on_disconnect

    # if username and password set
    if(MQTT_cfg['Username'] != ''):
        print('- MQTT - username set')
        client.username_pw_set(MQTT_cfg['Username'], MQTT_cfg['Password'])

    print('- MQTT - connecting to broker...')

    # connect to broker
    client.connect(MQTT_cfg['Address'], int(MQTT_cfg['Port']))

    # start the loop
    client.loop_start()

    #temperary - for test
    time.sleep(10)

    return client


# set subscribes from DB
def set_subscribes(client, subscribe_list):
    # count_topics = len(subscribe_list)
    print('Subscribes list:')
    for i in range(len(subscribe_list)):
        print(subscribe_list[i])
        client.subscribe(subscribe_list[i][0], int(subscribe_list[i][1]))

    test_subscibes(client)

    #client.loop_stop() #stop the loop


# publish testing message
def test_subscibes(client):
    # publish for test
    print('- MQTT - Publishing message to topic','house/bulbs/bulb2')
    client.publish('house/bulbs/bulb3','Hello2',1)

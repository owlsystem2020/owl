#!/usr/bin/env python3
#import owl_settings
import owl_database
import owl_mqtt

# start
print('- Owl server is starting')

# create default database tables
owl_database.create_MQTT_database()

# MQTT client run
mqtt_client = owl_mqtt.run_client(owl_database.mqtt_message_writer)

# just for test
owl_database.sql_reader()


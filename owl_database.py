#!/usr/bin/env python3
import owl_settings
import sqlite3

# connection
def connect(DB_cfg):
    # database
    try:
        conn = sqlite3.connect(DB_cfg['Database'])
    except sqlite3.Error as e:
        print(e)

    c = conn.cursor()
    
    return c


# sql query
def sql_writer(sql):
    # configuratuon
    cfg = owl_settings.load(owl_settings.CFG_FILE)
    db_cfg = owl_settings.DB(cfg)
    database = db_cfg['Database']

    # database
    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(e)

    database_cur = conn.cursor()

    #DB config
    try:
        database_cur.execute(sql)
        rows = database_cur.fetchall()
    except sqlite3.Error as e:
        print(e)

    # close all
    conn.commit()
    database_cur.close()
    conn.close()

    return rows


# MQTT writer
def mqtt_message_writer(message):
    # put into DB
    sql = 'INSERT INTO mqtt_row_data (topic, payload) VALUES ("' + message['topic'] + '", "' + message['payload'] + '")'
    sql_writer(sql)


# reader from DB
def sql_reader():
    # just for DB test
    sql = 'SELECT * FROM mqtt_row_data'

    # configuratuon
    rows = sql_writer(sql)

    # print all
    for row in rows:
        print(row)


# get MQTT subscribes from DB
def get_mqtt_subscribes():
    # select subscribes from DB
    print('- get MQTT subscribes')
    sql = 'SELECT topic, QoS FROM mqtt_subscribes'
    rows = sql_writer(sql)

    return rows


# DB creation
def create_database(database_name):
    sql = 'CREATE DATABASE ' + database_name
    sql_writer(sql)


# init for MQTT DB
def create_MQTT_database():
    # table for subscribes
    sql = '\
    CREATE TABLE IF NOT EXISTS mqtt_subscribes (\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        topic varchar(255),\
        QoS int,\
        comment varchar(255)\
    )'
    sql_writer(sql)

    #sql = 'DROP TABLE mqtt_row_data'
    #sql_writer(sql)

    # table for received data
    sql = '\
    CREATE TABLE  IF NOT EXISTS  mqtt_row_data (\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        topic varchar(255),\
        payload varchar(255)\
    )'
    sql_writer(sql)

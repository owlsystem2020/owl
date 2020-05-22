#!/usr/bin/env python3
import configparser

global CFG_FILE
CFG_FILE = 'owl.cfg'

# version is supported by config 
cfg_version = "1.0"

# load config
def load(config_file):
    # Load config
    cfg = configparser.ConfigParser()
    cfg.read(config_file)

    return cfg


# check version
def chech_cfg_version(version):
    # Config version
    if(version != cfg_version):
        print('Oops! - config version is wrong')
        exit()
    else:
        print('- Config version ' + cfg_version)


# config for MQTT
def MQTT(cfg):
    MQTT_cfg = {
        'Address' : cfg['MQTT']['Address'], 
        'Port' : cfg['MQTT']['Port'], 
        'Username' : cfg['MQTT']['Username'], 
        'Password' : cfg['MQTT']['Password']
    }
    return MQTT_cfg


# config for DB
def DB(cfg):
    DB_cfg = {
        'Type' : cfg['Database']['Type'],
        'Database' : cfg['Database']['Database'],
        'Host' : cfg['Database']['Host'],
        'Port' : cfg['Database']['Port'],
        'User' : cfg['Database']['User'],
        'Password' : cfg['Database']['Password']
    }
    return DB_cfg


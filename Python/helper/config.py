import configparser
import logging
import sys
import os

config = configparser.ConfigParser()
configDir = "./config"
configFile = "config/config.ini"

"""
Helper function to get the value of a config parameter

conf = helper.config.initconfig()
"""

def initconfig():
    if not os.path.isdir(configDir):
        os.mkdir(configDir)
        os.mkdir('./log')
    if not os.path.isfile(configFile):
        create()
    #Konfigdatei initialisieren
    try:
        #Config Datei auslesen
        config.read(configFile)
        return config['DEFAULT']
    except Exception as e:
        print("Error while loading the Config file:" + \
            str(sys.exc_info()) + "\n" + \
            str(e.message) + " " + str(e.args))
        logging.error("Error while loading the Config file" + str(sys.exc_info()) + \
            str(sys.exc_info()) + "\n" + \
            str(e.message) + " " + str(e.args))

def create():
    with open("config/config.template.ini", "r") as configtemp:
        config = configtemp.read()
    with open("config/config.ini", "w") as configfile:
        configfile.write(config)

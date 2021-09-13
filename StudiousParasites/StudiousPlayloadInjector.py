#!/usr/bin/python3
#coding: utf-8

from os import system

class Studious_Playload_Injector(object):
    def __init__(self):
        self.destination_filepath = None
        self.loaded_playload = None
        #
    def init(self):
        self.destination_filepath = None
        self.loaded_playload = None
    def setDestinationOfInjection(self, destined_filepath):
        self.destination_filepath = destined_filepath
        #
    def setPlayloadToInjection(self, playload):
        self.loaded_playload = playload
        #
    def inject(self, destination_filepath = None, 
                configured_playload = None):
        if destination_filepath == None:
            destination_filepath = self.destination_filepath
        if configured_playload == None:
            configured_playload = self.loaded_playload
        #
        try:
            #injection operations, 
            # at the end of file, 
            # writing in append mode
            with open(destination_filepath, "a") as configuration_file:
                configuration_file.write("\n{}".format(configured_playload))
                configuration_file.close()
        except Exception as e:
            print("\nError ! : \n{e}".format( e = e ))
            exit(-1)
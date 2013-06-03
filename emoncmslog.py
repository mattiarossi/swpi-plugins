###########################################################################
#     Sint Wind PI
#     Copyright 2012 by Tonino Tarsi <tony.tarsi@gmail.com>
#
#     USB comunication based pywws by 'Jim Easterbrook' <jim@jim-easterbrook.me.uk>
#     Please refer to the LICENSE file for conditions
#     Visit http://www.vololiberomontecucco.it
#
#   Emoncmslog plugin logs meteo data from sint wind pi to emoncms (http://emoncms.org/) using
#   the provided api (http://emoncms.org/site/docs/inputsandfeeds)
#
#   In order to successfully log data three parameters are required:
#
#   emoncms_serverfile: URL to emoncms post.json page
#   emoncms_apikey: WRITE API (available from emoncms interface at the url /emoncms/input/api)
#   emoncms_modeid: node id to identify the meteo data in the input config page
#
#
##########################################################################

"""emoncmslog plugin."""

import threading
import random
import datetime
import sys
import subprocess
import sys
import os
import thread
import time
import requests
import globalvars
import meteodata
from TTLib import  *



class swpi_plugin(threading.Thread):  #  do not change the name of the class

    def __init__(self,cfg):

        ###################### Plugin Initialization ################
        self.cfg = cfg
        self.last_measure_time = None
        self.sleep_time=30

        self.emoncms_apikey = "apikey"
        self.emoncms_serverfile = "http://localhost/emoncms/input/post.json"
        self.emoncms_nodeid = 9999

        threading.Thread.__init__(self)


        ###################### End Initialization ##################

    def logDataToEmonCMS(self):

        if ( globalvars.meteo_data.last_measure_time == None):
            return


        if(globalvars.meteo_data.last_measure_time == self.last_measure_time):
            log("Emoncmsplugin: No change detected")
            return


    #   Assign inputs to a node group   /emoncms/input/post.json?node=1&csv=100,200,300
    #   Inputs we want to log:
    #
    #           globalvars.meteo_data.hum_out = hum
    #           globalvars.meteo_data.temp_out = temp
    #           globalvars.meteo_data.wind_ave   = Wind_speed
    #           globalvars.meteo_data.wind_gust = Gust_Speed
    #           globalvars.meteo_data.wind_dir = dire*22.5
    #           globalvars.meteo_data.wind_dir_code = dir_code
    #           globalvars.meteo_data.rain = rain
    #           globalvars.meteo_data.winDayMin
    #           globalvars.meteo_data.rain_rate
    #           globalvars.meteo_data.wind_chill
    #           globalvars.meteo_data.temp_apparent
    #           globalvars.meteo_data.dew_point
    #           globalvars.meteo_data.winDayMax
    #           globalvars.meteo_data.winDayGustMin
    #           globalvars.meteo_data.winDayGustMax
    #           globalvars.meteo_data.TempOutMin
    #           globalvars.meteo_data.TempOutMax
    #           globalvars.meteo_data.wind_dir_ave
    #           globalvars.meteo_data.rain_rate_24h
    #           globalvars.meteo_data.rain_rate_1h
    #           globalvars.meteo_data.battery
    #

        self.last_measure_time = globalvars.meteo_data.last_measure_time
        param_list = []

        if globalvars.meteo_data.hum_out != None : param_list.append("{:.2f}".format((globalvars.meteo_data.hum_out)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.temp_out != None : param_list.append("{:.2f}".format((globalvars.meteo_data.temp_out)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.temp_apparent != None : param_list.append("{:.2f}".format((globalvars.meteo_data.temp_apparent)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.TempOutMin != None : param_list.append("{:.2f}".format((globalvars.meteo_data.TempOutMin)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.TempOutMax != None : param_list.append("{:.2f}".format((globalvars.meteo_data.TempOutMax)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.rain != None : param_list.append("{:.4f}".format((globalvars.meteo_data.rain)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.rain_rate != None : param_list.append("{:.4f}".format((globalvars.meteo_data.rain_rate)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.rain_rate_1h != None : param_list.append("{:.4f}".format((globalvars.meteo_data.rain_rate_1h)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.rain_rate_24h != None : param_list.append("{:.4f}".format((globalvars.meteo_data.rain_rate_24h)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_ave != None : param_list.append("{:.2f}".format((globalvars.meteo_data.wind_ave)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_gust != None : param_list.append("{:.2f}".format((globalvars.meteo_data.wind_gust)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_dir != None : param_list.append("{:.2f}".format((globalvars.meteo_data.wind_dir)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_chill != None : param_list.append("{:.2f}".format((globalvars.meteo_data.wind_chill)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.dew_point != None : param_list.append("{:.2f}".format((globalvars.meteo_data.dew_point)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.winDayMin != None : param_list.append("{:.2f}".format((globalvars.meteo_data.winDayMin)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.winDayMax != None : param_list.append("{:.2f}".format((globalvars.meteo_data.winDayMax)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.winDayGustMin != None : param_list.append("{:.2f}".format((globalvars.meteo_data.winDayGustMin)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.winDayGustMax != None : param_list.append("{:.2f}".format((globalvars.meteo_data.winDayGustMax)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_dir_ave != None : param_list.append("{:.4f}".format((globalvars.meteo_data.wind_dir_ave)))
        else :
            param_list.append("0");
        if globalvars.meteo_data.battery != None : param_list.append(str(globalvars.meteo_data.battery))
        else :
            param_list.append("-1");

        parameters = '?apikey=' + str(self.emoncms_apikey) +'&node='+str(self.emoncms_nodeid)+'&csv='+','.join(param_list)

        #print  parameters
        log("logToEmonCMS - url: " + self.emoncms_serverfile + " - Parameters: " + parameters)
        try:
            r = requests.get(self.emoncms_serverfile+parameters,timeout=10)
            msg = r.text.splitlines()
            log("Log to EmonCms Result: " +  msg[0])
        except Exception,e:
            log(  "Error Logging to EmonCms : " + str(e) )





    def run(self):
        log("Starting plugin : %s" % sys.modules[__name__])
        while 1:
        ###################### Plugin run
            time.sleep(self.sleep_time)
            if ( globalvars.meteo_data.status == 0 ):
                if ( globalvars.meteo_data.last_measure_time != None and  globalvars.meteo_data.status == 0 ) :
                    log("Logging data to EmonCMS plugin ...")
                    self.logDataToEmonCMS()
        ###################### end of Plugin run

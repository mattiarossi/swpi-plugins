###########################################################################
#     Sint Wind PI
#     Copyright 2012 by Tonino Tarsi <tony.tarsi@gmail.com>
#
#     USB comunication based pywws by 'Jim Easterbrook' <jim@jim-easterbrook.me.uk>
#     Please refer to the LICENSE file for conditions
#     Visit http://www.vololiberomontecucco.it
#
#
#
#   Wugraphslog plugin logs meteo data from sint wind pi to a local mysql table to be used by wugraphs 
#
#   In order to successfully log data a mysql database connection with the proper table already created must be provided
#
#
#     CREATE TABLE `wugraphs` (
#       `average_windspeed` float DEFAULT '0',
#       `wind_direction` smallint(3) DEFAULT '0',
#       `gust_windspeed` float DEFAULT '0',
#       `temperature` float DEFAULT '0',
#       `outdoor_humidity` float DEFAULT '0',
#       `barometer` float DEFAULT '0',
#       `daily_rainfall` float DEFAULT '0',
#       `rain_rate` float DEFAULT '0',
#       `indoor_temperature` float DEFAULT '0',
#       `indoor_humidity` float DEFAULT '0',
#       `actual_solar_reading` int(11) DEFAULT '0',
#       `max_daily_temperature` float DEFAULT '0',
#       `min_daily_temperature` float DEFAULT '0',
#       `max_gust_current_day` float DEFAULT '0',
#       `dew_point_temperature` float DEFAULT '0',
#       `datetime` datetime DEFAULT NULL,
#       `current_weather_desc` text,
#       `davis_vp_uv` float DEFAULT '0'
#     ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
#
#
##########################################################################

"""wugraphslog plugin."""

import threading
import random
import datetime
import sqlite3
import sys
import subprocess
import sys
import os
import thread
import time

import globalvars
import meteodata
from TTLib import  *
import MySQLdb







class swpi_plugin(threading.Thread):  #  do not change the name of the class

    def __init__(self,cfg):
        self.cfg = cfg
        self.mysqlDB = None
        self.last_measure_time = None
        self.sleep_time=30

        self.wugraphs_dbhost = "localhost"
        self.wugraphs_dbport = 3306
        self.wugraphs_user = "user"
        self.wugraphs_password = "pass"
        self.wugraphs_schema = "weather"
        self.wugraphs_table = "wugraphs"

        threading.Thread.__init__(self)

        ###################### Plugin Initialization ################

        ###################### End Initialization ##################



    def mysqlFormatString(self,value,formatstring):
        if (value is None):
            value = 0
        else:
            value = formatstring.format((value))
        return value



    def logDataToWugraphs(self):

        if ( globalvars.meteo_data.last_measure_time == None):
            return

        if(globalvars.meteo_data.last_measure_time == self.last_measure_time):
            log("logToWugraphs: No change detected")
            return

        self.last_measure_time = globalvars.meteo_data.last_measure_time


        cur = self.mysqlDB.cursor();

        sql = "INSERT INTO "+ self.wugraphs_table + " (datetime, outdoor_humidity, temperature, daily_rainfall, rain_rate, wind_direction, average_windspeed, gust_windspeed, dew_point_temperature, indoor_humidity, indoor_temperature, barometer, max_daily_temperature, min_daily_temperature, max_gust_current_day ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        datetimeMeas = globalvars.meteo_data.last_measure_time
        hum_out = self.mysqlFormatString(globalvars.meteo_data.hum_out, "{:.2f}")
        temp_out = self.mysqlFormatString(globalvars.meteo_data.temp_out, "{:.2f}")
        rain_rate = self.mysqlFormatString(globalvars.meteo_data.rain_rate, "{:.4f}")
        rain_rate_1h = self.mysqlFormatString(globalvars.meteo_data.rain_rate_1h, "{:.4f}")
        wind_dir = self.mysqlFormatString(globalvars.meteo_data.wind_dir, "{:.2f}")
        wind_ave = self.mysqlFormatString(globalvars.meteo_data.wind_ave, "{:.2f}")
        wind_gust = self.mysqlFormatString(globalvars.meteo_data.wind_gust, "{:.2f}")
        dew_point = self.mysqlFormatString(globalvars.meteo_data.dew_point, "{:.2f}")
        hum_in = self.mysqlFormatString(globalvars.meteo_data.hum_in, "{:.2f}")
        temp_in = self.mysqlFormatString(globalvars.meteo_data.temp_in, "{:.2f}")
        rel_pressure = self.mysqlFormatString(globalvars.meteo_data.rel_pressure, "{:.2f}")
        temp_out_max = self.mysqlFormatString(globalvars.meteo_data.TempOutMax, "{:.2f}")
        temp_out_min = self.mysqlFormatString(globalvars.meteo_data.TempOutMin, "{:.2f}")
        winDayGustMax = self.mysqlFormatString(globalvars.meteo_data.winDayGustMax, "{:.2f}")
		
        #print  parameters
        log("logToWugraphs ...")
        try:
            cur.execute(sql,(datetimeMeas,hum_out,temp_out,rain_rate,rain_rate_1h,wind_dir,wind_ave,wind_gust,dew_point,hum_in,temp_in,rel_pressure,temp_out_max,temp_out_min,winDayGustMax))
            self.mysqlDB.commit()
        except MySQLdb.Error, e:
            log(  "Error Logging to Wugraphs : "  )
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)



    def run(self):
        log("Starting plugin : %s" % sys.modules[__name__])
        try:
            self.mysqlDB = MySQLdb.connect(host=self.wugraphs_dbhost,user=self.wugraphs_user, passwd=self.wugraphs_password, db=self.wugraphs_schema, port=int(self.wugraphs_dbport))
        except Exception,e:
            log("Error connecting to Wugraphs db : " + str(e))
            return


        while 1:
        ###################### Plugin run
            time.sleep(self.sleep_time)
            if ( globalvars.meteo_data.status == 0 ):
                if ( globalvars.meteo_data.last_measure_time != None and  globalvars.meteo_data.status == 0 ) :
                    log("Logging data to wugraphs plugin")
                    self.logDataToWugraphs()
                    log("Logging data to wugraphs plugin: Success!")

        ###################### end of Plugin run

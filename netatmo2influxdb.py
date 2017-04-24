# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import lnetatmo
import influxdb


debug = False
netatmoDB = 'netatmo_dev'
mainmodule = 'Wohnzimmer'
outdoormodule = 'Balkon'

##
# netatmo
##
# get current weather station data
auth = lnetatmo.ClientAuth(username="xx",
                           password="yy",
                           clientId = "zz", 
                           clientSecret = "uu")
weatherData = lnetatmo.WeatherStationData(auth)
lastdata = weatherData.lastData()
if (debug):
    print("Info:\n"+str(lastdata)) 
 # modify data types for influx db
lastdata[mainmodule]['AbsolutePressure']=float(lastdata[mainmodule]['AbsolutePressure'])           
lastdata[mainmodule]['CO2']=float(lastdata[mainmodule]['CO2'])  
lastdata[mainmodule]['Humidity']=float(lastdata[mainmodule]['Humidity']) 
lastdata[mainmodule]['Noise']=float(lastdata[mainmodule]['Noise']) 
lastdata[mainmodule]['Pressure']=float(lastdata[mainmodule]['Pressure'])
lastdata[mainmodule]['Temperature']=float(lastdata[mainmodule]['Temperature'])  
lastdata[mainmodule]['max_temp']=float(lastdata[mainmodule]['max_temp'])
lastdata[mainmodule]['min_temp']=float(lastdata[mainmodule]['min_temp'])

lastdata[outdoormodule]['Humidity']=float(lastdata[outdoormodule]['Humidity'])
lastdata[outdoormodule]['Temperature']=float(lastdata[outdoormodule]['Temperature'])
lastdata[outdoormodule]['max_temp']=float(lastdata[outdoormodule]['max_temp'])
lastdata[outdoormodule]['min_temp']=float(lastdata[outdoormodule]['min_temp'])

## 
# influxdb
##
client = influxdb.InfluxDBClient(host='cubietruck', port=8086)
# create netatmo database if needed
databases = client.get_list_database()
if (not({'name': netatmoDB} in databases)):
    client.create_database(netatmoDB)
    if (debug):
        print("Info: database "+netatmoDB+" created.")
else:
    if (debug):
        print("Info: database "+netatmoDB+" already exists. Nothing to be done.")

# switch to netatmo database
client.switch_database(netatmoDB)
# prepare data for main module
data={"measurement": mainmodule,
             "time": lastdata[mainmodule]['When']}
data["fields"]= lastdata[mainmodule]
client.write_points([data],protocol='json')
# prepare data for outdoor module
data={"measurement": outdoormodule,
             "time": lastdata[outdoormodule]['When']}
data["fields"]= lastdata[outdoormodule]
client.write_points([data],protocol='json')             




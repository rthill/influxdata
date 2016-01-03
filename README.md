# smarthome-influxdata
Plugin to store data from smarthome.py in a InfluxData TSDB i.e. for graphing with Grafana or Chronograf.
This plugin uses InfluxData UDP line protocol for non-blocking execution.

Thanks to SgtSeppel for the initial plugin which can be found here: https://github.com/SgtSeppel/influxdb

## Configuration
### plugin.conf
<pre>
[influxdata]
    class_name = InfluxData
    class_path = plugins.influxdata
#   influx_host = localhost
#   influx_port = 8089
    influx_keyword = influx
</pre>

### plugin.conf
The configuration flag influx_keyword has a special relevance. Here you can choose which keyword the plugin should look for.
If you do not specify anything, the default keyword "influx" will be use i.e.:

<pre>
[['living_temperature']]
    type = num
    knx_dpt = 9
    influx = true
    visu_acl = true
    knx_send = 7/0/0
    knx_reply = 7/0/0
    cache = on
</pre>

However, you can change this. Many people use the sqlite keyword to store data in a sqlite database.
If you set 
<pre>
influx_keyword = sqlite
</pre>
you do not have to update anything in your item configuration files. All data thats pushed to sqlite (i.e. for smartVISU) will automatically be copied to InfluxData also.

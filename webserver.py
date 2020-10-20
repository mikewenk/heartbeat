#!/usr/bin/env python3
import serial 
import re
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        data = readHeartbeat()
    except Exception as err: 
        app.logger.error("Error: %s",err)
        data = {'heartbeat': 'UNK', 'color': '#007fbf'}
    return '''
<html>
    <head>
        <meta http-equiv="refresh" content="5"> 
        <title>hearbeat</title>
    </head>
    <body>

<div style="background-color: transparent; font-size: 5em; text-align: center; font-family: Play; color: ''' + data['color'] + ''';"><link href="https://fonts.googleapis.com/css?family=Play" rel="stylesheet">''' + data['heartbeat'] + ''' </div>
    </body>
</html>'''



def readHeartbeat():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().strip().decode('ascii')
            chunks = line.split(',')
            vals = chunks[0]
            if vals and vals[0].isdigit(): 
                val = int(vals) 
                if val > 40 and val < 150: 
                    hb = str(val)
                    if val < 75:  
                        ret = { 'heartbeat': hb, 'color': '#3df400'}
                    elif val < 85:  
                        ret = { 'heartbeat': hb, 'color': '#e9ff00'}
                    elif val < 95:  
                        ret = { 'heartbeat': hb, 'color': '#ff9400'}
                    elif val < 110:  
                        ret = { 'heartbeat': hb, 'color': '#ff0000'}
                    else:
                        ret = { 'heartbeat': hb, 'color': '#ae0709'}

                    return ret

   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

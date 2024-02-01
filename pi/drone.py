from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


#Give a unique ID for the drone
#===================================================================
myID = "DRONE_2"
#===================================================================

# Get initial longitude and latitude the drone
#===================================================================
current_longitude = 13.21008
current_latitude = 55.71106
with open('filen.txt','w') as output_fil:
          output_fil.write(current_longitude+'\n')
          output_fil.write(current_latitude+'\n')
          output_fil.close()
#===================================================================

drone_info = {'id': myID,
                'longitude': current_longitude,
                'latitude': current_latitude,
                'status': 'idle'
            }

# Fill in the IP address of server, and send the initial location of the drone to the SERVER
#===================================================================
SERVER="http://192.168.1.2:5001/drone"
with requests.Session() as session:
    resp = session.post(SERVER, json=drone_info)
#===================================================================

@app.route('/', methods=['POST'])
def main():
    coords = request.json
    # Get current longitude and latitude of the drone 
    #===================================================================
    with open('filen.txt', 'r') as fil: 
              #rader = fil.read().splitlines()
              Long=float(fil.readline())
              Lat = float(fil.readline())
    # long_variabel = rader[0]
    # lat_variabel=rader[1]


    current_longitude = Long
    current_latitude = Lat
    #===================================================================
    from_coord = coords['from']
    to_coord = coords['to']
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    long = current_longitude
    lat= current_latitude
    return 'New route received'
   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

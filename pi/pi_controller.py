import math
import requests
import argparse
from time import sleep

#Write you own function that moves the drone from one place to another 
#the function returns the drone's current location while moving
#====================================================================================================
def moveDrone(current_coords, from_coords, to_coords, index):
    
    delta_long = (from_coords[0] - current_coords[0])
    delta_lat = (from_coords[1] - current_coords[1])
    dist = math.sqrt(deltaLong**2 + deltaLat**2)

    sleep(0.02)
    
    return (current_coords[0] + index * ((delta_long / dist) / 10000), current_coords[1] + index * ((delta_lat / dist) / 10000))
#====================================================================================================


def run(current_coords, from_coords, to_coords, SERVER_URL):
    # Compmelete the while loop:
    # 1. Change the loop condition so that it stops sending location to the data base when the drone arrives the to_address
    # 2. Plan a path with your own function, so that the drone moves from [current_address] to [from_address], and the from [from_address] to [to_address]. 
    # 3. While moving, the drone keeps sending it's location to the database.
    #====================================================================================================
    index = 0
    dist_x = abs(current_coords[0] - from_coords[0])
    dist_y = abs(current_coords[1] - from_coords[1])
    
    while (dist_x > 0.001 or dist_y > 0.001):
        index += 1
        print(dist_x)
        print(dist_y)
        
        drone_coords = moveDrone(current_coords, from_coords, to_coords, index)
        
        dist_x = abs(drone_coords[0] - from_coords[0])
        dist_y = abs(drone_coords[1] - from_coords[1])
        
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
  #====================================================================================================

   
if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords)
    print(from_coords)
    print(to_coords)

    run(current_coords, from_coords, to_coords, SERVER_URL)

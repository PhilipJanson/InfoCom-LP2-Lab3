import math
import requests
import argparse
from time import sleep


def moveDrone(current_coords, next_coords, index):
    
    # Calculate the difference in distance for both x and y
    # Calculate the total distance between start and end
    delta_long = (next_coords[0] - current_coords[0])
    delta_lat = (next_coords[1] - current_coords[1])
    dist = math.sqrt(delta_long ** 2 + delta_lat ** 2)

    sleep(0.02)
    
    return (current_coords[0] + index * ((delta_long / dist) / 10000), current_coords[1] + index * ((delta_lat / dist) / 10000))


def run(current_coords, from_coords, to_coords, SERVER_URL):
    
    # Setup
    # index starts at 0
    # Set the next destiantion to the first adress
    # Calculate the distance to the end location
    index = 0
    next_coords = from_coords
    dist_x = abs(current_coords[0] - next_coords[0])
    dist_y = abs(current_coords[1] - next_coords[1])
    
    # Keep looping if the distance of both the x and y are not 0.001 from the end.
    while (dist_x > 0.001 or dist_y > 0.001):
        
        # Add 1 to index and move the drone
        index += 1
        drone_coords = moveDrone(current_coords, next_coords, index)
        
        # Calculate the new distance from the end coordinates
        # after the drone has moved.
        dist_x = abs(drone_coords[0] - next_coords[0])
        dist_y = abs(drone_coords[1] - next_coords[1])
        
        # Check if the drone has reached its destination, if it has:
        # Set the current_coords to the actual location.
        # Set the next destiantion to the second adress.
        # Calculate the new distance after changing the start and end position.
        if not (dist_x > 0.001 or dist_y > 0.001):
            current_coords = drone_coords
            next_coords = to_coords
            index = 0
            dist_x = abs(drone_coords[0] - next_coords[0])
            dist_y = abs(drone_coords[1] - next_coords[1])
            print("Destination reached")
            sleep(0.5)
            
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
    
    print("End reached")

   
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

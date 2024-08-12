import googlemaps
from datetime import datetime
import re
import html
from geopy.distance import geodesic
import time
from speech_text import *
from text_speech import *
from gps import *

# Function to calculate distance between current location and next turn
def calculate_distance(current_loc, next_turn):
    return geodesic(current_loc, next_turn).feet

# Function to get real-time user location (mock implementation)
#FIX LATER TO GET GPS STUFF!!
def get_current_location():
    coords = location()
    latitude = coords[0]
    longitude = coords[1]
    return (latitude, longitude)

sites = stt() #replace with actual file when we find out how to do that on pi's 

apiKey = "your api key"
map_client = googlemaps.Client(apiKey)

# Takes start and end locations from user
start = sites[0]
end = sites[1]

# This requests the directions
directions = map_client.directions(start, end, mode="walking")

# Loop through the directions and provide instructions
for route in directions:
    for leg in route['legs']:
        for step in leg['steps']:
            #Cleans up instructions to print
            clean_instructions = re.sub('<[^<]+?>', '', html.unescape(step['html_instructions']))
            tts(clean_instructions)
            next_turn_location = (step['end_location']['lat'], step['end_location']['lng'])
        
            instruction_given = False
            while not instruction_given:
                current_location = get_current_location()
            
                distance = calculate_distance(current_location, next_turn_location)
                
                if distance <= 42 and distance >= 40:  # If within 40 meters of the turn
                    tts(clean_instructions + " in 40 feet")
                elif distance >= 10 and distance <= 12: 
                    tts(clean_instructions + " in 10 feet") 
                elif distance <= 2: 
                    tts(clean_instructions + " in 2 feet")
                    instruction_given = True 

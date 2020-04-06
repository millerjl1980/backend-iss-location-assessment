#!/usr/bin/env python

__author__ = "Justin Miller using class walkthru on 4/1 demo recording"

import sys
import time
import turtle
import requests

if(sys.version_info[0] < 3):
    raise RuntimeError('This program requires Python 3+')

base_url = 'http://api.open-notify.org'
iss_icon = 'iss.gif'
world_map = 'map.gif'

def get_astronauts():
    """Returns dictionary of astronatus and spacecrafts from API"""
    r = requests.get(base_url + '/astros.json')
    r.raise_for_status() # Checks get request for any status other than 200, will throw runtime error
    return r.json()['people']

def get_iss_location():
    """Returns the current location of ISS"""
    r = requests.get(base_url + '/iss-now.json')
    r.raise_for_status()
    position = r.json()['iss_position']
    lat = float(position['latitude'])
    lon = float(position['longitude'])
    return lat, lon

def map_iss(lat, lon):
    """Draw a world map and place ISS icon at lat, lon"""
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(iss_icon)
    iss = turtle.Turtle()
    iss.shape(iss_icon)
    iss.setheading(90) # set heading of icon on screen 
    iss.penup() # penup vs pendown will track movment on screen
    iss.goto(lon, lat)
    return screen

def compute_rise_time(lat, lon):
    """Return the next horizon rise-time of ISS for specific lat/lon"""
    params = {'lat': lat, 'lon': lon}
    r = requests.get(base_url + '/iss-pass.json', params=params)
    r.raise_for_status()

    passover_time = r.json()['response'][1]['risetime']
    return time.ctime(passover_time)

def main():
    # Part A
    astro_dict = get_astronauts()
    print('\nCurrent people in space: {}'.format(len(astro_dict)))
    for a in astro_dict:
        print(' - {} in {}'.format(a['name'], a['craft']))
    
    # Part B
    lat, lon = get_iss_location()
    print('\nCurrent ISS coordinates: lat={:.02f} lon={:.02f}'.format(lat, lon))

    # Part C
    screen = None
    try:
        screen = map_iss(lat, lon)

        # Part D
        indy_lat = 39.768403
        indy_lon = -86.158068
        location = turtle.Turtle()
        location.penup()
        location.color('yellow')
        location.goto(indy_lon, indy_lat)
        location.dot(5)
        location.hideturtle()
        next_pass = compute_rise_time(indy_lat, indy_lon)
        location.write(next_pass, align='center', font=('Arial', 12, 'normal'))
    except RuntimeError as e:
        print('Error: problem loding graphics: ' + str(e))  

    # leave map on screen until user closes it
    if screen is not None:
        print('Click on screen to exit...')
        screen.exitonclick()

if __name__ == '__main__':
    main()

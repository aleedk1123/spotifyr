#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Anthony Withrow
@project: S670 Final Project

This script will get song title and artist data from billboard for some
  specified genres. It will then get the data from spotify that is needed
  to get the track audio features. The last step will be done in R.
"""

#****************************************************************************
# Imports
#****************************************************************************
#import the libraries we will need
import os
import pandas as pd

#set the working directory so we can import our custom functions
try:
    ABS_PATH = os.path.abspath(__file__)

except:
    ABS_PATH = os.path.abspath('')

os.chdir(os.path.dirname(ABS_PATH))

import billboard
import spotify

#billboard.charts()

#****************************************************************************
# Functions
#****************************************************************************
#we want to get the top 100 songs from two different generes
#for the last 10 years or so
def main():
    """Get the data we want from billboard and spotify
    """
    genres = ['hot-country-songs', 
              'hot-r-and-and-b-hip-hop-songs',
              'hot-rock-songs',
              'hot-latin-songs',
              'hot-dance-electronic--songs',
              'pop-songs']
    genre_title = ['country', 'r&b/hiphop', 'rock', 
                   'latin', 'dance', 'pop']
    years = 11
    sleep_time = 1

    columns = ['Genre', 'Title', 'Artist']
    data = []

    #get the data we want
    for genre in genres:
        songs = billboard.get_chart_multiple_years(genre, years, sleep_time)

        for song in songs:
            song[0] = genre_title[genres.index(song[0])]
            data.append(song)

    #create a datafram with our data in it
    chart_data = pd.DataFrame(data, columns=columns)

    #get the uri for the songs that we can
    chart_data = spotify.get_song_data(chart_data)

    #remove the songs we cound not find a uri for
    chart_data = chart_data[chart_data.URI != ""]

    #save the songs to a csv to be used later
    chart_data.to_csv("song_data.csv", index=False)

    print("Data has been generated and saved to song_data.csv")

#if we are running the script, then run the main function
if __name__ == "__main__":
    main()

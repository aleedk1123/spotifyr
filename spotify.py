#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Anthony Withrow
@project: S670 Final Project - compare genres based on spotify data
This script will provide functions to call the Spotify API and get
  information about the tracks that may be of interest. These are inteded to
  be helper functions, not a script to be run by itself.
"""

#****************************************************************************
# Imports
#****************************************************************************
#import the libraries we will need
import urllib
import requests

#****************************************************************************
# Functions
#****************************************************************************

def get_token():
    """Get the authorization token we will need to make requests
    """
    client_id = "b6eb08407bab41b4b3f8f5bb48a0f8f0"
    client_secret = "73efc29aa9b442fdbc83019dfc8fc0ed"

    grant_type = 'client_credentials'

    body_params = {'grant_type' : grant_type}

    url = 'https://accounts.spotify.com/api/token'

    response = requests.post(url, data=body_params,
                             auth=(client_id, client_secret))

    token = response.json()['access_token']

    return token

def get_song_data(chart_data):
    """Get the uri for the songs in the dataframe passed in
    
    Keyword arguments:
        chart_data -- dataframe containing song title and artists to look for
    """
    #set the base search url
    base_search_url = 'https://api.spotify.com/v1/search?'

    #get the authorization token
    token = get_token()

    #create an empty list to store the uri values to add to the dataframe
    song_uris = [""] * chart_data.shape[0]

    #loop through the rows in the dataframe and get the song information
    #from spotify
    for index, row in chart_data.iterrows():
        #urlencode the song title
        url_title = urllib.parse.quote(row['Title'])

        #format the url to send the request to
        url = '{0}q={1}&type=track'.format(base_search_url, url_title)

        #add the authorization header for the request
        headers = {'Authorization' : 'Bearer {0}'.format(token)}

        #make the request and get the response
        response = requests.get(url, headers=headers)

        #loop through the response and get the first uri that matches
        #with the artist for the current song
        for item in response.json()['tracks']['items']:
            #if we found a match, add the uri to the list and move on
            if item['album']['artists'][0]['name'] in row['Artist']:
                song_uris[index] = item['uri']
                break

    #add the column to the dataframe
    chart_data.insert(3, 'URI', song_uris, True)

    #return the datafram with the new column
    return chart_data

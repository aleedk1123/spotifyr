#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Anthony Withrow
@project: S670 Final Project - compare genres based on spotify data
This script will provide functions to parse billboard charts. It is a
  modification of a pre-existing billboard.py. We are interested in year
  end charts whereas the original package was for weekly chart data.

This is based on billboard.py written by guoguo12
https://github.com/guoguo12/billboard-charts
"""

#****************************************************************************
# Imports
#****************************************************************************
#import the libraries we will need
import datetime
import time
from bs4 import BeautifulSoup
import requests as req

#****************************************************************************
# Functions
#****************************************************************************
def get_chart_data(chart_name, year="2018"):
    """Get top 100 songs for a given year and chart
    
    Keyword arguments:
        chart_name -- name of the chart to get song title and artist for
        year -- single year to get the chart for
    """
    #we will return a list of songs
    return_data = []

    #get the current year
    current_year = datetime.datetime.today().year

    #the year must be less than the current year
    if current_year <= int(year):
        raise ValueError("Year argument must be less than the current year")

    #format the url we want to read
    url_string = 'https://www.billboard.com/charts/year-end/{0}/{1}'.format(
        year,
        chart_name)

    #get the page to process
    resp = req.get(url_string)

    #get the text to process
    soup = BeautifulSoup(resp.text, 'lxml')

    #loop through the elements and get the song title and artist
    for entry_soup in soup.find_all("article", "ye-chart-item"):
        song_title = entry_soup.find('div', 'ye-chart-item__title').text.strip()
        artist = entry_soup.find('div', 'ye-chart-item__artist').text.strip()

        #append the data to the list to return
        return_data.append([chart_name, song_title, artist])

    return return_data

def get_chart_multiple_years(chart_name, num_years=10, sleep_time=0):
    """Gets the top 100 songs for multiple years
    
    Keyword arguments:
        chart_name -- name of the chart to get song title and artist for
        num_years -- number of years to get the data for
        sleep_time -- amount of time to sleep if we make too many requests
    """
    #get the current year
    current_year = datetime.datetime.today().year

    #get the most current chart
    chart_songs = get_chart_data(chart_name)

    #get the rest of the data
    for i in range(1, num_years):
        year_to_pass = current_year - i

        new_songs = get_chart_data(chart_name, str(year_to_pass))

        for song in new_songs:
            chart_songs.append(song)

        #give the API a break
        if sleep_time > 0:
            time.sleep(sleep_time)

    #return the data
    return chart_songs

def get_charts():
    """Gets a list of all Billboard charts from Billboard.com.
    """
    res = req.get("https://www.billboard.com/charts/year-end", timeout=25)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return [
        link["href"].split("/")[-1]
        for link in soup.findAll("a", {"class": "chart-panel__link"})
    ]

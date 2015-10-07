#!/usr/bin/env python
"""
Created on Tue Oct  6 18:48:42 2015

@author: anders

Wrote this basic script to be able to set my desktop background to the
Astronomy Picture of the Day from http://apod.nasa.gov/apod/

This works on Linux and should also work with OS X 
(check in set_desktop_background)

Will not change the background if the APOD is a video, just print a comment.

Make sure to change the apod_image_path for your download path.
"""

import urllib.request
import re
import os, sys
#If Mac OS X, from appscript import app, mactypes (done in if statement)


def main():
    '''Main function of script.'''
    
    #Directory to save APOD files
    apod_image_path = '/home/anders/Pictures/APOD/'
    
    image_url = determine_apod_url()
    if image_url == None:
        return

    apod_file_location = save_apod_image(image_url, apod_image_path)
    
    set_desktop_background(apod_file_location)


def determine_apod_url():
    '''opens the APOD site, finds and returns the image url.'''

    #find and read in APOD source code
    with urllib.request.urlopen('http://apod.nasa.gov/apod/') as response:
        html = str(response.read())
    
    #Regular expression to find image file url and image name (0 and 1)
    pattern = 'href="(image/\d.*?/(.*?.(?:jpg|png)))'
    regex = re.compile(pattern)
    
    try:
        #Return tuple of image urls
        image_url = regex.findall(html)[0]
    
    #If the APOD is actually a video, regex won't find an image    
    except IndexError:
        print('Today is a video, go check it out!')
        return None
    return image_url


def save_apod_image(image_url, apod_image_path):
    '''Saves the image from the given url to a given path.'''
    url = 'http://apod.nasa.gov/apod/' + image_url[0]
    
    save_file_to = apod_image_path + image_url[1]
    
    #If a pic of that file name isn't in the folder, save image to file
    if not os.path.isfile(save_file_to):
        urllib.request.urlretrieve(url, save_file_to)
    
    return save_file_to

def set_desktop_background(apod_file_location):
    '''Checks operating system and runs command to set desktop background.'''
    
    #Commands for linux
    if sys.platform == 'linux':
        command = "gsettings set org.gnome.desktop.background picture-uri\
                file://" + apod_file_location
        os.system(command)

    #Commands for Mac OS X
    elif sys.platform == 'darwin':
        from appscript import app, mactypes
        app('Finder').desktop_picture.set(mactypes.File(apod_file_location))
    


    
    
main()



    
    
    
    
    
    
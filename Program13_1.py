'''
Program Name: Program13_1.py
Prgram Description: This program reads lines from the mbox-short.txt file and displays how many messages were sent on a specific date.
Programmer: Ray, Stephen
Date: 03/28/2022
Course: CSC233-1L1
'''

import urllib.request, urllib.parse, urllib.error
import json
import ssl

def main():    

    api_key = False
    # If you have a Google Places API key, enter it here
    # api_key = 'AIzaSy___IDByT70'
    # https://developers.google.com/maps/documentation/geocoding/intro

    if api_key is False:
        api_key = 42
        serviceurl = 'http://py4e-data.dr-chuck.net/json?'
    else :
        serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        address = input('Enter location: ')
        if len(address) < 1: break

        parms = dict()
        parms['address'] = address
        if api_key is not False: parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)

        print('Retrieving', url)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        print('Retrieved', len(data), 'characters')

        try:
            js = json.loads(data)
        except:
            js = None

        if not js or 'status' not in js or js['status'] != 'OK':
            print('==== Failure To Retrieve ====')
            print(data)
            continue

        print(json.dumps(js, indent=4))

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        print('lat', lat, 'lng', lng)
        location = js['results'][0]['formatted_address']
        print(location)

        #Establish the locationContent variable using the js
        results = js['results'][0]
        locationContent = results["locationContent"]
        
        #Declare and initialize the countryExists boolean variable
        countryExists = False

        #Use try/except clause to print the two character country code of the location entered
        try:
            for unit in locationContent:
                types = unit["types"]
                #IF country and political appear in the location, then the location is in a country and countryExists is assigned the True boolean value
                if types == ["country", "political"]:
                    countryExists = True
                    print("The character county code is:", unit["short_name"])
            #If countryExists remains false, then not country was detected in the search and an exception is passed
            if not countryExists:
                raise Exception
        except:
            print("No country code exists for this entry.")

    
#Call the main() function
main()
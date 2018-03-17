import googlemaps

f = open("app/mapsapikey.txt", "r")
mapsapikey = f.read()
f.close()

gmaps = googlemaps.Client(key=mapsapikey)
geocode_result = gmaps.geocode('Manhattan Drive, Cambridge CB4')
print(geocode_result[0]['geometry']['location']['lat'])

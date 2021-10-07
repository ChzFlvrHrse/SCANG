import requests

GOOGLE_API_KEY = 'AIzaSyACfy1Gpj75UiBV-fa9NIfdhKCnskzZHvw'

def extract_lat_long(address_or_zipcode):
    formatted_address, lat, lng = None, None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None, None
    try:
        results = r.json()['results'][0]
        formatted_address = results['formatted_address']
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return formatted_address, lat, lng

#print(extract_lat_long(input("Enter Hunt Area: ",)))

sampleList = ["Alapaha River WMA", "Albany Nursery WMA", "Alexander WMA Georgia"]

latLongList =[]
for line in sampleList:
    toady = line, extract_lat_long(line)
    latLongList.append(toady)

for item in latLongList:
    print(item)

import requests
import json
import sys
import folium
import tkinter as tk
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

# Get the current location of the ISS
url = 'http://api.open-notify.org/iss-now.json'

try:
    response = requests.get(url)
    data = json.loads(response.text)
except requests.exceptions.RequestException as e:
    print("Error: Could not connect to API. Check your internet connection.")
    sys.exit(1)
except json.decoder.JSONDecodeError as e:
    print("Error: Invalid response from API. Check the API documentation.")
    sys.exit(1)

# Print the location
print('Latitude:', data['iss_position']['latitude'])
print('Longitude:', data['iss_position']['longitude'])
a = data['iss_position']['latitude']
b = data['iss_position']['longitude']
location = geolocator.reverse("{}, {}".format(a, b), timeout=10)

address = location.address

print(address)


def update_location():
    response = requests.get(url)
    data = json.loads(response.text)
    lat.config(text="Latitude: " + data['iss_position']['latitude'])
    lon.config(text="Longitude: " + data['iss_position']['longitude'])
    location = geolocator.reverse("{}, {}".format(data['iss_position']['latitude'], data['iss_position']['longitude']), timeout=10)
    address = location.address
    addr.config(text="Address: " + address)
def update_location():
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        lat.config(text="Latitude: " + data['iss_position']['latitude'])
        lon.config(text="Longitude: " + data['iss_position']['longitude'])
        location = geolocator.reverse("{}, {}".format(data['iss_position']['latitude'], data['iss_position']['longitude']), timeout=10)
        address = location.address
        if address:
            addr.config(text="Address: " + address)
        else:
            addr.config(text="Address: Not found")
    except Exception as e:
        print("Error: {}".format(str(e)))
        lat.config(text="Latitude: Not found")
        lon.config(text="Longitude: Not found")
        addr.config(text="Address: Not found")
# Create a map with the location of the ISS
map = folium.Map(location=[a, b], zoom_start=4)
folium.CircleMarker(location=[a, b], radius=15, color='red').add_to(map)


root = tk.Tk()
root.title("ISS Location")

lat = tk.Label(root, text="Latitude:")
lat.pack()

lon = tk.Label(root, text="Longitude:")
lon.pack()

addr = tk.Label(root, text="Address:")
addr.pack()

refresh_button = tk.Button(root, text="Refresh", command=update_location)
refresh_button.pack()

update_location()
root.mainloop()
root.after(20000, update_location)
root.mainloop()

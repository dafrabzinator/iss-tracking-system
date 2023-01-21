import requests
import json
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

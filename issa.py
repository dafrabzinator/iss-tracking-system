import requests
import json
import tkinter as tk
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import folium
import sys
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("iss.db")
cursor = conn.cursor()

# Create the table to store the location data
cursor.execute("""
CREATE TABLE IF NOT EXISTS location_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
)
""")
conn.commit()
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


# Get the latitude and longitude of the ISS
iss_latitude = float(data['iss_position']['latitude'])
iss_longitude = float(data['iss_position']['longitude'])
# Store the current location in the database
cursor.execute("""
INSERT INTO location_history (latitude, longitude)
VALUES (?, ?)
""", (iss_latitude, iss_longitude))
conn.commit()

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
        #store the new location in the database.
        cursor.execute("""
    INSERT INTO location_history (latitude, longitude)
    VALUES (?, ?)
    """, (iss_latitude, iss_longitude))
    conn.commit()    
    # Update the map with the new location of the ISS
    map = folium.Map(location=[iss_latitude, iss_longitude], zoom_start=2)
    folium.Marker(location=[iss_latitude, iss_longitude], popup="ISS").add_to(map)
    map.save("map.html")
# Retrieve the history of the location of the ISS
cursor.execute("""
SELECT * FROM location_history
ORDER BY timestamp
""")
location_history = cursor.fetchall()


# Create graphs and charts to show the historical location data of the ISS
fig, ax = plt.subplots()
ax.plot(iss_latitude, iss_longitude)
ax.set(xlabel='Latitude', ylabel='Longitude', title='Historical Location Data of the ISS')
ax.grid()
plt.savefig("iss_location_data.png")
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
root.geometry("500x500")
root.title("ISS Location Tracker")
root.config(background="#3c3f41")
root.after(2000, update_location)
root.mainloop()

# Use ttk widgets for a more attractive appearance
frame = tk.Frame(root, padding=10, relief="solid", borderwidth=2)
frame.pack(fill="both", expand=True)
frame.config(background="#3c3f41")

lat_label = tk.Label(frame, text="Latitude: ", font=("TkDefaultFont", 14), background="#3c3f41", foreground="white")
lat_label.pack(pady=10)

lon_label = tk.Label(frame, text="Longitude: ", font=("TkDefaultFont", 14), background="#3c3f41", foreground="white")
lon_label.pack(pady=10)

addr_label = tk.Label(frame, text="Address: ", font=("TkDefaultFont", 14), background="#3c3f41", foreground="white")
addr_label.pack(pady=10)
# Display the history of the location of the ISS
for location in location_history:
    print("Latitude: {}, Longitude: {}, Timestamp: {}".format(*location))

    conn.close()

# Add images to the GUI
img = tk.PhotoImage(file="iss_location_data.png")
img_label = tk.Label(frame, image=img)
img_label.pack(pady=10)

root.mainloop()
def refresh():
    # Code to update the database

    # Refresh the display
    root.update_idletasks()

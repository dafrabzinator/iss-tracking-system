# ISS Location Tracker

This is a python application that tracks the location of the International Space Station (ISS) and displays it in real-time. The location information includes the latitude, longitude, and address (when available) of the ISS. The location history is also stored in a SQLite database.

## Features
- Display the current latitude, longitude, and address (when available) of the ISS
- Store the location history of the ISS in a SQLite database
- Create a graph of the historical location data of the ISS using matplotlib
- Display the location of the ISS on a map using folium. see the [map](map.html).

## Requirements
- Python 3
- matplotlib
- folium
- geopy
- sqlite3
- requests
- tkinter
- json

## Usage
1. Clone the repository to your local machine. `git clone https://github.com/dafrabzinator/iss-tracking-system.git`
2. Run the issa.py file using `Python3 -m issa`.
3. The location information of the ISS will be displayed on a tkinter GUI.
4. The location history will be stored in the iss.db SQLite database.
5. The historical location data of the ISS will be displayed in a graph in the iss_location_data.png file.
6. The location of the ISS will be displayed on a map in the map.html file.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

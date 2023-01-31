import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# API endpoint to retrieve flight data
url = "https://flightxml.flightaware.com/json/FlightXML3/FlightRoute"

# API credentials
username = "your_username"
api_key = "your_api_key"

# Flight information
flight_number = "your_flight_number"

# API request parameters
params = {
    "ident": flight_number,
    "howMany": 1,
    "offset": 0
}

# Make API request
response = requests.get(url, auth=(username, api_key), params=params)

# Parse API response
data = response.json()

# Extract flight information
flight = data["FlightRouteResult"]["data"][0]

# Latitude and longitude coordinates of flight route
lats = [point["latitude"] for point in flight["route"]]
lons = [point["longitude"] for point in flight["route"]]

# Create map
map = Basemap(projection='mill',
              llcrnrlat=min(lats) - 5,
              urcrnrlat=max(lats) + 5,
              llcrnrlon=min(lons) - 5,
              urcrnrlon=max(lons) + 5,
              resolution='c')

# Plot flight route on map
map.scatter(lons, lats, latlon=True, c='r', marker='o')
map.drawcoastlines()

# Show map
plt.show()

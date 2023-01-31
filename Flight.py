import requests
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# API endpoint to retrieve flight data
url = "https://flightxml.flightaware.com/json/FlightXML3/FlightInfo"

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
flight = data["FlightInfoResult"]["flights"][0]

# Latitude and longitude coordinates of flight route
lats = [point["latitude"] for point in flight["latlons"]]
lons = [point["longitude"] for point in flight["latlons"]]

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

# Create flight report
doc = SimpleDocTemplate("flight_report.pdf", pagesize=landscape(letter))

# Flight details
flight_details = [
    ("Flight Number", flight_number),
    ("Altitude", str(flight["altitude"]) + " feet"),
    ("Speed", str(flight["groundspeed"]) + " knots"),
    ("Fuel Consumption", "-"),
    ("Time of Take Off", flight["filed_departuretime"]["time"]),
    ("Estimated Time of Landing", flight["estimatedarrivaltime"]["time"]),
    ("Take Off Point", flight["origin"]["airport_name"]),
    ("Destination", flight["destination"]["airport_name"]),
    ("Airplane Model", flight["aircrafttype"]),
    ("Capacity", "-")
]

# Create table for flight details
table = Table(flight_details)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
]))
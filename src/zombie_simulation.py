import folium
import random
import time
import threading
import pandas as pd
import numpy as np
from folium.plugins import HeatMap

# Initialize map centered on the US
us_map = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

# Load a dataset of major US cities (or generate random locations for infection points)
cities = [
    (34.0522, -118.2437),  # Los Angeles, CA
    (40.7128, -74.0060),   # New York, NY
    (41.8781, -87.6298),   # Chicago, IL
    (29.7604, -95.3698),   # Houston, TX
    (33.4484, -112.0740),  # Phoenix, AZ
    (39.7392, -104.9903),  # Denver, CO
    (32.7767, -96.7970),   # Dallas, TX
    (47.6062, -122.3321),  # Seattle, WA
    (42.3601, -71.0589),   # Boston, MA
    (38.9072, -77.0369),   # Washington, DC
    (37.7749, -122.4194),  # San Francisco, CA
    (36.1627, -86.7816),   # Nashville, TN
    (35.2271, -80.8431),   # Charlotte, NC
    (44.9778, -93.2650),   # Minneapolis, MN
    (45.5152, -122.6784),  # Portland, OR
    (25.7617, -80.1918),   # Miami, FL
    (39.9526, -75.1652),   # Philadelphia, PA
    (35.1495, -90.0490),   # Memphis, TN
    (36.1699, -115.1398),  # Las Vegas, NV
    (27.9506, -82.4572),   # Tampa, FL
    (32.7157, -117.1611),  # San Diego, CA
    (46.8787, -113.9966),  # Missoula, MT
    (30.2672, -97.7431),   # Austin, TX
]

# Simulation parameters
infection_radius = float(input("Enter infection radius (in degrees of latitude/longitude): "))  # Degrees of latitude/longitude
infection_rate = float(input("Enter infection rate (probability of spread per step): "))    # Probability of spreading
initial_infected = 3    # Number of initial outbreaks
iterations = 50         # Number of simulation steps

# Track infections
infected_points = set(random.sample(cities, initial_infected))

# Function to update infection spread
def spread_infection():
    global infected_points
    for _ in range(iterations):
        new_infections = set()
        for lat, lon in infected_points:
            for city in cities:
                if city not in infected_points and random.random() < infection_rate:
                    if abs(city[0] - lat) < infection_radius and abs(city[1] - lon) < infection_radius:
                        new_infections.add(city)
        infected_points.update(new_infections)
        time.sleep(0.5)  # Simulate time passing

# Start infection spread in a separate thread
threading.Thread(target=spread_infection, daemon=True).start()

# Function to generate map updates
def generate_map():
    while len(infected_points) < len(cities):
        us_map = folium.Map(location=[39.8283, -98.5795], zoom_start=5)
        HeatMap(infected_points).add_to(us_map)
        us_map.save("zombie_simulation.html")
        time.sleep(1)

# Start map updates
threading.Thread(target=generate_map, daemon=True).start()


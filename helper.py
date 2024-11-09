from typing import Dict, Any

import folium

def generate_route_map(route: Dict[str, Any]) -> folium.Map:
    # Initialize the map centered on the first point in the route
    base_map = folium.Map(location=route[0], zoom_start=12, tiles='Stamen Terrain')

    # Add the route as a polyline
    folium.PolyLine(locations=route, color="blue", weight=4, opacity=0.7).add_to(base_map)

    # Calculate the bounds of the route for proper map zooming
    route_bounds = base_map.get_bounds()

    # Adjust map view to fit the route bounds
    base_map.fit_bounds(route_bounds)

    return base_map

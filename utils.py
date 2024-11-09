import ast
import json
import os
import pprint
import urllib.parse
from typing import Dict, List, Any

import requests
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from langchain.tools import BaseTool

SEARCH_RADIUS = 80000  # Adjusted radius to change coverage slightly
FSQ_SEARCH_API = "https://api.foursquare.com/v3/places/search"
FSQ_DETAILS_API = "https://api.foursquare.com/v3/places/{}/tips"
BING_ROUTE_API = "http://dev.virtualearth.net/REST/V1/Routes/{}?"

class InterestLocator(BaseTool):
    """
    Tool for retrieving points of interest in a specified location. It provides descriptions for local attractions,
    eateries, and more, based on a precise area.
    """
    name = "Interest Locator"
    description = (
        "Utilize this tool to find places of interest in a specified area, such as a city or town. "
        "It should be used for retrieving points of interest only and not for detailed information like historical or "
        "religious significance. Only one location can be processed at a time. The input is 'location', a string representing "
        "the specific area to search within."
    )

    def _run(self, location: str) -> Dict[str, str]:
        """Performs a synchronous search for places of interest around the given location.

        Args:
            location (str): location input from the agent

        Returns:
            output (dict): Places of interest with descriptions
        """
        location_details = fetch_location_data(location)
        points_of_interest = fetch_places_of_interest(location_details.latitude, location_details.longitude, SEARCH_RADIUS)
        output = {"output": points_of_interest}
        return output

    def _arun(self, location: str):
        """Asynchronous support is not implemented.

        Args:
            location (str): location input from the agent
        """
        raise NotImplementedError("Asynchronous operation is not supported for this tool.")


def fetch_places_of_interest(latitude: float, longitude: float, radius: int) -> str:
    """Finds places of interest around the given latitude and longitude within a specified radius.

    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
        radius (int): Search radius in meters

    Returns:
        points_info (str): Concise descriptions of nearby points of interest
    """
    try:
        api_key = os.getenv('FSQ_API_KEY')
        if not api_key:
            raise ValueError("Foursquare API key is required")

        headers = {
            "accept": "application/json",
            "Authorization": api_key
        }
        params = {
            "ll": f"{latitude},{longitude}",
            "radius": radius,
            "sort": "DISTANCE",
            "limit": 8
        }
        response = requests.get(FSQ_SEARCH_API, headers=headers, params=params)
        response.raise_for_status()
        
        places = response.json().get('results', [])
        points_info = '\n'.join(compile_place_info(place['name'], place['fsq_id']) for place in places)
        return points_info
    except Exception as error:
        print(f"Error while fetching places of interest: {error}")
        return "No information available."


def fetch_location_data(location: str) -> Nominatim:
    """Uses the Nominatim geocoder to fetch latitude and longitude details for a location.

    Args:
        location (str): Specified location

    Returns:
        location_details (Nominatim): Geopy location details
    """
    location = location.strip("location=")
    geolocator = Nominatim(user_agent="interest_locator_tool")
    rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    try:
        location_details = rate_limiter(location)
        if location_details:
            return location_details
        else:
            raise ValueError("Location not found. Please specify a more precise query.")
    except Exception as exc:
        print(f"Error during geocoding: {exc}")
        raise


def compile_place_info(name: str, fsq_id: str) -> str:
    """Gathers additional details for a specific place using Foursquare.

    Args:
        name (str): Name of the location
        fsq_id (str): Unique Foursquare ID for the location

    Returns:
        info (str): Description of the location's points of interest
    """
    try:
        url = FSQ_DETAILS_API.format(fsq_id)
        api_key = os.getenv('FSQ_API_KEY')
        if not api_key:
            raise ValueError("Foursquare API key is required")
        
        headers = {
            "accept": "application/json",
            "Authorization": api_key
        }
        response = requests.get(url, headers=headers, params={"sort": "POPULAR", "limit": 3})
        response.raise_for_status()
        
        tips = response.json()
        info = name + ': ' + ' '.join(tip.get('text', '') for tip in tips)
        return info
    except Exception as error:
        print(f"Error retrieving place information: {error}")
        return f"{name}: No further information available."


class RoutePathfinder(BaseTool):
    name = "Route Pathfinder"
    description = (
        "Use this tool to generate travel routes based on input locations and transportation modes. "
        "Accepts a dictionary 'input_data' with keys 'locations' (a list of location names) and 'transport_mode' "
        "(a string indicating the mode of transport, e.g., 'car', 'walking', 'transit'). "
        "Example usage: {'locations': ['Delhi', 'Agra'], 'transport_mode': 'car'}. "
        "Returns step-by-step directions for travel across the locations."
    )

    def _run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(input_data, str):
            input_data = ast.literal_eval(input_data)
        transport_mode = self.get_transport_mode(input_data.get('transport_mode', 'driving'))
        locations = input_data.get('locations', [])
        route = generate_route(locations, transport_mode)
        return route

    def _arun(self, locations: List[str], transport_mode: str) -> None:
        raise NotImplementedError("Asynchronous operations are unsupported.")

    @staticmethod
    def get_transport_mode(transport_mode: str) -> str:
        transport_mode = transport_mode.lower().strip()
        if 'walk' in transport_mode:
            return 'Walking'
        elif 'bike' in transport_mode or 'cycle' in transport_mode:
            return 'Bicycling'
        elif 'transit' in transport_mode or 'bus' in transport_mode or 'train' in transport_mode:
            return 'Transit'
        else:
            return 'Driving'


def generate_route(locations: List[str], mode: str) -> Dict[str, Any]:
    api_key = os.getenv('BING_API_KEY')
    if not api_key:
        raise ValueError("Bing Maps API key is required")

    route_url = BING_ROUTE_API.format(mode)
    for index, location in enumerate(locations):
        encoded_location = urllib.parse.quote(location, safe='')
        route_url += f"&wp.{index}=" + encoded_location

    route_url += "&key=" + api_key
    print("Requesting route from URL:", route_url)

    try:
        response = requests.get(route_url)
        response.raise_for_status()
        
        route_data = response.json()
        itinerary = route_data["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]
        directions = ["- " + item["instruction"]["text"] for item in itinerary]
        geo_points = [item["maneuverPoint"]["coordinates"] for item in itinerary]
        
        route = {"output": '\n'.join(directions), 'geocode_points': geo_points}
        return route
    except Exception as error:
        raise ConnectionError(f"Route retrieval error: {error}")

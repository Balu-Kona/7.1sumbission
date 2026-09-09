import json
import os


class ResearchAgent:
    def __init__(self):
        self.name = "Research Agent"

    def load_data(self, filename):
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "data", filename)

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def normalize_destination(self, destination):
        destination = destination.lower().strip()

        if "hersh" in destination:
            return "Hershey"

        if "orlando" in destination:
            return "Orlando"

        return destination.title()

    def research(self, plan):
        attractions = self.load_data("attractions.json")
        hotels = self.load_data("hotels.json")
        transportation = self.load_data("transportation.json")
        restaurants = self.load_data("restaurants.json")

        destination = self.normalize_destination(plan["destination"])

        matching_attractions = [
            attraction
            for attraction in attractions
            if attraction.get("destination") == destination
        ]

        matching_hotels = [
            hotel
            for hotel in hotels
            if hotel.get("destination") == destination
        ]

        matching_restaurants = [
            restaurant
            for restaurant in restaurants
            if restaurant.get("destination") == destination
        ]

        results = {
            "destination": destination,
            "attractions": matching_attractions,
            "hotels": matching_hotels,
            "restaurants": matching_restaurants,
            "transportation": transportation
        }

        return results

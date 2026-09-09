class ItineraryAgent:
    def __init__(self):
        self.name = "Itinerary Agent"

    def create_itinerary(self, plan, research, budget):
        attractions = research["attractions"]
        restaurants = research.get("restaurants", [])

        interests = " ".join(
            plan.get("interests", [])
        ).lower()

        preferences = " ".join(
            plan.get("preferences", [])
        ).lower()

        food_preferences = f"{interests} {preferences}"
        matching_restaurants = [
            restaurant for restaurant in restaurants
            if restaurant.get("cuisine", "").lower() in food_preferences
        ]

        if not matching_restaurants:
            matching_restaurants = [
                restaurant for restaurant in restaurants
                if restaurant.get("family_friendly", False)
            ]

        restaurant = matching_restaurants[0] if matching_restaurants else None

        # Find activities matching the user's interests.
        selected = []

        if "theme" in interests or "park" in interests:
            theme_parks = [
                a for a in attractions
                if a["type"] == "theme park"
            ]

            if theme_parks:
                selected.append(theme_parks[0])

        if "zoo" in interests:
            zoos = [
                a for a in attractions
                if a["type"] == "zoo"
            ]

            if zoos:
                selected.append(zoos[0])

        # Add family-friendly activities that are not already selected.
        family_activities = [
            a for a in attractions
            if a["family_friendly"]
            and a not in selected
            and a.get("driving_time_minutes", 0) <= 45
        ]

        for activity in family_activities:
            if len(selected) >= 3:
                break

            selected.append(activity)

        itinerary = [
            {
                "day": "Day 1",
                "activities": [
                    "Arrive in " + research["destination"],
                    "Check in at " + budget["hotel"],
                    "Relax and explore the local area"
                ]
            }
        ]

        day_number = 2

        for activity in selected[:3]:
            activities = [
                "Visit " + activity["name"],
                "Family-friendly activities",
                "Free time for relaxation"
            ]

            # Add a restaurant that matches the user's cuisine preference.
            if restaurant is not None and day_number == 3:
                activities.insert(
                    1,
                    "Dinner at " + restaurant["name"]
                )

            itinerary.append(
                {
                    "day": f"Day {day_number}",
                    "activities": activities
                }
            )

            day_number += 1

        itinerary.append(
            {
                "day": "Day 5",
                "activities": [
                    "Relaxing morning",
                    "Check out of hotel",
                    "Depart " + research["destination"]
                ]
            }
        )

        return itinerary

class TravelPlanner:
    def __init__(self):
        self.name = "Travel Planner Agent"

    def create_plan(self, request):
        """
        Extract basic travel requirements from the user's request.
        """

        plan = {
            "destination": request.get("destination"),
            "dates": request.get("dates"),
            "travelers": request.get("travelers"),
            "budget": request.get("budget"),
            "interests": request.get("interests", []),
            "preferences": request.get("preferences", []),
        }

        return plan
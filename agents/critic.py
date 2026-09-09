class CriticAgent:
    def __init__(self):
        self.name = "Critic Agent"

    def review(self, plan, research, budget, itinerary):

        issues = []
        recommendations = []

        # Check budget
        if not budget["within_budget"]:
            issues.append("Trip is over the user's budget.")
            recommendations.append(
                "Choose a lower-cost hotel or reduce paid activities."
            )

        # Check driving time
        for attraction in research["attractions"]:
            if attraction["name"] in str(itinerary):
                if attraction.get("driving_time_minutes", 0) > 45:
                    issues.append(
                        f"{attraction['name']} requires significant driving."
                    )
                    recommendations.append(
                        "Consider replacing it with a closer activity."
                    )

        # Check relaxation preference
        relaxation_found = any(
            "relax" in str(day).lower()
            for day in itinerary
        )

        if not relaxation_found:
            issues.append(
                "The itinerary does not include enough relaxation time."
            )
            recommendations.append(
                "Add free time between major activities."
            )

        # Check family-friendly requirement
        for attraction in research["attractions"]:
            if attraction["name"] in str(itinerary):
                if not attraction.get("family_friendly", False):
                    issues.append(
                        f"{attraction['name']} may not match the "
                        "family-friendly requirement."
                    )

        if not issues:
            status = "APPROVED"
        else:
            status = "NEEDS REVISION"

        return {
            "status": status,
            "issues": issues,
            "recommendations": recommendations
        }
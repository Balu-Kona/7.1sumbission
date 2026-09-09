import re
from datetime import date, datetime, timedelta


class BudgetAgent:
    def __init__(self):
        self.name = "Budget Agent"

    def calculate_nights(self, dates):
        """Return the number of nights in a date range such as 'June 10 - June 14'."""
        parts = re.split(r"\s*(?:-|–|to|through|until)\s*", dates.strip(), maxsplit=1, flags=re.IGNORECASE)
        if len(parts) != 2:
            raise ValueError(
                "Dates must be a range such as 'June 10 - June 14'."
            )

        start_text, end_text = [part.strip().replace(",", "") for part in parts]
        default_year = 2026

        def parse_endpoint(text, inherited_month=None):
            formats = ("%B %d %Y", "%b %d %Y", "%B %d", "%b %d")
            for fmt in formats:
                try:
                    parsed = datetime.strptime(text, fmt)
                    return parsed.date().replace(year=parsed.year or default_year)
                except ValueError:
                    pass

            if inherited_month and text.isdigit():
                return datetime.strptime(
                    f"{inherited_month} {text}", "%B %d"
                ).date().replace(year=default_year)

            raise ValueError(
                f"Could not understand date '{text}'. Use a format like 'June 10 - June 14'."
            )

        start = parse_endpoint(start_text)
        inherited_month = start.strftime("%B")
        end = parse_endpoint(end_text, inherited_month)

        if end <= start:
            end = end.replace(year=end.year + 1)

        return (end - start).days

    def calculate(self, plan, research):
        travelers = int(plan["travelers"])
        nights = self.calculate_nights(plan["dates"])
        travel_days = nights + 1

        # Choose the lowest-cost family-friendly hotel
        hotel = min(
            research["hotels"],
            key=lambda x: x["nightly_rate"]
        )

        # Choose rental car
        transportation = next(
            item for item in research["transportation"]
            if item["type"] == "Rental Car"
        )

        hotel_cost = hotel["nightly_rate"] * nights
        transportation_cost = transportation["daily_cost"] * travel_days

        # Start with one theme park day
        theme_park = next(
            item for item in research["attractions"]
            if item["type"] == "theme park"
        )

        attraction_cost = theme_park["price_per_person"] * travelers

        estimated_total = (
            hotel_cost
            + transportation_cost
            + attraction_cost
        )

        remaining_budget = plan["budget"] - estimated_total

        return {
            "hotel": hotel["name"],
            "nights": nights,
            "hotel_cost": hotel_cost,
            "transportation": transportation["type"],
            "travel_days": travel_days,
            "transportation_cost": transportation_cost,
            "main_attraction": theme_park["name"],
            "attraction_cost": attraction_cost,
            "estimated_total": estimated_total,
            "remaining_budget": remaining_budget,
            "within_budget": estimated_total <= plan["budget"]
        }

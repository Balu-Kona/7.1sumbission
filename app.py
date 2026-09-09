from agents.planner import TravelPlanner
from agents.research import ResearchAgent
from agents.budget import BudgetAgent
from agents.itinerary import ItineraryAgent
from agents.critic import CriticAgent
from memory.memory import TravelMemory


def prompt_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def prompt_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number > 0:
                return number
        except ValueError:
            pass
        print("Please enter a positive whole number.")


def prompt_nonnegative_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if number >= 0:
                return number
        except ValueError:
            pass
        print("Please enter a valid non-negative budget.")


def main():
    planner = TravelPlanner()

    print("\n=== TRIP REQUEST ===")

    destination = prompt_required("Where do you want to go? ")
    dates = prompt_required("What are your travel dates? ")
    travelers = prompt_positive_int("How many people are traveling? ")
    budget = prompt_nonnegative_float("What is your total budget? $ ")

    interests_input = input(
        "What are your interests? (separate with commas) "
    )

    preferences_input = input(
        "Any preferences? (separate with commas) "
    )

    travel_request = {
        "destination": destination,
        "dates": dates,
        "travelers": travelers,
        "budget": budget,
        "interests": [
            item.strip()
            for item in interests_input.split(",")
        ],
        "preferences": [
            item.strip()
            for item in preferences_input.split(",")
        ]
    }

    memory = TravelMemory()

    memory.save_preferences({
        "family_friendly": True,
        "avoid_long_drives": True,
        "include_relaxation": True
    })

    plan = planner.create_plan(travel_request)
    research_agent = ResearchAgent()
    research = research_agent.research(plan)

    if not research["attractions"]:
        print(
            f"\nNo attraction data was found for '{destination}'. "
            "Please try Orlando or Hershey."
        )
        return

    if not research["hotels"]:
        print(
            f"\nNo hotel data was found for '{destination}'. "
            "Please try Orlando or Hershey."
        )
        return

    print("\n=== AI TRAVEL PLANNING AGENT ===\n")

    print("Destination:", plan["destination"])
    print("Dates:", plan["dates"])
    print("Travelers:", plan["travelers"])
    print("Budget: $", plan["budget"])

    print("\nInterests:")
    for interest in plan["interests"]:
        print("-", interest)

    print("\nPreferences:")
    for preference in plan["preferences"]:
        print("-", preference)

    print("\n=== RESEARCH RESULTS ===")

    print("\nAttractions:")
    for attraction in research["attractions"]:
        print(
            f"- {attraction['name']} "
            f"(${attraction['price_per_person']} per person)"
        )

    print("\nHotels:")
    for hotel in research["hotels"]:
        print(
            f"- {hotel['name']} "
            f"(${hotel['nightly_rate']}/night)"
        )

    print("\nTransportation:")
    for transport in research["transportation"]:
        print(
            f"- {transport['type']} "
            f"(${transport['daily_cost']}/day)"
        )

    print("\nRestaurants:")

    for restaurant in research["restaurants"]:
        print(
            f"- {restaurant['name']} "
            f"({restaurant['cuisine']}, "
            f"{restaurant['price_level']})"
        )

    budget_agent = BudgetAgent()
    try:
        budget = budget_agent.calculate(plan, research)
    except ValueError as error:
        print(f"\nUnable to calculate the trip budget: {error}")
        return

    print("\n=== BUDGET ANALYSIS ===")

    print("Hotel:", budget["hotel"])
    print("Nights:", budget["nights"])
    print("Hotel cost: $", budget["hotel_cost"])

    print("Transportation:", budget["transportation"])
    print("Transportation cost: $", budget["transportation_cost"])

    print("Main attraction:", budget["main_attraction"])
    print("Attraction cost: $", budget["attraction_cost"])

    print("\nEstimated total: $", budget["estimated_total"])
    print("Remaining budget: $", budget["remaining_budget"])

    if budget["within_budget"]:
        print("Status: WITHIN BUDGET")
    else:
        print("Status: OVER BUDGET")

    itinerary_agent = ItineraryAgent()
    itinerary = itinerary_agent.create_itinerary(
        plan,
        research,
        budget
    )

    print("\n=== PROPOSED ITINERARY ===")

    for day in itinerary:
        print(f"\n{day['day']}")

        for activity in day["activities"]:
            print("-", activity)

    critic_agent = CriticAgent()

    critique = critic_agent.review(
        plan,
        research,
        budget,
        itinerary
    )

    print("\n=== CRITIC REVIEW ===")

    print("Status:", critique["status"])

    if critique["issues"]:
        print("\nIssues:")
        for issue in critique["issues"]:
            print("-", issue)

    if critique["recommendations"]:
        print("\nRecommendations:")
        for recommendation in critique["recommendations"]:
            print("-", recommendation)

    # Revision loop
    if critique["status"] == "NEEDS REVISION":
        print("\n=== REVISION LOOP ===")
        print("Critic found an issue.")
        print("Rebuilding itinerary based on user preferences...")

        itinerary = itinerary_agent.create_itinerary(
            plan,
            research,
            budget
        )

        critique = critic_agent.review(
            plan,
            research,
            budget,
            itinerary
        )

        print("\n=== REVISED ITINERARY ===")

        for day in itinerary:
            print(f"\n{day['day']}")

            for activity in day["activities"]:
                print("-", activity)

        print("\n=== FINAL CRITIC REVIEW ===")
        print("Status:", critique["status"])

    print("\n=== TRAVEL MEMORY ===")

    saved_preferences = memory.get_preferences()

    for key, value in saved_preferences.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()

# AI Travel Planning Agent

This is my capstone project for building a small travel-planning agent. The idea is to help someone turn a few travel preferences into a simple itinerary. For example, a user can enter a destination, dates, number of travelers, budget, interests, and preferences such as family-friendly activities, short driving times, or Indian food.

This is a learning prototype, not a real booking service. The travel information in the JSON files is public or synthetic sample data. It does not provide live prices or availability.

## Why I built it

Travel planning is more complicated than asking for one recommendation. A useful plan has to combine attractions, hotels, transportation, food, cost, and the user’s preferences. My goal was to split those responsibilities across a few small agents so that each part could be checked separately.

## How the pieces work together

The basic flow is:

```text
User request
    ↓
Planner Agent
    ↓
Research Agent + Travel Memory
    ↓
Budget Agent
    ↓
Itinerary Agent
    ↓
Critic Agent
    ↓
Final itinerary
```

The agents have these responsibilities:

- **Planner Agent:** Organizes the user’s answers into a structured travel request.
- **Research Agent:** Finds attractions, hotels, transportation, and restaurants in the local JSON data. It also understands that “Hershys” means Hershey.
- **Budget Agent:** Calculates hotel cost, transportation cost, attraction cost, number of nights, and the amount left in the budget.
- **Itinerary Agent:** Uses the user’s interests and preferences to select activities. It can also add a matching restaurant, such as an Indian restaurant.
- **Critic Agent:** Reviews the itinerary for budget problems, long drives, family suitability, and relaxation time.
- **Travel Memory:** Stores general preferences used during the planning session.

If the critic finds a problem, the app has a revision step that rebuilds and checks the itinerary again.

## Running the project

The project uses the Python standard library, so no special package installation is needed right now.

```bash
cd FInal_sumbission/AI-Travel-Planning-Agent
python3 app.py
```

The program asks questions in the terminal. One example request is:

```text
Where do you want to go? Hershys, Pennsylvania
What are your travel dates? June 10 - June 14
How many people are traveling? 4
What is your total budget? $ 2000
What are your interests? theme parks and zoo
Any preferences? kids friendly and indian food
```

For this request, the research step normalizes the destination to Hershey, selects Hershey attractions and hotels, and the itinerary includes Hersheypark, ZooAmerica, and an Indian restaurant.

## Running the evaluation

The evaluation cases cover both Hershey and Orlando. They check destination filtering, hotel and attraction selection, restaurant matching, budget limits, and critic approval.

```bash
python3 evaluation/run_evaluation.py
```

The current result is:

```text
Evaluation result: 2/2 cases passed
```

## Limitations and next improvements

The data is only sample data, so the app should not be used to make real bookings. It does not connect to live flight, hotel, weather, or map APIs yet. It also supports only a small number of destinations and has basic date parsing.

My next improvements would be adding live retrieval tools, more destinations, better hotel preference matching, a larger evaluation set, and a more persistent memory system. Any final recommendation should still be reviewed by a person, especially for current prices, schedules, accessibility information, and travel advisories.

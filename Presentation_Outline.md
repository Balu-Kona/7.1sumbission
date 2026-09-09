# AI Travel Planning Agent — Presentation Outline

## Slide 1 — Title

**AI Travel Planning Agent**

Capstone project by Balamurali Konathala

Briefly say that this project creates a personalized sample itinerary from a user’s destination, dates, budget, interests, and preferences.

## Slide 2 — The Problem

- Travel planning requires comparing many details.
- Users care about cost, activities, transportation, food, and schedule.
- A basic chatbot may ignore constraints or use the wrong information.

Explain that the goal is to make the planning process more organized and easier to review.

## Slide 3 — Example User Request

Show the test request:

```text
Destination: Hershys, Pennsylvania
Travelers: 4
Budget: $2,000
Interests: theme parks and zoo
Preferences: kids friendly and Indian food
```

Point out that the system recognizes “Hershys” as Hershey and uses the other details when creating the plan.

## Slide 4 — System Architecture

Show this flow:

```text
User → Planner → Research + Memory → Budget
                          ↓
                    Itinerary → Critic
                          ↓
                    Final plan or revision
```

Explain that each agent has one main responsibility.

## Slide 5 — Agent Roles

- Planner: structures the request.
- Research: retrieves destination data.
- Budget: calculates estimated costs.
- Itinerary: chooses activities and restaurants.
- Critic: checks the plan and recommends revisions.
- Memory: stores session preferences.

Keep this slide focused on the division of work.

## Slide 6 — Retrieval and Personalization

Explain that the Research Agent filters attractions and hotels by destination. It also retrieves restaurants.

For the Hershey example, the system returns:

- Hersheypark
- ZooAmerica
- Hershey hotels
- Hershey Indian Kitchen

The itinerary changes because the user asked for theme parks, a zoo, and Indian food.

## Slide 7 — Budget and Final Itinerary

Show the results:

```text
Hotel: Hershey Budget Motel
Nights: 4
Estimated total: $1,015
Remaining budget: $985
Status: WITHIN BUDGET
```

Then show that the itinerary includes Hersheypark, ZooAmerica, and dinner at Hershey Indian Kitchen.

## Slide 8 — Critic and Reliability

Explain that the critic checks:

- Budget
- Driving time
- Family suitability
- Relaxation time

If a problem is found, the system rebuilds and reviews the itinerary again. The current Hershey test ended with:

```text
Status: APPROVED
```

## Slide 9 — Evaluation Results

The project includes two automated evaluation cases:

- Hershey preference-aware trip
- Orlando destination filtering

Result:

```text
2/2 cases passed
```

Mention that the tests check destination normalization, retrieval, hotel and attraction selection, restaurant matching, budget, and critic approval.

## Slide 10 — Limitations and Next Steps

Current limitations:

- Sample JSON data instead of live APIs
- Only two destinations
- Basic hotel matching
- Session-only memory

Future work:

- Live weather, map, and booking information
- More destinations and evaluation cases
- Persistent user-approved memory
- More itinerary alternatives and stronger comparison

End by explaining that a person should confirm live travel information before booking.

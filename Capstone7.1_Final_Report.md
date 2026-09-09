# AI Travel Planning Agent

## Project Summary

For my capstone project, I built an AI Travel Planning Agent. The purpose of the project is to help a person create a basic trip plan without searching through several different websites by hand. The user enters a destination, travel dates, number of travelers, budget, interests, and preferences. The program then finds matching sample travel information, estimates the cost, creates an itinerary, and checks the itinerary for problems.

I chose travel planning because it is a problem with several parts. A person may care about the price of a hotel, the type of activities, driving time, food preferences, and whether an activity is appropriate for children. These requirements can easily conflict with each other. My project is a small demonstration of how different agents can divide this work.

This is a learning prototype, not a real travel-booking application. The information in the data files is public or synthetic sample information. The program does not check live prices, book reservations, or guarantee that an attraction is open.

## Problem and Goal

The problem is that travel planning takes time and requires comparing information from different sources. A regular language model could write a nice-looking itinerary, but it could also ignore a budget, recommend activities in the wrong city, or make up information. My goal was to create a system that keeps the travel requirements organized and checks its own recommendations before showing them.

The current version supports Orlando and Hershey as demonstration destinations. It can retrieve attractions, hotels, transportation options, and restaurants from local JSON files. It can also understand that a user who types “Hershys, Pennsylvania” probably means Hershey.

## How the System Works

The application follows this general process:

```text
User input
    ↓
Planner Agent
    ↓
Research Agent and Travel Memory
    ↓
Budget Agent
    ↓
Itinerary Agent
    ↓
Critic Agent
    ↓
Final itinerary or revision
```

The **Planner Agent** takes the answers from the terminal and puts them into a structured plan. This gives the rest of the program consistent fields for the destination, dates, number of travelers, budget, interests, and preferences.

The **Research Agent** reads the data files and returns information for the requested destination. It filters attractions and hotels so that a Hershey trip does not accidentally receive Orlando hotels. It also returns transportation and restaurant choices. The destination normalization step handles common spelling variations such as “Hershys.”

The **Budget Agent** chooses a lower-cost hotel and rental-car option from the available sample data. It calculates the number of nights from the dates, calculates transportation days, estimates attraction costs for the number of travelers, and shows the remaining budget.

The **Itinerary Agent** uses the user’s interests instead of always selecting the same activities. If the user mentions theme parks, it looks for a theme park. If the user mentions a zoo, it looks for a zoo. It also avoids activities that require more than 45 minutes of driving. When the user asks for Indian food, it adds a matching Indian restaurant to the itinerary.

The **Critic Agent** reviews the proposed plan. It checks whether the budget is exceeded, whether an activity requires too much driving, whether the itinerary has relaxation time, and whether selected attractions are family-friendly. If the critic finds a problem, the application rebuilds the itinerary and reviews it again.

The **Travel Memory** component stores preferences for the current session. The current examples include family-friendly travel, avoiding long drives, and including relaxation. This is simple in-memory storage and is not a permanent database.

## Retrieval and Data

The project uses local JSON files as a simple retrieval layer. There are separate files for attractions, hotels, transportation, and restaurants. Each record has details that later agents can use, such as destination, price, type, family suitability, rating, cuisine, and driving time.

For example, when the user enters “Hershys, Pennsylvania,” the Research Agent changes that value to “Hershey.” It then returns Hersheypark, ZooAmerica, Hershey’s Chocolate World, Hershey Gardens, Hershey hotels, and Hershey restaurants. Orlando records are not included in those results.

This is not yet a production vector database or a live web search system. It is a smaller and more understandable version for demonstrating the architecture. A future version could store public travel documents as embeddings and use semantic search. Live services could be added for weather, maps, current prices, transportation schedules, and travel advisories.

## How the Design Changed

At the beginning, I described the project as a general travel assistant. As the modules continued, I added more structure to it. First, I separated planning, research, budgeting, itinerary creation, and review into different agents. Then I added retrieval so the system would return information for the correct destination instead of returning every record.

I added memory to keep track of travel preferences during a session. I changed the itinerary logic so it uses interests such as theme parks and zoos. I then added restaurant data so a preference such as Indian food affects the actual itinerary instead of only being displayed as text.

The current system uses a mostly sequential workflow with a review and revision step. I considered a full Tree-of-Thought design with many competing itineraries, but I decided that the simpler review loop was a better fit for this prototype. It is easier to follow and does not create unnecessary extra model calls. A future version could generate several complete plans and compare them with a scoring rubric.

## Evaluation

I created two test cases in `evaluation/test_cases.json` and ran them using `evaluation/run_evaluation.py`.

The first test uses this type of request: Hershys, Pennsylvania; four travelers; a $2,000 budget; theme parks and zoo interests; and an Indian food preference. The test checks destination normalization, Hershey-specific attractions and hotels, Indian restaurant selection, budget compliance, and critic approval.

The second test uses Orlando and checks that the results contain Orlando attractions and hotels instead of Hershey information.

The current result is:

```text
Evaluation result: 2/2 cases passed
```

For the Hershey test, the estimated total is $1,015 and the amount left in the sample budget is $985. The final critic status is `APPROVED`.

## Safety and Limitations

I used only public or synthetic sample information in this project. The application does not collect sensitive personal information and does not make reservations. It should not be used as the final authority for travel decisions. A user should confirm prices, opening hours, accessibility information, transportation schedules, and travel advisories before booking anything.

The program now checks several invalid situations. It asks the user to enter a non-empty destination and date range, a positive traveler count, and a valid budget. It also gives a message when it cannot find data for a destination instead of failing with an error.

There are still limitations. The data covers only two destinations, the hotel selection is basic, and the memory disappears when the program closes. The restaurant data is very small. The project also does not connect to live APIs and does not yet compare several complete itinerary choices.

For future work, I would add live retrieval tools, more destinations, persistent user-approved memory, better hotel preference matching, more complete date handling, and additional evaluation cases. I would also add a final confirmation step so the user can approve or change the itinerary before it is treated as complete.

## Running the Project

From the project directory, run:

```bash
python3 app.py
```

To run the evaluation:

```bash
python3 evaluation/run_evaluation.py
```

GitHub repository: https://github.com/Balu-Kona/7.1sumbission

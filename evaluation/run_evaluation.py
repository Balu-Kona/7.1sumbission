import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.budget import BudgetAgent
from agents.critic import CriticAgent
from agents.itinerary import ItineraryAgent
from agents.planner import TravelPlanner
from agents.research import ResearchAgent


TEST_CASES = PROJECT_ROOT / "evaluation" / "test_cases.json"


def run_case(case):
    plan = TravelPlanner().create_plan(case["request"])
    research = ResearchAgent().research(plan)
    budget = BudgetAgent().calculate(plan, research)
    itinerary = ItineraryAgent().create_itinerary(plan, research, budget)
    critique = CriticAgent().review(plan, research, budget, itinerary)

    itinerary_text = str(itinerary)
    checks = {
        "destination": research["destination"] == case["expected_destination"],
        "hotel": budget["hotel"] == case["expected_hotel"],
        "attractions": all(
            attraction in [item["name"] for item in research["attractions"]]
            for attraction in case["expected_attractions"]
        ),
        "budget": budget["estimated_total"] <= case["max_estimated_total"],
        "critic": critique["status"] == "APPROVED",
    }

    if case.get("expected_restaurant"):
        checks["restaurant"] = case["expected_restaurant"] in itinerary_text

    passed = all(checks.values())
    return passed, checks, budget, critique


def main():
    cases = json.loads(TEST_CASES.read_text(encoding="utf-8"))
    passed_count = 0

    for case in cases:
        passed, checks, budget, critique = run_case(case)
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {case['name']}")
        for name, result in checks.items():
            print(f"  {'✓' if result else '✗'} {name}")
        print(f"  estimated total: ${budget['estimated_total']}")
        print(f"  critic status: {critique['status']}")
        if passed:
            passed_count += 1

    print(f"\nEvaluation result: {passed_count}/{len(cases)} cases passed")
    return 0 if passed_count == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())

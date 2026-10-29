from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

class State(TypedDict):
    user_request: str
    destination_info: str
    food_info: str
    budget_info: str
    final_plan: str

def destination_agent(state: State):
    prompt = [
        SystemMessage(
            content="""
            You are a destination travel assistant.
            Analyze the destination and recommend interesting attractions and activities.
            Focus only on destinations and activities.
            """
        ),
        HumanMessage(content=state["user_request"])
    ]
    response = llm.invoke(prompt)

    return {
        "destination_info": response.text
    }

def food_agent(state: State):
    prompt = [
        SystemMessage(
            content="""
            You are a food travel assistant.
            Recommend local dishes and places to eat based on the user's budget and preferences.
            Focus only on food and dining.
            """
        ),
        HumanMessage(content=state["user_request"])
    ]
    response = llm.invoke(prompt)

    return {
        "food_info": response.text
    }

def budget_agent(state: State):
    prompt = [
        SystemMessage(
            content="""
            You are a travel budget assistant.
            Estimate costs for accommodation, food, transportation, and activities.
            Consider the user's trip duration and budget.
            """
        ),
        HumanMessage(content=state["user_request"])
    ]
    response = llm.invoke(prompt)

    return {
        "budget_info": response.text
    }
def planner_agent(state: State):
    prompt = [
        SystemMessage(
            content="""
            You are a master travel planner. 
            Combine the destination info, food recommendations, and budget details into a cohesive final travel plan.
            """
        ),
        HumanMessage(
            content=f"""
            User request: {state['user_request']}
            Destination information: {state['destination_info']}
            Food recommendations: {state['food_info']}
            Budget information: {state['budget_info']}
            """
        )
    ]
    response = llm.invoke(prompt)
    return {
        "final_plan": response.text
    }

builder = StateGraph(State)

builder.add_node("destination_agent", destination_agent)
builder.add_node("food_agent", food_agent)
builder.add_node("budget_agent", budget_agent)
builder.add_node("planner_agent", planner_agent)

builder.add_edge(START, "destination_agent")
builder.add_edge(START, "food_agent")
builder.add_edge(START, "budget_agent")

builder.add_edge("destination_agent", "planner_agent")
builder.add_edge("food_agent", "planner_agent")
builder.add_edge("budget_agent", "planner_agent")
builder.add_edge("planner_agent", END)

graph = builder.compile()

result = graph.invoke({
    "user_request": "Plan a 3-day trip to Rome with a moderate budget.",
    "destination_info": "",
    "food_info": "",
    "budget_info": "",
    "final_plan": ""
})

print(result["final_plan"])


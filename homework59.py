from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

MODEL = "gemini-3.5-flash-lite"
MAX_ATTEMPTS = 3

llm = ChatGoogleGenerativeAI(
    model=MODEL
)

class State(TypedDict):
    ingredients: str
    recipe: str
    feedback: str
    approved: bool
    attempts: int

def generate_recipe(state: State):
    prompt = f"""
    Create a simple recipe using these ingredients: {state['ingredients']}.
    Include ingredient quantities, preparation steps, and cooking time.
    Write the recipe in English.
    """

    response = llm.invoke(prompt)

    return{
        "recipe": response.text
    }

def check_recipe(state: State):
    prompt = f"""
    Check whether this recipe uses the required ingredients, has clear steps, reasonable quantities, and cooking time.
    Recipe: {state['recipe']}
    Return APPROVED: YES or NO and FEEDBACK: followed by a short explanation.
    """

    response = llm.invoke(prompt)
    text = response.text.strip()

    approved = "YES" in text
    return{
        "feedback": text,
        "approved": approved,
        "attempts": state["attempts"] + 1
        }
def improve_recipe(state: State):
    prompt = f"""
    Improve this recipe based on the feedback.
    Ingredients: {state['ingredients']}
    Current Recipe: {state['recipe']}
    Feedback: {state['feedback']}
    
    Provide the updated complete recipe.
    """
    response = llm.invoke(prompt)

    return{
        "recipe": response.text
    }

def should_continue(state: State):
    if state['approved']:
        return END

    if state['attempts'] >= MAX_ATTEMPTS:
        return END

    return 'improve_recipe'

builder = StateGraph(State)

builder.add_node("generate_recipe", generate_recipe)
builder.add_node("check_recipe", check_recipe)
builder.add_node("improve_recipe", improve_recipe)

builder.add_edge(START, "generate_recipe")
builder.add_edge("generate_recipe", "check_recipe")
builder.add_conditional_edges("check_recipe", should_continue)
builder.add_edge("improve_recipe", "check_recipe")

graph = builder.compile()

initial_state = {
    "ingredients": "chicken, rice, onion, tomato",
    "recipe": "",
    "feedback": "",
    "approved": False,
    "attempts": 0
}

result = graph.invoke(initial_state)

print(result["recipe"])
print(result["feedback"])
print(f"Attempts: {result['attempts']}")
print(f"Approved: {result['approved']}")




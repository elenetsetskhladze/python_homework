from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL = "gemini-3.5-flash-lite"

class State(TypedDict):
    product_text: str
    product_info: str
    marketing_text: str
    final_description: str

def extract(state: State):
    llm = ChatGoogleGenerativeAI(model=MODEL)

    prompt = f"""
    Extract the main product information from the following text and organize it into clear lines.
    Use only the provided information and do not invent details.
    Product description: {state['product_text']}
    """
    response = llm.invoke(prompt)

    return {
        "product_info": response.text
    }

def marketing(state: State):
    llm = ChatGoogleGenerativeAI(model=MODEL)

    prompt = f"""
       Write an attractive and professional marketing description for an online store using the following product information.
       Use only the provided information and do not invent product features.
       Product information: {state['product_info']}
       """

    response = llm.invoke(prompt)

    return {
        "marketing_text": response.text
    }


def format(state: State):


    text = f"""
    === PRODUCT DESCRIPTION ===

    {state['marketing_text']}

    === END ===
    """
    return {
     "final_description": text.strip()
    }

builder = StateGraph(State)

builder.add_node("extract", extract)
builder.add_node("marketing", marketing)
builder.add_node("format", format)

builder.add_edge(START, "extract")
builder.add_edge("extract", "marketing")
builder.add_edge("marketing", "format")
builder.add_edge("format", END)

graph = builder.compile()

result = graph.invoke({
    "product_text": "iphone 15, 6.1 inch oled, 128gb, a16 bionic, 48mp camera, usb-c, battery good, available in black and blue",
    "product_info": "",
    "marketing_text": "",
    "final_description": ""
})

print(result["final_description"])



from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage

MODEL = "gemini-3.5-flash-lite"


@tool
def search_hotel(city: str):
    """Find hotels in a city."""

    hotel_data = {
        "tbilisi": [
            "Hotel A — 120 GEL/night",
            "Hotel B — 180 GEL/night",
            "Hotel C — 250 GEL/night"
        ],
        "batumi": [
            "Hotel Sea — 100 GEL/night",
            "Hotel Coast — 170 GEL/night",
            "Hotel Plaza — 230 GEL/night"
        ],
        "kutaisi": [
            "Hotel Central — 90 GEL/night",
            "Hotel Comfort — 140 GEL/night",
            "Hotel Grand — 200 GEL/night"
        ]
    }

    return hotel_data.get(
        city.lower(),
        "Hotel data not available for this city."
    )


@tool
def get_exchange_rate(currency: str):
    """Get currency exchange rates against GEL."""

    exchange_rates = {
        "USD": 2.70,
        "EUR": 3.15,
        "GBP": 3.60
    }

    rate = exchange_rates.get(currency.upper())

    if rate is None:
        return "Exchange rate not available for this currency."

    return f"1 {currency.upper()} = {rate} GEL"


@tool
def search_attractions(city: str):
    """Find popular attractions in a city."""

    attractions_data = {
        "tbilisi": [
            "Narikala Fortress",
            "Old Tbilisi",
            "Mtatsminda Park"
        ],
        "batumi": [
            "Batumi Boulevard",
            "Ali and Nino Statue",
            "Batumi Botanical Garden"
        ],
        "kutaisi": [
            "Bagrati Cathedral",
            "Gelati Monastery",
            "Prometheus Cave"
        ]
    }

    return attractions_data.get(
        city.lower(),
        "Attraction data not available for this city."
    )


llm = ChatGoogleGenerativeAI(
    model=MODEL
)

tools = [
    search_hotel,
    get_exchange_rate,
    search_attractions
]

llm_with_tools = llm.bind_tools(tools)

question = input("Enter your travel question: ")

response = llm_with_tools.invoke(question)

tool_results = []

for tool_call in response.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print(f"Executing tool: {tool_name}")
    print(f"Tool arguments: {tool_args}")

    selected_tool = next(
        tool for tool in tools
        if tool.name == tool_name
    )

    result = selected_tool.invoke(tool_args)

    tool_results.append(
        ToolMessage(
            tool_call_id=tool_call["id"],
            content=str(result)
        )
    )

messages = [
    {
        "role": "user",
        "content": question
    },
    response,
    *tool_results
]

final_response = llm_with_tools.invoke(messages)

print("\nTravel Assistant:")
print(final_response.text)

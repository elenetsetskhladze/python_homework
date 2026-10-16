
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Literal

MODEL_NAME = "gemini-3.5-flash-lite"

model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0
)


class ProductReview(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    pros: list[str]
    cons: list[str]
    summary: str
    recommend: bool


parser = PydanticOutputParser(pydantic_object=ProductReview)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are a product review analyzer.

        Analyze the product review and provide:
        - sentiment: positive, negative, or neutral
        - pros: a list of positive aspects
        - cons: a list of negative aspects
        - summary: a short summary of the review
        - recommend: whether you recommend buying the product (true or false)

        Do not invent information that is not mentioned in the review.
        If there are no pros or cons, return an empty list.

        {format_instructions}
        """),

        ("human", "{review}")
    ]
)


chain = prompt | model | parser


while True:
    review = input("Enter a product review (or type 'exit' to quit): ")

    if review.lower() == "exit":
        break

    response = chain.invoke(
        {
            "review": review,
            "format_instructions": parser.get_format_instructions()
        }
    )

    print(response)
    print(type(response))

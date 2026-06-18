import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# News Tool
def news_tool(topic: str):
    news = {
        "ai": [
            "OpenAI releases a new AI model",
            "Google announces new AI features"
        ],
        "cricket": [
            "India wins the T20 series",
            "IPL schedule announced"
        ],
        "india": [
            "Government launches a new digital initiative",
            "Economic growth forecast updated"
        ]
    }

    return {"headlines": news.get(topic.lower(), ["No news available"])}

# Tool Metadata
tools = [{
    "name": "latest_news",
    "description": "Provides the latest news on a given topic.",
    "arguments": [{"topic": "news topic"}]
}]

tools_mapping = {
    "latest_news": news_tool
}

# LLM
model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# Prompt
template = """
You are a News AI Assistant.

Available Tools:
{tools}

Respond only in JSON.

If a tool is needed:
{{"actions":[{{"action":"latest_news","arguments":{{"topic":"..."}}}}]}}

If tool responses are available:
{{"answer":"your response"}}

Question: {question}
Tool Responses: {tool_responses}
"""

prompt = ChatPromptTemplate.from_template(template)

# User Question
question = input("Enter Question: ")

# Step 1
response = model.invoke(
    prompt.invoke({
        "question": question,
        "tools": tools,
        "tool_responses": ""
    })
)

response_json = json.loads(response.content)
print("STEP 1:", response_json)

# Step 2
if "actions" in response_json:
    action = response_json["actions"][0]

    result = tools_mapping[action["action"]](**action["arguments"])

    tool_response = [{
        "action": action["action"],
        "response": result
    }]

    print("STEP 2:", tool_response)

    # Step 3
    final = model.invoke(
        prompt.invoke({
            "question": question,
            "tools": tools,
            "tool_responses": tool_response
        })
    )

    print("Final Answer:", final.content)
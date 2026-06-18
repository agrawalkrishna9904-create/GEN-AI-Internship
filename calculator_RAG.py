import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Calculator Tool
def calculator_tool(expression: str):
    try:
        return {"result": eval(expression)}
    except:
        return {"error": "Invalid Expression"}

tools = [{
    "name": "calculator",
    "description": "Performs mathematical calculations.",
    "arguments": [{"expression": "mathematical expression"}]
}]
tools_mapping = {
    "calculator": calculator_tool
}
# LLM
model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)
# Prompt
template = """
You are a Calculator AI Assistant.

Available Tools:
{tools}

Respond only in JSON.

If a tool is needed:
{{"actions":[{{"action":"calculator","arguments":{{"expression":"..."}}}}]}}

If you have the tool response:
{{"answer":"your answer"}}

Question: {question}
Tool Responses: {tool_responses}
"""

prompt = ChatPromptTemplate.from_template(template)
question = input("Enter Question: ")
response = model.invoke(
    prompt.invoke({
        "question": question,
        "tools": tools,
        "tool_responses": ""
    })
)
response_json = json.loads(response.content)
print("STEP 1:", response_json)

# Step 2: Execute Tool
if "actions" in response_json:
    action = response_json["actions"][0]
    result = tools_mapping[action["action"]](
        **action["arguments"]
    )
    tool_response = [{
        "action": action["action"],
        "response": result
    }]
    print("STEP 2:", tool_response)

    # Step 3: Final Answer
    final = model.invoke(
        prompt.invoke({
            "question": question,
            "tools": tools,
            "tool_responses": tool_response
        })
    )
    print("Final Answer:", final.content)
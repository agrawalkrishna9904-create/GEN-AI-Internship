import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

topic = "Python"
difficulty = "Intermediate"
num_questions = 10
llm =ChatGroq(model="llama-3.1-8b-instant")
template = f"""
Generate {num_questions} MCQs on {topic} with {difficulty} difficulty.
qive question name as 1,2,3,4,5...
Give each options name it as A,B,C,D
generate questions in json format
"""
prompt_template = ChatPromptTemplate.from_template(template=template)
prompt = prompt_template.invoke({
    "num_questions": num_questions,
    "topic": topic,
    "difficulty":difficulty
    })

# response=llm.invoke(prompt)
# questions=response.content
#     print("\n MCQ Question:")
#     print(questions)
response = llm.invoke(prompt)
print(response.content)
questions=response.content
quiz = json.loads(questions)

with open("quiz.json", "w") as file:
    json.dump(quiz, file, indent=4)



filename = f"{topic}_{difficulty}_{num_questions}_MCQ.txt"
with open(filename, "w", encoding="utf-8") as file:
        file.write(str(questions))

print(f"\nQuestions saved to {filename}")
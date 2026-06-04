# Q2:
# Generate MCQs from a topic.
# Requirements
# i)   Input:
#         Topic: Python
#         Difficulty: Intermediate
#         Number of Questions: 10
# ii)  Output:
#      Q1
#      A.
#      B.
#      C.
#      D.
#      Answer:
#      Bonus
# iii) Save quiz in JSON format.
# Example:
# [
#  {{
#   "question":"What is Python?",
#   "options":["A","B","C","D"],
#   "answer":"A"
#  }}
# ]

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm =ChatGroq(model="llama-3.1-8b-instant")
template = ("Generate exactly {num_question} MCQ questions for user for in {level} in {Topic}")
prompt_template = ChatPromptTemplate.from_template(template=template)

while True:
    Topic = input("Enter Topic Name (or 'quit' to exit): ") 
    if Topic.lower()=="quit":
        print("Application Terminated")
        break
    level=input("Enter Difficulty level: Fresher,Intermediate,Advanced:")
    num_question=input("Enter number of Questions:")
    prompt = prompt_template.invoke({
    "Topic": Topic,
    "level": level,
    "num_question":num_question
    })

    response=llm.invoke(prompt)
    questions=response.content
    print("\n MCQ Question:")
    print(questions)


    filename = f"{Topic}_{level}_{num_question}_MCQ.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(questions))

    print(f"\nQuestions saved to {filename}")





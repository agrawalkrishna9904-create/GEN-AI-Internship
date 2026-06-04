# Q1: Create a GenAI application that generates interview questions.
# Requirements
# 1. Ask the user for:
#      i)  Technology Name
#      ii) Experience Level
# 2. Use a ChatPromptTemplate to create a prompt dynamically.
# 3. Example Input:
#         i) Technology: Python
#         ii) Level: Fresher
# 4. Prompt:
#           Generate 10 interview questions for a Fresher in Python.
# 5. Display questions on screen.
# 6. Save questions to a file:
#          Python_Fresher_Interview.txt
# 7. Allow the user to generate questions for multiple technologies in a loop.
# 8. The application should terminate when the user enters:
#                   quit

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant")
template = """Generate 10 interview questions for a {level} in {technology}."""
prompt_template = ChatPromptTemplate.from_template(template=template)
while True:
    technology = input("Enter Technology Name (or 'quit' to exit): ")
    if technology.lower() == "quit":
        print("Application Terminated.")
        break
    level = input("Enter Experience Level: Fresher,Intermediate,Advanced:")

    # create prompt (generate 10 interviwe questions)
  
  
    prompt = prompt_template.invoke({
        "technology": technology,
        "level": level
    })
    response = llm.invoke(prompt)
    questions = response.content
    print("\nInterview Questions:\n")
    print(questions)
    
   
    filename = f"{technology}_{level}_Interview.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(questions))  
        
    print(f"\nQuestions saved to {filename}")

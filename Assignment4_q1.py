# CSV Explainer Chatbot using Streamlit, Pandas, SQL, and LLM
# Objective
# To allow users to upload a CSV file and ask questions in natural language. The chatbot converts the question into an SQL query, executes it on the CSV data, and explains the result in simple English.
# (check Expected UI Screenshot shared on Assignment folder (2 screenshot added)
# Steps:
# 1. User uploads a CSV file.
# 2. CSV data is loaded into a Pandas DataFrame.
# 3. The schema (column names and data types) is displayed.
# 4. User asks a question in natural language.
# 5. LLM converts the question into an SQL query.
# 6. PandasQL executes the SQL query on the DataFrame.
# 7. Results are displayed in a table.
# 8. LLM generates a simple English explanation of the output.

# Question: What is the average salary of employees?
# Generated SQL:
# SELECT AVG(salary) AS average_salary
# FROM data;

# Output:
# average_salary
# 55000
# Explanation:
# The average salary of all employees in the dataset is ₹55,000

import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant")

st.title("CSV Explainer ChatBot ")

file = st.file_uploader("Upload csv",type="Csv")
if file:
    data=pd.read_csv(file)

    st.write("### Dataset")
    st.dataframe(data)

    st.write("###Schema")   #column name
    st.write(data.dtypes)   #datatypes

#Ask the question   
question = st.text_input("Ask any question")
if st.button("submit") and question:
     prompt = f"""
        Table name: data
        Columns: {', '.join(data.columns)}
        Convert this question into SQL:
        {question}
        Return only SQL.
        """     
 #LLM converts the question into SQL     
sql = llm.invoke(prompt).content.strip()
sql = sql.replace("```sql", "").replace("```", "")

#shows the SQL Query
st.write("### Sql Query")  
st.code(sql)
result = sqldf (sql,{"data":data})

#shoes the result in the form of table
st.write("### Result")
st.dataframe(result)

explain = llm.invoke(
            f"Explain this result in simple English:\n{result}"
        ).content

st.write("### Explaination")
st.write(explain)
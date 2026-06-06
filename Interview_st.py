import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant")
st.title("Generate Interview Questions")
technology=st.text_input("Technology name")
level = st.selectbox(
    "Experience Level",
    ["Fresher", "Intermediate", "Advanced"]
)
if st.button("Generate Questions"):

 prompt = ChatPromptTemplate.from_template(
        """
        Generate 10 interview questions for a {level} in {technology}.
        Return questions in numbered format.
        """
    )
chain = prompt | llm

response = chain.invoke({
        "level": level,
        "technology": technology
    })

st.subheader("Interview Questions")
st.write(response.content)
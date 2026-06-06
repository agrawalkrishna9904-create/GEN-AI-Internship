
import streamlit as st
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
st.title("AI CHATBOT")
llm = ChatGroq(model="llama-3.1-8b-instant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#user input
if prompt := st.chat_input("Ask a question..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
with st.chat_message("user"):
        st.markdown(prompt)
#prompt
query = f"""
    Answer the following question in EXACTLY 2 bullet points only name bullet points as 1,2 each point on new line.

    Question: {prompt}
    """

response = llm.invoke(query)
answer = response.content

def stream_data(text):
        for word in text.split():
            yield word + " "
            time.sleep(0.05)

with st.chat_message("assistant"):
        st.write_stream(stream_data(answer))

st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    

   




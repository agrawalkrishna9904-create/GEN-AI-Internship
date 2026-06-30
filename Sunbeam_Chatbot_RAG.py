import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.embeddings import init_embeddings
from langchain_groq import ChatGroq
load_dotenv()

st.set_page_config(
    page_title="Sunbeam Course Chatbot",
    page_icon="🎓",
    layout="centered"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "kb_created" not in st.session_state:
    st.session_state.kb_created = False

st.markdown("""
<style>

h1 {
    text-align: center;
    color: #0E76A8;
}

.login-text {
    text-align: center;
    color: gray;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

COURSE_FOLDER = "courses_data"
DB_FOLDER = "knowledge_base"

os.makedirs(COURSE_FOLDER, exist_ok=True)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def login():
    st.markdown("<h1>🎓 Sunbeam Course Chatbot</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='login-text'>AI Powered Course Information Assistant</p>",
        unsafe_allow_html=True
    )

    st.write("---")
    st.subheader("🔐 Login")

    username = st.text_input("👤 Username", placeholder="Enter Username")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter Password")

    remember = st.checkbox("Remember Me")

    col1, col2 = st.columns(2)

    with col1:
        login_btn = st.button("🚀 Login", use_container_width=True)

    with col2:
        st.button("🔄 Reset", use_container_width=True)

    if login_btn:

        if username == "admin" and password == "sunbeam123":

            st.session_state.logged_in = True
            st.success("✅ Login Successful!")
            st.balloons()
            st.rerun()

        else:
            st.error("❌ Invalid Username or Password")

def logout():
    st.sidebar.title("Menu")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

def get_embeddings():
    return init_embeddings(
        model="text-embedding-nomic-embed-text-v1.5",
        provider="openai",
        base_url="http://127.0.0.1:1234/v1",
        api_key="not-needed",
        check_embedding_ctx_length=False
    )

def load_course_files():
    documents = []
    doc_id = 1

    txt_files = [
        file for file in os.listdir(COURSE_FOLDER)
        if file.endswith(".txt")
    ]
    for file_name in txt_files:
        file_path = os.path.join(COURSE_FOLDER, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_name,
                    "doc_id": doc_id
                }
            )
        )

        doc_id += 1

    return documents

def create_knowledge_base():

    documents = load_course_files()

    if len(documents) == 0:
        st.error("No TXT files found inside courses_data folder.")
        st.stop()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    try:
        vector_store = Chroma(
            collection_name="sunbeam_courses",
            persist_directory=DB_FOLDER,
            embedding_function=get_embeddings()
        )
        vector_store.delete_collection()
    except:
        pass

    vector_store = Chroma(
        collection_name="sunbeam_courses",
        persist_directory=DB_FOLDER,
        embedding_function=get_embeddings()
    )

    vector_store.add_documents(chunks)

def load_knowledge_base():
    return Chroma(
        collection_name="sunbeam_courses",
        persist_directory=DB_FOLDER,
        embedding_function=get_embeddings()
    )

if not st.session_state.kb_created:
    with st.spinner("Creating Knowledge Base..."):
        create_knowledge_base()
    st.session_state.kb_created = True

prompt = PromptTemplate.from_template("""
You are an AI assistant for Sunbeam Institute.

Use ONLY the context provided below.

Context:
{context}

Question:
{question}

Answer:
""")
def chatbot():

    st.title("🎓 Sunbeam Course Chatbot")

    if mode == "RAG":

        st.header("📚 RAG Mode")

        question = st.text_input(
            "Ask about Sunbeam Courses",
            key="rag_question"
        )

    elif mode == "Agentic-RAG":

        st.header("🤖 Agentic-RAG Mode")

        question = st.text_input(
            "Ask about Sunbeam Courses",
            key="agent_question"
        )

        if st.button("Search", key="agent_button"):

            st.info("🚀 Agentic-RAG Coming Soon...")
        st.divider()


    if st.button("Search"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            st.stop()

        list_queries = [
            "list all courses",
            "show all courses",
            "courses available",
            "show courses",
            "list courses"
        ]

        if any(q in question.lower() for q in list_queries):

            st.subheader("📚 Courses Offered")

            txt_files = sorted([
                file.replace(".txt", "")
                for file in os.listdir(COURSE_FOLDER)
                if file.endswith(".txt")
            ])

            for i, course in enumerate(txt_files, start=1):
                st.write(f"{i}. {course}")

            st.stop()

        vector_store = load_knowledge_base()

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10}
        )
        docs = retriever.invoke(question)

        if len(docs) == 0:
            st.warning("No relevant information found.")
            st.stop()
        context = "\n\n".join(doc.page_content for doc in docs)

        chain = prompt | llm

        response = chain.invoke({
            "context": context,
            "question": question
        })

        st.subheader("🤖 Answer")
        st.write(response.content)

        st.divider()

        st.subheader("📚 Source Files")

        shown = set()

        for doc in docs:
            source = doc.metadata.get("source")
            if source not in shown:
                st.write("📄", source)
                shown.add(source)

        with st.expander("Retrieved Context"):
            for doc in docs:
                st.write(doc.page_content)
if not st.session_state.logged_in:
    login()
    st.stop()
logout()

st.sidebar.title("🤖 Chat Mode")
mode = st.sidebar.radio(
    "Select Mode",
    [
        "RAG",
        "Agentic-RAG"
    ]
)
st.sidebar.divider()
st.sidebar.info(f"Current Mode : {mode}")
chatbot()
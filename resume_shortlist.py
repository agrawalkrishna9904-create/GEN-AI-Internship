from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain.embeddings import init_embeddings
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import streamlit as st
import os
load_dotenv()

st.title("AI Resume Shortlisting")
pdf_folder = "fake-resumes"
os.makedirs(pdf_folder, exist_ok=True)

# Load PDFs
def load_pdf_file():
    documents = []
    doc_id = 1
    pdf_files = [
        file for file in os.listdir(pdf_folder)
        if file.endswith(".pdf")
    ]
    for file_name in pdf_files:
        file_path = os.path.join(pdf_folder, file_name)

        loader = PyMuPDFLoader(file_path)
        pages = loader.load()
        for page in pages:
            documents.append(
                Document(
                    page_content=page.page_content,
                    id=str(doc_id),
                    metadata={
                        "source": file_name,
                        "doc_id": doc_id
                    }
                )
            )
            doc_id += 1
    return documents
    
# Embeddings
def get_embeddings():
    return init_embeddings(
        model="text-embedding-nomic-embed-text-v1.5",
        provider="openai",
        base_url="http://127.0.0.1:1234/v1",
        api_key="not-needed",
        check_embedding_ctx_length=False
    )

 #  Create Knowledge Base 
def create_knowledge_base():
    documents = load_pdf_file()
    if not documents:
        st.warning("No resumes found.")
        return None
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    vector_store = Chroma(
        collection_name="my_collection",
        persist_directory="./knowledge_base",
        embedding_function=get_embeddings()
    )
    vector_store.add_documents(chunks)
    return vector_store

# Load Vector DB 
def load_knowledge_base():
    return Chroma(
        collection_name="my_collection",
        persist_directory="./knowledge_base",
        embedding_function=get_embeddings()
    )
#sidebar
st.sidebar.title("Resume Management")
menu = st.sidebar.radio(
     "select operation",
[ 
     "Upload Resume",
     "Update Resume",
     "List Resumes",
     "Delete Resume",
     "Shortlist Resumes"
])
os.makedirs("fake-resumes",exist_ok=True)

#upload resume
if menu == "Upload Resume":
    uploaded_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )
    if uploaded_files:
        for file in uploaded_files:
            path = os.path.join(pdf_folder, file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            st.success(f"{file.name} uploaded.")
        if st.button("Create Knowledge Base"):
            create_knowledge_base()
            st.success("Knowledge Base Created Successfully")
#  UPDATE 
elif menu == "Update Resume":
    st.header("Update Existing Resume")
    pdf_files = [
        file for file in os.listdir(pdf_folder)
        if file.endswith(".pdf")
    ]
    if pdf_files:
        selected_file = st.selectbox(
            "Select Resume",
            pdf_files
        )
        updated_file = st.file_uploader(
            "Upload Updated Resume",
            type=["pdf"]
        )
        if st.button("Update"):
            if updated_file:
                file_path = os.path.join(
                    pdf_folder,
                    selected_file
                )
                with open(file_path, "wb") as f:
                    f.write(updated_file.getbuffer())
                create_knowledge_base()
                st.success(
                    f"{selected_file} updated successfully."
                )
    else:
        st.warning("No resumes available.")

#  List Resumes 
elif menu == "List Resumes":
    pdf_files = [
        file for file in os.listdir(pdf_folder)
        if file.endswith(".pdf")
    ]
    if pdf_files:
        for file in pdf_files:
            st.write(file)
    else:
        st.warning("No resumes uploaded.")

# Delete Resume 
elif menu == "Delete Resume":
    pdf_files = [
        file for file in os.listdir(pdf_folder)
        if file.endswith(".pdf")
    ]
    if pdf_files:

        file_name = st.selectbox(
            "Select Resume",
            pdf_files
        )
        if st.button("Delete"):
            os.remove(
                os.path.join(
                    pdf_folder,
                    file_name
                )
            )
            st.success(
                f"{file_name} deleted."
            )
            st.rerun()
    else:
        st.warning("No resumes available.")

# Shortlist Resumes 
elif menu == "Shortlist Resumes":
    st.header("Shortlist Candidates")
    job_description = st.text_area(
        "Enter Job Description"
    )
    k = st.number_input(
        "Number of Resumes",
        min_value=1,
        value=2
    )
    if st.button("Shortlist"):
        vector_store = load_knowledge_base()
        results = vector_store.similarity_search(
            job_description,
            k=k
        )
        st.subheader("Top Candidates")
        shortlisted = set()
        for doc in results:
            file_name = doc.metadata["source"]
            if file_name not in shortlisted:
                st.success(file_name)
                shortlisted.add(file_name)
        

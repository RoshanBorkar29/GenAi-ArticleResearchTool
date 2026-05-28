import os
from dotenv import load_dotenv

import streamlit as st

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI


# =====================================
# Load Environment Variables
# =====================================
load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
if GEMINI_MODEL.startswith("models/"):
    GEMINI_MODEL = GEMINI_MODEL.removeprefix("models/")


# =====================================
# Streamlit UI
# =====================================
st.set_page_config(
    page_title="AI Equity Research Tool",
    layout="wide"
)

st.title("AI Equity Research Tool")
st.sidebar.title("News Article URLs")


# =====================================
# URL Inputs
# =====================================
urls = []

for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")

    if url:
        urls.append(url)


# =====================================
# Process Button
# =====================================
process_url_clicked = st.sidebar.button("Process URLs")

main_placeholder = st.empty()


# =====================================
# Process URLs Section
# =====================================
if process_url_clicked:

    if len(urls) == 0:
        st.warning("Please enter at least one URL.")

    else:
        try:

            # ---------------------------------
            # Load Article Data
            # ---------------------------------
            main_placeholder.text("Loading article data...")

            loader = UnstructuredURLLoader(urls=urls)

            data = loader.load()

            st.success("URLs loaded successfully!")


            # ---------------------------------
            # Split Text into Chunks
            # ---------------------------------
            main_placeholder.text("Splitting text into chunks...")

            text_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", ".", ","],
                chunk_size=1000,
                chunk_overlap=200
            )

            docs = text_splitter.split_documents(data)

            st.success("Text split into chunks successfully!")


            # ---------------------------------
            # Create Embeddings
            # ---------------------------------
            main_placeholder.text("Creating embeddings...")

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )


            # ---------------------------------
            # Store in Chroma DB
            # ---------------------------------
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory="vectorstore"
            )

            # Persist DB
            vectorstore.persist()

            main_placeholder.text("Embeddings stored successfully!")

            st.success("Embeddings stored in ChromaDB successfully!")


           

        except Exception as e:
            st.error(f"Error while processing URLs: {e}")


# =====================================
# User Query Section
# =====================================
query = st.text_input("Ask a Question About the Articles:")


if query:

    # Check if vector DB exists
    if os.path.exists("vectorstore"):

        try:

            # ---------------------------------
            # Load Embedding Model
            # ---------------------------------
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )


            # ---------------------------------
            # Load Existing Chroma DB
            # ---------------------------------
            vectorstore = Chroma(
                persist_directory="vectorstore",
                embedding_function=embeddings
            )


            # ---------------------------------
            # Create Retriever
            # ---------------------------------
            retriever = vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )


            # ---------------------------------
            # Load Gemini Model
            # ---------------------------------
            llm = ChatGoogleGenerativeAI(
                model=GEMINI_MODEL,
                temperature=0.3
            )


            # ---------------------------------
            # Create Retrieval Chain
            # ---------------------------------
            prompt = ChatPromptTemplate.from_template(
                """Answer the question using only the context below.

Context:
{context}

Question: {input}

If the answer is not in the context, say I don't know.
"""
            )

            document_chain = create_stuff_documents_chain(llm, prompt)

            chain = create_retrieval_chain(retriever, document_chain)


            # ---------------------------------
            # Generate Response
            # ---------------------------------
            response = chain.invoke(
                {"input": query}
            )


            # ---------------------------------
            # Display Answer
            # ---------------------------------
            st.header("Answer")

            st.write(response["answer"])


        except Exception as e:
            st.error(f"Error while generating answer: {e}")

    else:
        st.error("Please process URLs first!")

# Install the required packages
# pip install langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
import google.generativeai as genai
import os

# read api key from environment variable
google_api_key = os.getenv('gemini-api')

file_path = os.path.abspath("backend/src/training_data/ESC_Guidelines.pdf")

loader = PyPDFLoader(file_path)
data = loader.load()

# split the document into chunks

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 50)
docs = text_splitter.split_documents(data)

# setting up the embeddings and creating a vector store with google GEMINI


embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key = google_api_key)

# Geminin esilämmitys
_ = embeddings.embed_documents(["test"])

cache_store = InMemoryStore()

# Käytetään Chroma:n pysyvää tallennusta (persist)
vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory="db_cache")


# retrieve information using LangChain and Gemini

retriever = vectorstore.as_retriever(search_type = "mmr", search_kwargs = {"k": 5})

retrieved_docs = retriever.invoke("ESC Guidelines for the management of acute coronary syndromes in patients presenting without persistent ST-segment elevation")
retrieved_docs

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash-002', temperature = 0, max_tokens = 500, google_api_key = google_api_key)

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use only the following pieces of retrieved context to answer the question. "
    "If you don't know the answer based on the context, say 'The information is not available in the documents provided.' "
    "Do not use any outside knowledge or make assumptions. "
    "Use three sentences maximum and keep the answer concise."
    "\n\n"
    "{context}"
)

# Construct the prompt template with the system and human messages
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)

rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input":"What are the recommendations for the management of acute coronary syndromes in patients presenting without persistent ST-segment elevation?"})

print(response["answer"])


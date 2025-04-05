"""
RAG (Retrieval-Augmented Generation) System with Google Gemini and ChromaDB

This system provides conversational question-answering capabilities by:
1. Loading and processing PDF documents from Google Cloud Storage
2. Creating vector embeddings using Google Generative AI
3. Storing documents in ChromaDB vector store
4. Retrieving relevant context for questions
5. Generating answers using Gemini 2.0 Flash model with conversation memory

Features:
- Supports both English and Finnish
- Maintains conversation history
- Automatically handles cases when information isn't found
- Provides follow-up questions
"""

from google.cloud import storage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from PyPDF2 import PdfReader
import os
import io
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory

class RAGSystem:
    """
    A Retrieval-Augmented Generation system using Google Gemini and ChromaDB.
    
    Attributes:
        bucket_name (str): Google Cloud Storage bucket name
        persist_directory (str): Path to store ChromaDB data
        google_api_key (str): API key for Google Generative AI
    """
    
    def __init__(self, bucket_name="training_data-1", persist_directory="data/chroma_db"):
        load_dotenv()
        self.bucket_name = bucket_name
        self.persist_directory = persist_directory
        self.google_api_key = os.getenv('GEMINI_API')
        self.vectorstore = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.initialize_components()
    
    def initialize_components(self):
        if os.path.exists(self.persist_directory):
            print("Using existing processed data...")
            self.initialize_existing_vectorstore()
        else:
            print("Processing PDFs from bucket...")
            self.process_new_documents()
        
        self.initialize_retriever()
        self.initialize_llm_chain()
    
    def initialize_existing_vectorstore(self):
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.google_api_key
        )
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings
        )
    
    def process_new_documents(self):
        all_texts = self.download_and_extract_pdfs()
        docs = self.split_texts(all_texts)
        self.create_vectorstore(docs)
    
    def download_and_extract_pdfs(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        
        all_texts = []
        for blob in blobs:
            if blob.name.endswith(".pdf"):
                print(f"Downloading {blob.name}...")
                pdf_stream = io.BytesIO()
                blob.download_to_file(pdf_stream)
                pdf_stream.seek(0)
                
                reader = PdfReader(pdf_stream)
                text = "\n".join(
                    [page.extract_text() for page in reader.pages if page.extract_text()]
                )
                all_texts.append(text)
        return all_texts
    
    def split_texts(self, texts):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=300,
            separators=["\n\n", "\n", " ", ""],
        )
        return text_splitter.create_documents(texts)
    
    def create_vectorstore(self, docs):
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.google_api_key
        )
        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=self.persist_directory
        )
    
    def initialize_retriever(self):
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5}
        )
    
    def initialize_llm_chain(self):
        self.llm = ChatGoogleGenerativeAI(
            model='gemini-1.5-flash-002',
            temperature=0.55,
            max_tokens=500,
            google_api_key=self.google_api_key
        )
        
        system_prompt = self._create_system_prompt()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
    

    def _create_system_prompt(self):
        return (
            """
            You are a medical AI assistant designed to provide accurate, reliable, and evidence-based information by integrating the user's input with trusted medical reference data. Follow these guidelines:
            
            1. **Leverage Relevant Context:** Utilize and reference the most pertinent medical information from the available documents.
            2. **Analyze the User's Query:** Carefully evaluate the user's health-related questions, incorporating provided medical data as necessary.
            3. **Ensure Precision:** Offer clear, concise, and evidence-supported responses. Always cite credible sources when available.
            4. **Maintain Focus:** Concentrate solely on medically validated information and avoid speculation.
            5. **Exercise Expertise:** Provide confident, direct advice, and clearly indicate when the user should consult a healthcare professional.

            "\n\n"
            Context: {context}
            "\n\n"
            "Chat history: {chat_history}"
            """
        )
    
    def get_response(self, user_input: str) -> str:

        self.memory.chat_memory.add_user_message(user_input)
        
        response = self.rag_chain.invoke({
            "input": user_input,
            "chat_history": self.memory.buffer
        })
        
        self.memory.chat_memory.add_ai_message(response["answer"])
        return response["answer"]
    
    def clear_memory(self):
        self.memory.clear()

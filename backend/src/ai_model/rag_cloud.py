# Jos importit eivät toimi, vaihda interpreteriksi Python 3.10.6 64-bit
from google.cloud import storage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from PyPDF2 import PdfReader
import os
import io
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

# Google API-key
load_dotenv() # Load .env file
google_api_key = os.getenv('GEMINI_API')

# Google Cloud Storage asetukset
bucket_name = "training_data-1" 

# ChromaDB:n tallennuskansio
persist_directory = "data/chroma_db"

# -----------------------------
# 1) Ladataan PDF:t (tarvittaessa), alustetaan Chroma
# -----------------------------

if os.path.exists(persist_directory):
    print("Käytetään aiemmin prosessoitua dataa...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=google_api_key
    )
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
else:
    # Ladataan PDF:t GCS:stä
    print("Ladataan ja prosessoidaan kaikki PDF-tiedostot bucketista...")

    def download_pdfs_from_bucket(bucket_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        all_texts = []
        for blob in blobs:
            if blob.name.endswith(".pdf"):
                print(f"Ladataan {blob.name} bucketista {bucket_name}...")
                pdf_stream = io.BytesIO()
                blob.download_to_file(pdf_stream)
                pdf_stream.seek(0)
                print(f"Tiedosto {blob.name} ladattu muistiin.")

                reader = PdfReader(pdf_stream)
                text = "\n".join(
                    [page.extract_text() for page in reader.pages if page.extract_text()]
                )
                all_texts.append(text)
        return all_texts

    all_texts = download_pdfs_from_bucket(bucket_name)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300,
        separators=["\n\n", "\n", " ", ""],
    )
    docs = text_splitter.create_documents(all_texts)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=google_api_key
    )
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )

# -----------------------------
# 2) Luodaan RAG-ketju (retriever + LLM + prompt)
# -----------------------------
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5}
)

llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash-002',
    temperature=0,
    max_tokens=500,
    google_api_key=google_api_key
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use only the following pieces of retrieved context to answer the question. "
    "Do not use any outside knowledge or make assumptions. "
    "Use three sentences maximum for the main answer and keep the response concise. "

    "If the question is in English and the information is found in the context, first provide a concise answer. "
    "Then, naturally continue the conversation by asking a relevant follow-up question based on the user's query. "

    "If the question is in Finnish and the information is found in the context, first provide a concise answer. "
    "Sen jälkeen jatka keskustelua luontevasti kysymällä aiheeseen liittyvän jatkokysymyksen, joka auttaa käyttäjää syventämään ymmärrystään. "

    "If the question is in English and the information is not found in the context, say: "
    "'Unfortunately, I do not have enough information on the topic you asked about. I recommend reaching out to a specialist or your healthcare provider if needed.' "
    "Then, naturally ask a relevant follow-up question to better understand the user's concern. "

    "If the question is in Finnish and the information is not found in the context, say: "
    "'Valitettavasti minulla ei ole riittävästi tietoa esittämääsi aiheeseen. Suosittelen ottamaan yhteyttä asiantuntijaan tai hoitavaan tahoon tarvittaessa.' "
    "Tämän jälkeen kysy luontevasti jatkokysymys, joka auttaa käyttäjää tarkentamaan tilannettaan. "

    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# -----------------------------
# 3) Julkaistava funktio, jolla saa RAG-vastauksen
# -----------------------------
def get_rag_response(user_input: str) -> str:
    """ Kysyy RAG-ketjulta (Chroma+GEMINI) ja palauttaa vastauksen tekstinä. """
    response = rag_chain.invoke({"input": user_input})
    return response["answer"]

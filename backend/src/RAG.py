# Asenna tarvittavat paketit, jos niitä ei ole asennettu
# pip install langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage // jos PyPDF2 importti ei toimi -> pip3 install PyPDF2.
# Jos importit eivät toimi, vaihda interpreteriksi Python 3.10.6 64-bit

from google.cloud import storage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
import io
import time
from logging_config import logger, log_event

# Lue API-avain ympäristömuuttujasta
google_api_key = os.getenv('gemini-api')

# Google Cloud Storage asetukset
bucket_name = "training_data-1"  # GCS bucket name
blob_name = "ESC_Guidelines.pdf"  # Tiedoston nimi bucketissa

# ChromaDB:n tallennuskansio
persist_directory = "db_cache"

# Funktio PDF-tiedoston lataamiseen Google Cloud Storage -bucketista
def download_file_from_gcs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    print(f"Ladataan tiedosto {blob_name} bucketista {bucket_name}...")

    pdf_stream = io.BytesIO()
    blob.download_to_file(pdf_stream)
    pdf_stream.seek(0)

    print("Tiedosto ladattu muistiin.")
    return pdf_stream

# Tarkistetaan, onko data jo prosessoitu
if os.path.exists(persist_directory):
    print("Käytetään aiemmin prosessoitua dataa...")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key))
else:
    print("Ladataan ja prosessoidaan PDF ensimmäistä kertaa...")
    
    # Lataa PDF vain kerran
    pdf_stream = download_file_from_gcs(bucket_name, blob_name)

    # Käytä PdfReaderia tiedoston käsittelyyn
    reader = PdfReader(pdf_stream)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    # Jaa dokumentti osiin (chunking)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,  
        chunk_overlap=300,  
        separators=["\n\n", "\n", " ", ""],
    )

    docs = text_splitter.create_documents([text])

    # Määritä upotukset ja vektorivarasto Google GEMINI:n avulla
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

    # Luo Chroman vektorivarasto ja tallenna se
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)

# Luo hakutoiminto
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# LLM asetukset
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-002', temperature=0, max_tokens=500, google_api_key=google_api_key)

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

# Rakennetaan prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Luo RAG-malli
from langchain.chains.combine_documents import create_stuff_documents_chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Testaa suorituskyky (mittaa suoritusaika)
start_time = time.time()

# Lähetetään kysymys RAG-mallille
response = rag_chain.invoke({"input": "What are the recommendations for the management of acute coronary syndromes in patients presenting without persistent ST-segment elevation?"})

end_time = time.time()
print(f"Execution Time: {end_time - start_time:.2f} sec")
print(response["answer"])
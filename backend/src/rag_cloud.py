# Asenna tarvittavat paketit, jos niitä ei ole asennettu:
# pip install langchain_google_genai langchain_community langchain_text_splitters pypdf chromadb google-cloud-storage langchain-chroma
# jos PyPDF2 importti ei toimi -> pip3 install PyPDF2.
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

# Lue API-avain ympäristömuuttujasta
google_api_key = os.getenv('gemini-api')

# Google Cloud Storage asetukset
bucket_name = "training_data-1" 


# ChromaDB:n tallennuskansio
persist_directory = "db_cache"

# Funktio, joka hakee kaikki PDF-tiedostot Google Cloud Storage -bucketista ja lukee ne muistivirtana 
def download_pdfs_from_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()  # Hakee kaikki tiedostot bucketista

    all_texts = []  # Lista, johon kaikki PDF-tiedostojen tekstit tallennetaan

    for blob in blobs:
        if blob.name.endswith(".pdf"):  # Vain PDF-tiedostot käsitellään
            print(f"Ladataan {blob.name} bucketista {bucket_name}...")

            pdf_stream = io.BytesIO()
            blob.download_to_file(pdf_stream)
            pdf_stream.seek(0)

            print(f"Tiedosto {blob.name} ladattu muistiin.")

            # Käytetään PdfReaderia tiedoston käsittelyyn
            reader = PdfReader(pdf_stream)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            all_texts.append(text)

    return all_texts

# Tarkistetaan, onko data jo prosessoitu
if os.path.exists(persist_directory):
    print("Käytetään aiemmin prosessoitua dataa...")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key))
else:
    print("Ladataan ja prosessoidaan kaikki PDF-tiedostot bucketista...")
    

    all_texts = download_pdfs_from_bucket(bucket_name)
    
    # Jakaa dokumentit osiin (chunking)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,  
        chunk_overlap=300,  
        separators=["\n\n", "\n", " ", ""],
    )

    docs = text_splitter.create_documents(all_texts)

    # Määritetään upotukset ja vektorivarasto Google GEMINI:n avulla
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

    # Luo Chroman vektorivaraston ja tallentaa sen
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)

# Luo hakutoiminnon
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# LLM asetukset
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-002', temperature=0, max_tokens=500, google_api_key=google_api_key)

from langchain_core.prompts import ChatPromptTemplate

# Prompti ohjeistamaan AI-agenttia
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


# Rakennetaan prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Luodaan RAG-malli
from langchain.chains.combine_documents import create_stuff_documents_chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Testataan suorituskyky (mittaa suoritusaikaa)
start_time = time.time()

# Lähetetään kysymys RAG-mallille
response = rag_chain.invoke({"input": "Voinko liikkua sydäninfarktin jälkeen?"})

end_time = time.time()
print(f"Execution Time: {end_time - start_time:.2f} sec")
print(response["answer"])
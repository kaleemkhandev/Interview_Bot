import os
from PyPDF2 import PdfReader
import langchain
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

os.environ["OPENAI_API_KEY"] = "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"


# Functions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            
    return text

def pdf_doc_loader(pdf_file:str):
    loader_pdf = PyPDFLoader(pdf_file)
    document_pdf = loader_pdf.load_and_split(RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200))
    
    return document_pdf

def vector_database_creation(pdf_document=None):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = FAISS.from_documents(documents=pdf_document, embedding=embeddings)
    
    return docsearch

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
    return vectorstore

def load_db():
    embeddings_openai = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    db = FAISS.load_local('db', embeddings_openai)
    
    return db

def get_conversation_chain(vectorstore, temp_input):
    
    llm = ChatOpenAI(model_name='gpt-4', temperature=temp_input)
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True
    )
    
    return conversation_chain
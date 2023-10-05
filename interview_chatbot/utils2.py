# NousResearch/Llama-2-7b-chat-hf
import os
import tiktoken
#import transformers
import langchain
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)
import torch

os.environ["OPENAI_API_KEY"] = "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"


# Functions
def pdf_doc_loader(pdf_file:str):
    loader_pdf = PyPDFLoader(pdf_file)
    document_pdf = loader_pdf.load_and_split(RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200))
    
    return document_pdf

def pdf_dir_loader(pdf_dir:str):
    loader_pdf = PyPDFDirectoryLoader(pdf_dir)
    document_pdf = loader_pdf.load_and_split(RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100))
    
    return document_pdf

# def vector_db_creation(pdf_document=None):
#     model_name = "sentence-transformers/all-mpnet-base-v2"
#     model_kwargs = {"device": "cuda"}

#     embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

#     # storing embeddings in the vector store
#     docsearch = FAISS.from_documents(pdf_document, embeddings)
#     return docsearch

def vector_database_creation(pdf_document=None):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = FAISS.from_documents(documents=pdf_document, embedding=embeddings)
    
    return docsearch

def save_db(docsearch, save_path=str):
    docsearch = docsearch.save_local(save_path)
    
    print('db_saved....')
    
def merge_db(db1_path:str, db2_path:str):
    # print(db1_path,db2_path)
    db1 = load_db(db1_path)
    db2 = load_db(db2_path)
    db1.merge_from(db2)
    return db1
    
def load_db(path_to_db:str):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    db = FAISS.load_local(path_to_db, embeddings)
    
    return db


def load_Llama2(model_name):
    model_name = model_name
    use_4bit = True
    bnb_4bit_quant_type = "nf4"
    bnb_4bit_compute_dtype = "float16"
    use_nested_quant = False
    # Load the entire model on the GPU 0
    device_map = {"": 0}
    compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

    bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
    )
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map=device_map
            )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # Load LLaMA tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training



    # Ignore warnings
    logging.set_verbosity(logging.CRITICAL)

    # Run text generation pipeline with our next model
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
    return pipe    

def query_db_llama2(pipe,prompt):
    result = pipe(f"<s>[INST] {prompt} [/INST]")
    return result[0]['generated_text'] 

# def query_db_llama2(prompt):
#     llm = Ollama(base_path="/path/to/your/fine_tuned_model", model="llama2",temperature=1.25)
#     quests = llm(prompt)
#     return quests
    

def query_db_gpt3(fine_tuned_model, prompt):
    llm = OpenAI(model_name=fine_tuned_model, temperature=1.25)
    quests = llm(prompt)
    return quests

def query_database(db,job_role):
    llm = OpenAI(model_name='gpt-3.5-turbo', temperature=1.25)
    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    vectorstore=db, 
                                    return_source_documents=True)
    
    
    query = f""" 

    With the context provided, I want you to impersonate an "{job_role} Team lead", I want you to ask interview questions from the candidate. 
    The questions should be "TECHNICAL" and  should be related to his "SKILL SET". Also, you can create a specific scenario related to his skills to test his knowledge to the field.  
    The difficulty of the interview depends on the number of years of experience mentioned in the context.
    Generate the questions in bullet points.
    Generate 10 questions at all times.
    Please be very strcit with the Questions Format as follows:
    - "Q(number): " <Question Statement>
    
    """
    
    
    results = qa({'query': query})
    questions = results['result']
    print(results['result'])
    return questions


# Function to create a PDF document
def create_pdf(filename, content):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    # Title
    styles = getSampleStyleSheet()
    story.append(Paragraph("<b>Interview Questions and Answers</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    
    # Content
    for question, answer in content:
        story.append(Paragraph(f"<b>Hiring Mangaer:</b> {question}", styles["Normal"]))
        story.append(Paragraph(f"<b>Candidate:</b> {answer}", styles["Normal"]))
        story.append(Spacer(1, 12))
    
    # Build the PDF document
    doc.build(story)


def return_questions(id,key,prompt,user_id,job_role):
    try:
        if id == 1:
            pdf_filename = f"interviews/{user_id}_interview.pdf"
            create_pdf(pdf_filename, prompt)
            doc = pdf_doc_loader('interviews/{user_id}_interview.pdf')
            db = vector_database_creation(doc)
            query = query_database(db=db,job_role=job_role) # Enter Role here 
            ques = query.split("\n") # questions lists
            return ques
        elif id == 2:
            query = query_db_gpt3(key, prompt)
            ques = query.split("\n")
            return ques
        elif id == 3:
            pipe = load_Llama2(key)
            query = query_db_llama2(pipe, prompt)
            ques = query.split("\n")
            return ques
        else:
            return "Choose an option between 1 to 3"
    except Exception as e:
        print(e)
        return e

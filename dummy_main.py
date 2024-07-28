#importing all necessary modules
from langchain_community.document_loaders import TextLoader, UnstructuredURLLoader
# from langchain_community.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import UnstructuredImageLoader
# from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
import json
import tempfile
# from langchain_community import
# load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")

llm = GoogleGenerativeAI(google_api_key=api_key,model="models/text-bison-001")

def split_data(data):
    splitter= RecursiveCharacterTextSplitter(
        separators=["\n\n","\n"," ","."],
        chunk_size=1000,
        chunk_overlap=100
    )
    print("splitting the data")
    chunks=splitter.split_documents(data)
    return chunks

def handle_file_upload(upload_file):
        if upload_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload_file.name)[1]) as tmp_file:
                tmp_file.write(upload_file.getbuffer())
                tmp_file_path = tmp_file.name
                print(tmp_file_path)
                return tmp_file_path
def handle_youtube_url(youtube_link):
    if youtube_link is not None:
    # delimiters = ["=", "&"]
        formated_url=youtube_link.replace('=', ' ').replace('&', ' ').split()
        print(formated_url)
        print(formated_url[1])
        transcirpt_key=formated_url[1]
        return transcirpt_key


def return_data_in_chunks(upload_type,url):
    if upload_type=="Document":
            loader = Docx2txtLoader(url)
    elif upload_type=="URL":
            loader = UnstructuredURLLoader(urls=[url])
    elif upload_type=="Image":
            loader=UnstructuredImageLoader(url)
    elif upload_type=="YouTube":
            loader=YoutubeLoader.from_youtube_url(url)
    data=loader.load()
    # print(data)
    data=split_data(data)
    return data



def create_vector_index(data_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("creating vector indexes")
    vector_index= FAISS.from_documents(data_chunks,embeddings)
    return vector_index

def return_chain(vector_index):
    #creating prompt template
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    don't add response at beggining of the response just give me tyhe anwer
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer .

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain=RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_index.as_retriever(),
        input_key='query',
        return_source_documents=True
    )
    return chain

def get_retreivial_chain(*args):
    print(*args)
    upload_type,url,prompt=args[0],args[1],args[2]

    data_chunks=return_data_in_chunks(upload_type,url)
    vector_index=create_vector_index(data_chunks)

    print("creating chain!!")
    chain=return_chain(vector_index)
    respose= chain.invoke(prompt)
    print(respose["result"])
    return respose["result"]
    # if upload_type=="Document":
    #     data_chunks = return_data_from_url(url)
    # elif upload_type=="URL":
    #     data_chunks = return_data_from_url(url)
    # elif upload_type=="Youtube":
    #     data_chunks = return_data_from_url(url)
    # elif upload_type=="Image":
    #     data_chunks = return_data_from_url(url)
    
    # print(type(args[0]))
    

#     response=chain.invoke("Director of bahubali")
#     print(response['result'])
# get_retreivial_chain("URL","https://en.wikipedia.org/wiki/Baahubali:_The_Beginning","Director of bahubali")

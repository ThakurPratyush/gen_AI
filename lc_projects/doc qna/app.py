import streamlit as st 
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()
## Load groq api
os.environ['GROQ_API_KEY']= os.getenv('GROQ_API_KEY')
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

## LLM MODEL
llm = ChatGroq(groq_api_key = groq_api_key, model_name  = "Gemma-7b-It")

#prompt template
prompt = ChatPromptTemplate.from_template(
    """
    answer the questions based on provided context only.
    Please provide the most accurate response based on the context
    {context}
    {input}
    
    
    """
)

def create_vector_embedding():
    if "vectors" not in st.session_state:
        ## initializing the open ai embeddings 
        ## can also use ollama embeddings here , would be slow comp since 
        ## runs on local
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("research_papers")
        st.session_state.docs= st.session_state.loader.load()## loading in documents in the session state
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        st.session_state.final_documents= st.session_state.text_splitter.split_documents(st.session_state.docs[:50]) #take the first 
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
        
        
        
st.title("RAG Document Q&A With Groq And openai")
user_prompt = st.text_input("Enter the query you have on research paper")

if st.button("document embedding"):
    create_vector_embedding()
    st.write("vector database is ready")
    
import time
if user_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    ## this combine the llm and the prompt
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    ## now context is filled with the retirval information which is embeded vector form of document
    start = time.process_time()
    response = retrieval_chain.invoke({"input" : user_prompt})
    print(f"Response time :{time.process_time()-start}")
    
    st.write(response['answer'])
    ## write context and sources from streamlit expander
    with st.expander("document similarity search"):
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("--------------")    
    
    
    


import os
from dotenv import load_dotenv
import streamlit as st 
## would be used to create llm models 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import OllamaLLM

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
## LANGSMITH TRACKING
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LC_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


## prompt template 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","you are a useful assistant"),
        ("user","question: {question}")
    ]
)

## streamlit framework
st.title("langchain demo using gemma2:2b")
input_text = st.text_input("what question do you have in mind?")


## ollama gemma2:2b model 
llm = OllamaLLM(model = "gemma2:2b")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))
    
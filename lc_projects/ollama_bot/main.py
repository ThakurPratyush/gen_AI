from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LC_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With OLLAMA"

    ## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful massistant . Please  repsonse to the user queries"),
        ("user","{question}")
    ]
)

def generate_response(question,engine,temperature,max_tokens):

    llm=OllamaLLM(model=engine,temperature=temperature, max_tokens=max_tokens)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

## #Title of the app
st.title("Enhanced Q&A Chatbot With OpenAI")

## Select the ollama model
engine=st.sidebar.selectbox("Select Open AI model",["gemma2:2b"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## MAin interface for user input
st.write("Goe ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)

else:
    st.write("Please provide the user input")






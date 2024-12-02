import streamlit as st 
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

## set up streamlit

st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant",page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")

## sidebar for groq api key 
groq_api_key = st.sidebar.text_input(label = "Groq_api Key", type= "password")

## if groq api key not specified:

if not groq_api_key:
    st.info("Please add your groq api key to continue")
    st.stop()
    

llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

## initializing the tools

## wikipedia tool for formulas
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name = "wikipedia",
    func = wikipedia_wrapper.run,
    description = "A tool for searching information or reffering the formulas" 
)

## initialize the math tool

## mathchain component uses llm to solve the math questions
math_chain = LLMMathChain.from_llm(llm= llm)
calculator = Tool(
    name = "Calculator",
    func = math_chain.run,
    description="a tool for answering math related questions , input only mathematical expressions"
)

prompt="""
Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below
Question:{question}

"""

prompt_template = PromptTemplate(
input_variable = ["question"],
template = prompt)

## combine all tools int a chain
chain = LLMChain(llm= llm , prompt = prompt_template)

### reasoning tool is the one that calls for chain internallyy

reasoning_tool = Tool(
    name = "Reasoning tool",
    func = chain.run,
    description = "Tool for answering the logic based and reasoning questions"
    
)

## initialize the agents
## combines all the tools 
assistant_agent = initialize_agent(
  tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)



## adding message to the session state if nothing initialized yet
## first message in the session state would be from assistant
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assistant", "content":"Hi i am a math chatbot who can answer math ques"}
    ]
## if a message is present in session state 
## as it to the chat of streamlit
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
## start interaction
## getting input from user, added a basic ques for check
question=st.text_area("Enter your question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

## creates the button and executes if the button pressed

if st.button("find my answer"):
    if question:
        ## question is not nulll
        with st.spinner("generate response..."):
            ##add question and role to session state
            st.session_state.messages.append({"role":"user","content":question})
            ## adds the message to the screen "user" indicating message is from user
            st.chat_message("user").write(question)
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({'role':'assistant',"content":response})
            st.write('### Response:')
            st.success(response)            
    else:
        st.warning("please enter ques:")
            
## langchain to interact with model and gradio for frontend
import requests
import json
import gradio as gr

## specifying where app runs
url="http://localhost:11434/api/generate"
## info given in form of json
headers={

    'Content-Type':'application/json'
}

history=[]

def generate_response(prompt):
    ## generate response considering the history too
    history.append(prompt)
    final_prompt="\n".join(history)

    data={
        "model":"papa_coder",
        "prompt":final_prompt,
        "stream":False
    }

    response=requests.post(url,headers=headers,data=json.dumps(data))

    if response.status_code==200:
        response=response.text
        data=json.loads(response)
        actual_response=data['response']
        return actual_response
    else:
        print("error:",response.text)


interface=gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4,placeholder="Enter your Prompt"),
    outputs="text"
)
interface.launch()

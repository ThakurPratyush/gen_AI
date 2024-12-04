import boto3
import json

prompt_data="""
Act as a Shakespeare and write a poem on Genertaive AI
"""

bedrock=boto3.client(service_name="bedrock-runtime")

payload={
    "prompt":"<s>[INST]"+ prompt_data +"[/INST]",
    "max_tokens":512,
    "temperature":0.5,
    "top_p":0.9
}
body=json.dumps(payload)
model_id="mistral.mistral-small-2402-v1:0"
response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)

response_body=json.loads(response.get("body").read())
repsonse_text=response_body
print(response_body)
import boto3
import json

# Prepare the conversation data
conversation_data = [
    {"role": "user", "content": "Tell me about Paris"},
    {"role": "assistant", "content": "Paris is a city in France."},
    {"role": "user", "content": "Is it the biggest city in France?"}
]

# Set up the parameters
parameters = {
    "max_new_tokens": 512,
    "top_p": 0.9,
    "temperature": 0.6
}

# Initialize Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime")

# Structuring the payload with the conversation and parameters
payload = {
    "inputs": conversation_data,  # List of turns in the conversation
    "parameters": parameters  # Include the parameters here
}

# Convert the payload into JSON
body = json.dumps(payload)

# ARN or ID of the Inference Profile (replace with actual ARN or ID)
inference_profile_arn = "arn:aws:bedrock:us-east-1:455586058507:inference-profile/us.meta.llama3-2-3b-instruct-v1:0"

# Invoking the model using the Inference Profile ARN
response = bedrock.invoke_model(
    body=body,
    modelId=inference_profile_arn,  # Use the ARN of the inference profile
    accept="application/json",
    contentType="application/json"
)

# Parse the response body
response_body = json.loads(response.get("body").read())
response_text = response_body.get("outputs", [{}])[0].get("content", "No response content")

# Print the result
print(response_text)

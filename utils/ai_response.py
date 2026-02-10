import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
# Get the path to the .env file in the root directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable is not set. Checked: " + dotenv_path)

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def get_completion(user_message, system_message="You are a helpful assistant."):
    """
    Get a completion from the AI model.
    
    Args:
        user_message: The user's message/question
        system_message: The system prompt (default: "You are a helpful assistant.")
    
    Returns:
        The model's response
    """
    response = client.complete(
        messages=[
            SystemMessage(system_message),
            UserMessage(user_message),
        ],
        model=model
    )
    return response.choices[0].message.content

import os  
from openai import AzureOpenAI  
from pathlib import Path
from dotenv import load_dotenv


class AzureRAGQueryClient:
    def __init__(
        self,
        azure_openai_endpoint: str,
        azure_openai_api_key: str,
        azure_openai_api_version: str,
        azure_openai_deployment_name: str,
        azure_ai_search_endpoint: str,
        azure_ai_search_index: str,
        azure_ai_search_key: str
    ) -> None:
        # Initialize Azure OpenAI client with key-based authentication
        self.client = AzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            api_key=azure_openai_api_key,
            api_version=azure_openai_api_version,
        )

        self.azure_openai_deployment_name = azure_openai_deployment_name
        self.rag_source_payload = {
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": azure_ai_search_endpoint,
                        "index_name": azure_ai_search_index,
                        "authentication": {
                            "type": "api_key",
                            "key": f"{azure_ai_search_key}"
                        }
                    }
                }
            ]
        }

        self.messages = [
            {
                "role": "system",
                "content": Path("HealthChat/prompts/system.v2.txt").read_text()
            }
        ]

    def complete(self, user_message: str):
        # Prepare the chat prompt  
        self.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # Generate the completion  
        chat_completion = self.client.chat.completions.create(
            model=self.azure_openai_deployment_name,  
            messages=self.messages,
            max_tokens=800,  
            temperature=0.7,  
            top_p=0.95,  
            frequency_penalty=0,  
            presence_penalty=0,  
            stop=None,  
            stream=False,
            extra_body=self.rag_source_payload
        )

        ai_msg = chat_completion.choices[0].message
        citations = chat_completion.choices[0].message.context.get('citations', [])
        citations = [{
            "title":citation['title'],
            "content":citation['content']
        } for citation in citations]

        output = {
            "content": ai_msg.content,
            "context": citations
        }
        return output


if __name__ == "__main__":
    load_dotenv()

    endpoint = os.getenv("ENDPOINT_URL", "https://hackathon-dev-uks-ai-team2.openai.azure.com/")  
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
    api_version = "2024-05-01-preview"
    search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://hackathon-dev-uks-search-2.search.windows.net/")  
    search_index = os.getenv("SEARCH_INDEX", "england-nhs-vector-1732110139794")
    search_key = os.getenv("SEARCH_KEY", "put your Azure AI Search admin key here")  
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")  
    
    client = AzureRAGQueryClient(
        azure_openai_endpoint=endpoint,
        azure_openai_api_key=subscription_key,
        azure_openai_api_version=api_version,
        azure_ai_search_endpoint=search_endpoint,
        azure_ai_search_index=search_index,
        azure_ai_search_key=search_key
    )

    chat_completion = client.complete("What is the recommended dosage of amoxicillin for a child with pneumonia?")
    # Extract citations
    print(chat_completion)

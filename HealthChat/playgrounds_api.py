import os
import requests
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path


class AzurePlaygroundsQueryClient:
    def __init__(self) -> None:
        
        # Configuration
        load_dotenv()
        self.API_KEY = os.getenv("AZURE_ENDPOINT_API_KEY")
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        if not self.API_KEY:
            raise ValueError("No API key provided")
        else:
            logger.info("Loaded API key successfully")
        if not self.endpoint:
            raise ValueError("No endpoint provided")
        else:
            logger.info(f"Loaded endpoint successfully: {self.endpoint}")
        self.headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }
        self.system_prompt = {
            "type":"text",
            "text":Path("HealthChat/prompts/system.v1.txt").read_text()
        }

        self.messages = []

    def get_response(self, user_message):
        if len(self.messages) == 0:
            self.messages.append({"role": "system", "content": self.system_prompt})

        self.messages.append({
            "role": "user",
            "content": {
                "type":"text",
                "text":user_message
            }
        })

        payload = {
            "messages": self.messages,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
    
        ai_msg = response.json()
        self.messages.append({
            "role": "assistant",
            "content": ai_msg["choices"][0]["message"]["content"]
        })
        return self.messages[-1]["content"]
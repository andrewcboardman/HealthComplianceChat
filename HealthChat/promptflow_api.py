import urllib.request
import urllib.error
import json
import os
import ssl
from typing import Optional
from dotenv import load_dotenv


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


class AzurePromptflowQueryClient:
    def __init__(
            self,
            api_key: Optional[str] = os.getenv("AZURE_PROMPTFLOW_API_KEY"),
            endpoint: Optional[str] = os.getenv("AZURE_PROMPTFLOW_ENDPOINT")
        ) -> None:
        allowSelfSignedHttps(True)
        # this line is needed if you use self-signed certificate 
        # in your scoring service.
        self.endpoint = endpoint
        if not self.endpoint:
            raise ValueError("No endpoint provided")
        
        # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
        self.api_key = api_key
        if not self.api_key:
            raise Exception("A key should be provided to invoke the endpoint")
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': ('Bearer ' + self.api_key)
        }

    def query(self, data: dict):
        # Request data goes here
        # The example below assumes JSON formatting which may be updated
        # depending on the format your endpoint expects.
        # More information can be found here:
        # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

        body = str.encode(json.dumps(data))
        req = urllib.request.Request(
            self.endpoint,
            body,
            self.headers
        )

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            return result
        except urllib.error.HTTPError as error:
            raise ValueError(
                "The request failed with status code: "
                + str(error.code))


if __name__ == "__main__":
    load_dotenv()
    client = AzurePromptflowQueryClient(
        api_key=os.getenv("AZURE_PROMPTFLOW_API_KEY"),
        endpoint=os.getenv("AZURE_PROMPTFLOW_ENDPOINT")
    )
    response = client.query({
        "question": "How does the 10-Year Health Plan address the current workforce challenges within the NHS?"
        })
    print(response)
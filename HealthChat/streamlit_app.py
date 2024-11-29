import streamlit as st
# from promptflow_api import AzurePromptflowQueryClient
from playgrounds_api_index import AzureRAGQueryClient
from dotenv import load_dotenv
import os
import json

col1, _ = st.columns(2)

with col1:
    st.image("National_Health_Service_(England)_logo.svg")


# Set OpenAI API key from Streamlit secrets
if "promptflow_client" not in st.session_state:
    load_dotenv()
    endpoint = os.getenv(
        "ENDPOINT_URL",
        "YOUR_ENDPOINT_URL"
    )
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
    api_version = "2024-05-01-preview"
    search_endpoint = os.getenv(
        "SEARCH_ENDPOINT",
        "YOUR_SEARCH_ENDPOINT"
    )
    search_index = os.getenv(
        "SEARCH_INDEX",
        "YOUR_SEARCH_INDEX"
    )
    search_key = os.getenv(
        "SEARCH_KEY",
        "put your Azure AI Search admin key here"
    )
    subscription_key = os.getenv(
        "AZURE_OPENAI_API_KEY",
        "REPLACE_WITH_YOUR_KEY_VALUE_HERE"
    )

    st.session_state["client"] = AzureRAGQueryClient(
        azure_openai_endpoint=endpoint,
        azure_openai_api_key=subscription_key,
        azure_openai_api_version=api_version,
        azure_openai_deployment_name=deployment,
        azure_ai_search_endpoint=search_endpoint,
        azure_ai_search_index=search_index,
        azure_ai_search_key=search_key
    )

tab1, tab2 = st.tabs(["About me", "Ask a question"])

with tab1:
    st.title("About me")
    st.write(
        """
        I am a chatbot designed to help you with any questions you have about the NHS. 
        I am powered by Azure's Promptflow API, which uses a language model to generate responses to your questions. 
        Feel free to ask me anything you want to know about the NHS!
        """
    )

with tab2:
    # Accept user input
    if prompt := st.chat_input("What's up, NHS web chat?"):
        # Clear chat history on new question
        st.session_state.messages = []
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            try: 
                response = st.session_state["client"].complete(prompt)

                context_string = ""
                for i, citation in enumerate(response["context"]):
                    context_string += \
                        f"""\n**Citation {i}**\n<details open>\n\n{citation['content']}\n\n</details>\n\n"""

                response_string = f"""
                {response["content"]}
                ## Citations
                {context_string}
                """
                response = st.write(response_string)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                st.write(f"An error occurred: {e}")
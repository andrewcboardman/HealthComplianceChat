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
        "Your Azure OpenAI endpoint URL"
    )
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
    api_version = "2024-05-01-preview"
    search_endpoint = os.getenv(
        "SEARCH_ENDPOINT",
        "Your Azure AI Search endpoint URL"
    )
    search_index = os.getenv(
        "SEARCH_INDEX",
        "Your Azure AI Search index name"
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
        Welcome to NHS Webchat!
 
        This is a tool to support with finding information from the england.nhs.uk 
        website. 
        
        You can ask questions and the tool will review the website, summarise 
        its findings and give a concise answer.
        
        It will provide citations for the information provided - you should 
        review these before acting on the advice given by the tool.
        """
    )

with tab2:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if 'await_response' not in st.session_state:
        st.session_state.await_response = False

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                expander = st.expander("Citations")
                for i, citation in enumerate(message["citations"]):
                    expander.write(f"# Citation {i}")
                    expander.write(citation['content'])

    # Generate new messages from the chatbot
    if st.session_state.await_response:
        st.session_state.await_response = False
        with st.chat_message("assistant"):
            try:
                prompt = st.session_state.messages[-1]["content"]
                response = st.session_state["client"].complete(prompt)
                st.markdown(response["content"])
                expander = st.expander("Citations")
                for i, citation in enumerate(response["context"]):
                    expander.write(f"# Citation {i}")
                    expander.write(citation['content'])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["content"],
                    "citations": response["context"]
                })

            except Exception as e:
                st.write(f"An error occurred: {e}")

    # Input box for user
    prompt = st.chat_input("What is up?", key="chat_input")

    # React to user input
    if prompt:
        # User message
        # st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.await_response = True
        # Rerun to generate messages above
        st.rerun()  

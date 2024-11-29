# NHS Website Compliance Chat

This repo contains scripts from a hackathon where NHSE collaborated with Microsoft and Kainos. The working app uses the Azure AI Studio Playgrounds API which is quite slow. To run, 
* add appropriate keys and endpoints to .env, as specified in `HealthChat/playgrounds_api_index.py`
* make a virtual Python environment and activate it (I used Python 3.12)
* Install the required packages (`pip install requirements.txt`)
* Run the app by typing `streamlit run HealthChat/streamlit_app_v2.py` on Windows or `make run` on Linux/MacOS.

🚀 Getting Started
This project uses Python to create a chatbot that answers medical questions based on a provided PDF document. It leverages a Retrieval-Augmented Generation (RAG) approach, combining a vector database (Pinecone) for information retrieval with a Large Language Model (LLM) for conversational responses.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8 or higher: The project is built using Python, so you'll need it installed on your system.

Ollama: This is required to run the mistral LLM locally. Make sure Ollama is installed and running on your machine. You can download it from ollama.com.

🛠️ Installation
Follow these steps to set up the project locally.

1. Clone the repository
First, clone this repository to your local machine.

Bash

git clone https://github.com/harshita-313/Medical-Assistant-Chatbot
2. Install dependencies
Install all the required Python packages using pip. The dependencies are listed in the requirements.txt file.

pip install -r requirements.txt
3. Set up environment variables
Create a file named .env in the root directory of the project. This file will store your Pinecone API key.

PINECONE_API_KEY="YOUR_API_KEY_HERE"
Replace "YOUR_API_KEY_HERE" with your actual Pinecone API key.  You can get one by signing up for a free account on the Pinecone website.

4. Download the LLM
This project uses the mistral model from Ollama. You need to pull this model before you can run the application.

ollama pull mistral
🤖 How to Run the App
Once everything is set up, you can start the chatbot.

1. Ingest the data
Run the chatbot.py script once. This script will:

Read the medical PDF (The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf).

Split the text into smaller chunks.

Create embeddings for each chunk.

Upsert (upload) these embeddings into your Pinecone vector database.

This step can take a few minutes depending on the size of the PDF and your internet connection.

python chatbot.py (Run the file)
2. Launch the Streamlit application
After the data has been ingested, you can run the Streamlit app.

streamlit run app.py (Run the UI file)
This command will open a new browser tab with the Streamlit interface for your medical assistant chatbot. You can now type in your medical queries and get responses.

📁 Project Structure
chatbot.py: Contains the core logic for data ingestion, setting up the RAG chain, and defining the get_answer function.

app.py: The Streamlit application that provides the user interface for the chatbot.

data/: Directory where the source PDF file (The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf) is stored.

.env: The file to store your Pinecone API key.

requirements.txt: Lists all the necessary Python dependencies.

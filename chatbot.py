import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone, ServerlessSpec
from langchain_community.llms import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# LOAD ENV FILE
load_dotenv()
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']

data = PdfReader('data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf')

# GET THE TEXT OUT OF THE PDF FILE
text=""
for page in data.pages:
    data_text = page.extract_text()
    if data_text:
        text += data_text + " "

# SPLITTING DATA INTO CHUNKS
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
chunks = splitter.split_text(text)

# CONVERT THE CHUNKS TO EMBEDDINGS USING SENTENCE TRANSFORMERS
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# SETTING UP PINECONE

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("medical-data")

index_name = "medical-data"  # index name

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# UPSERT THE EMBEDDING INTO PINECONE INDEX (TO UPLOAD ALL YOUR CHUNKS TO THE PINECONE VECTORDB)
docsearch = PineconeVectorStore.from_texts (
    texts=chunks,
    index_name=index_name,
    embedding=embedding_function
)

# LOAD EXISTING PINECONE INDEX FOR SEARCH/RETRIEVAL
docsearch = PineconeVectorStore.from_existing_index (
    index_name=index_name,
    embedding=embedding_function
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3, "score_threshold": 0.4},
)

# retrieved_docs = retriever.invoke("What is osteoarthritis ?") (TO TEST THE RESULTS)
# print (retrieved_docs)

# INTEGRATE LLM FOR BETTER CONVERSATION
llm = Ollama(model="mistral") # Loading the Mistral model

# SYSTEM MESSAGE
system_prompt = (
    "You are a medical assistant chatbot."
    "Use the pieces of retrieved content to answer the questions."
    "If the answer is not in the context, reply strictly and do not add anything else: "
    "'Sorry, not found in my medical database.' "
    "Use three senetences maximum to answer the question and keep the answer really very concise and easy"
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# INTIALIZING THE CHAIN 
question_answer_Chain = create_stuff_documents_chain(llm,prompt)
rag_Chain = create_retrieval_chain(retriever,question_answer_Chain)

response = rag_Chain.invoke({"input": "Hi, How are you ?"})
print (response["answer"])

# Function to get chatbot response
def get_answer(query: str) -> str:
    response = rag_Chain.invoke({"input": query})
    return response["answer"]
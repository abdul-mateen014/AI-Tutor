from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter

# Fast + lightweight model
embedding = OllamaEmbeddings(model="llama3")
model = ChatOllama(model="llama3")

def build_qa_chain(docs):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    vectordb = Chroma.from_documents(chunks, embedding)
    retriever = vectordb.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever)
    
    return chain

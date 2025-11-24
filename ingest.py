from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Define o caminho para os dados e para o banco de dados
DATA_PATH = "data/"
DB_PATH = "chroma_db"

def create_vector_db():
    """
    Função principal para carregar os dados, processá-los e
    armazená-los no ChromaDB.
    """
    
    # Carregar os documentos
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    
    # Dividir os documentos em "chunks" (pedaços)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    # Selecionar o modelo de embeddings (local e gratuito)
    # 'all-MiniLM-L6-v2' é rápido e leve.
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    
    # Criar o banco de dados vetorial e salvá-lo
    print("Criando e persistindo o banco de dados vetorial...")
    vectordb = Chroma.from_documents(documents=texts, 
                                     embedding=embeddings,
                                     persist_directory=DB_PATH)
    
    print(f"Banco de dados criado com sucesso em {DB_PATH}!")
    print(f"Total de {len(texts)} chunks de texto processados.")

if __name__ == "__main__":
    create_vector_db()

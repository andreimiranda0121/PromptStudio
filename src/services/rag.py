from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.document_loaders import CSVLoader,PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import hashlib

class VectorStore:
    def __init__(self,model, email, prompt_id, file_path: str):
        self.model = model
        self.email = email
        self.prompt_id = prompt_id
        self.file_path = file_path
        self.email_hash = self.email_to_short_hex()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join("database", "chroma_db")
        self.persistent_directory = os.path.join(self.root_dir, "..",self.base_dir, self.email_hash, self.prompt_id)
        self.embeddings = self.check_embeddings()

    def email_to_short_hex(self):
        hash_object = hashlib.sha256(self.email.encode())
        return hash_object.hexdigest()[:16]  # 16 hex characters (8 bytes)

    def check_embeddings(self):
        if "gpt" in self.model.lower():
            return OpenAIEmbeddings(
                model="text-embedding-ada-002"
            )
        else:
            return GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004"
            )

    def split_docs(self):
            if os.path.exists(self.file_path):
                ext = os.path.splitext(self.file_path)[-1].lower()
                if ext == ".csv":
                    print("Loading the CSV File")
                    loader = CSVLoader(self.file_path)
                elif ext in [".pdf"]:
                    print("Loading the PDF File")
                    loader = PyMuPDFLoader(self.file_path)
                else:
                    raise ValueError(f"Unsupported file type: {ext}")

                docs = loader.load()
                print("Splitting text into chunks...")
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_overlap=200,
                    chunk_size=1500
                )
                return text_splitter.split_documents(docs)
            else:
                raise FileNotFoundError(f"The file does not exist: {self.file_path}")

    def create_vector_store(self):
        if not os.path.exists(self.persistent_directory):
            print("---Persistent does not exist yet. Creating new vector store ---")
            docs = self.split_docs()
            db = Chroma.from_documents(
                docs,self.embeddings,persist_directory=self.persistent_directory
            )
            print("--- Finished Creating Vector Store ---")

            return db
        else:
            print("Vector store already exists. Loading ......")
            db = Chroma(
                persist_directory=self.persistent_directory,
                embedding_function=self.embeddings
            )
            return db
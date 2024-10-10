from langchain.docstore.document import Document
import sqlite3  
import time
import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

load_dotenv()

activeloop_token = os.getenv("ACTIVELOOP_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")


class DeeplakeStorage:
    
    def __init__(self):
        self.activeloop_org = "<YOUR_ACTIVELOOP_ORGANISATION NAME" # replace with your ActiveLoop organisation name
        self.activeloop_dataset = "<DATASET_NAME>" # replace with your ActiveLoop dataset name you want to be created
        self.dataset_path = f"hub://{self.activeloop_org}/{self.activeloop_dataset}"
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.db = None
        self.docs = []
        self.init_db() 

    def init_db(self):
        conn = sqlite3.connect('baseUrl_embeddingId.db', timeout=10)  
        conn.execute('PRAGMA busy_timeout = 5000') 
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS baseUrl_embeddingId (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_url TEXT,
                embeddingId TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_base_url_embeddingId(self, base_url, ids):
        conn = sqlite3.connect('baseUrl_embeddingId.db', timeout=10)
        c = conn.cursor()
        for id in ids:
            c.execute('INSERT INTO baseUrl_embeddingId (base_url, embeddingId) VALUES (?, ?)', (base_url, id))
        conn.commit()
        conn.close()

    def get_all_base_url_embeddingId(self):
        conn = sqlite3.connect('baseUrl_embeddingId.db', timeout=10)
        c = conn.cursor()
        c.execute('SELECT base_url, embeddingId FROM baseUrl_embeddingId')
        result = c.fetchall()
        conn.close()
        return result

    def get_embeddingIds(self, base_url):
        conn = sqlite3.connect('baseUrl_embeddingId.db', timeout=10)
        c = conn.cursor()
        c.execute('SELECT embeddingId FROM baseUrl_embeddingId WHERE base_url = ?', (base_url,))
        result = [row[0] for row in c.fetchall()]
        conn.close()
        return result

    def delete_base_url_embeddingId(self, base_url):
        conn = sqlite3.connect('baseUrl_embeddingId.db', timeout=10)
        c = conn.cursor()
        c.execute('DELETE FROM baseUrl_embeddingId WHERE base_url = ?', (base_url,))
        conn.commit()
        conn.close()

    # Create/Insert into dataset with the provided documents
    def create_dataset(self, docs, base_url):
        self.db = DeepLake(dataset_path=self.dataset_path, embedding_function=self.embeddings)
        ids = self.db.add_documents(docs)

        for id in ids:
            self.insert_base_url_embeddingId(base_url, [id])

        base_url_and_embeddingId = self.get_all_base_url_embeddingId()

        print(f"----{base_url_and_embeddingId}-----")
        
        for row in base_url_and_embeddingId:
            print(f"Base URL: {row[0]}, Embedding ID: {row[1]}")

        self.docs = docs
        return self.db

    # Load the dataset
    def load_dataset(self):
        try:
            self.db = DeepLake(dataset_path=self.dataset_path, embedding_function=self.embeddings)
            print(f"Loaded dataset.")
            if self.db is not None:
                return self.db  
            else:
                return None
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None 

    # Delete from the dataset
    def delete_from_dataset(self, base_url):
        ids = self.get_embeddingIds(base_url)
        self.db.delete(ids=ids)
        self.delete_base_url_embeddingId(base_url)

        base_url_and_embeddingId = self.get_all_base_url_embeddingId()

        if len(base_url_and_embeddingId) == 0:
            print("All base URLs and their embedding IDs have been deleted.")
    
        return self.db

            
        

    
import pandas as pd
import chromadb
import uuid 


class Portfolio:
    def __init__(self, file_path="apps/resources/my_resume.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    
    def load_portfolio(self):
        if not self.collection.count():
            for _,row in self.data.iterrows():
                self.collection.add(documents=[row['Section']],
                    metadatas=[{"details": row['Details']}],
                                ids=[str(uuid.uuid4())])   
                                   

    def query_links(self, skills):
        result_list=[]
        for key, value in skills[0].items():
            value = self.collection.query(query_texts=key, n_results=2).get('metadatas', [])
            result_list.append(value)
        return result_list[0]

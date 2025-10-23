from typing import List, Optional, Any
import os
from pptx import Presentation


from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rag.base import RetrievalChain

class pdfToVectorDb_RetrievalChain(RetrievalChain):
    def __init__(self, 
                    source_uri: List[str], 
                    persist_directory: Optional[str] = None,
                    **kwargs) -> None:

        super().__init__(source_uri=source_uri, persist_directory="C:\qdrant\qdrant_storage", **kwargs)
    
    def load_documents(self, source_uris: List[str]) -> List[Document]:
        docs = []
        for i,source_uri in enumerate(source_uris):
            if not os.path.exists(source_uri):
                print(f"File not found: {source_uri}")
                continue
                
            print(f"Loading PDF {i} : {source_uri}")
            loader = PDFPlumberLoader(source_uri)
            docs.extend(loader.load())

        return docs
    
    def create_text_splitter(self) -> RecursiveCharacterTextSplitter:
        return RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50
        )
    
    def create_vectorstore(self, split_docs: List[Document]) -> Any:
        if not split_docs:
            raise ValueError("No split documents available.")
            
        if self.persist_directory:
            os.makedirs(self.persist_directory, exist_ok=True)
            
            if os.path.exists(self.persist_directory) and any(os.listdir(self.persist_directory)):
                print(f"Loading existing vector store: {self.persist_directory}")

        # client = QdrantClient(url="http://localhost:6333",api_key="45e4600ad1ed2fd63a446570af9fbe0a7a8260614448452e7f03a509341c473f")
        vectorstore = Qdrant.from_documents(
            documents=split_docs,
            embedding=self.create_embedding(),
            collection_name="pdf_collection_test",
            url="http://localhost:6333",  # 여기 반드시 문자열
            api_key="45e4600ad1ed2fd63a446570af9fbe0a7a8260614448452e7f03a509341c473f",       # 없으면 None
        )
        
        return vectorstore
# ChromaDB Vector Memory

from chromadb.config import Settings
import chromadb
from typing import List, Dict
import uuid


class VectorMemory:
    """Vector database for agent knowledge storage"""
    
    def __init__(self, collection_name: str = "knowledge"):
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            is_persistent=True
        ))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    async def store(self, text: str, metadata: Dict = None):
        """Store knowledge in vector database"""
        self.collection.add(
            documents=[text],
            ids=[str(uuid.uuid4())],
            metadatas=[metadata or {}]
        )
    
    async def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant knowledge"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    async def get_stats(self) -> Dict:
        """Get memory statistics"""
        return {
            "total_items": self.collection.count()
        }


# Global memory instance
memory = VectorMemory()

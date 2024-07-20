from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from google.cloud import firestore

@dataclass
class FirestoreDocument:
    id: str
    data: Dict[str, Any]

@dataclass
class Firestore:
    db: Any = field(default_factory=firestore.Client)

    # def add_document(self, collection: str, data: Dict[str, Any]) -> FirestoreDocument:
    #     """
    #     Agrega un nuevo documento a una colección y devuelve un FirestoreDocument.
    #     """
    #     doc_ref = self.db.collection(collection).add(data)
    #     return FirestoreDocument(id=doc_ref[1].id, data=data)
    
    def document_exists(self, collection: str, doc_id: str) -> bool:
        """
        Checks if a document with the given ID exists in the specified collection.
        """
        doc_ref = self.db.collection(collection).document(doc_id)
        return doc_ref.get().exists

    def add_document(self, collection: str, data: Dict[str, Any], doc_id: Optional[str] = None) -> FirestoreDocument:
        """
        Adds a new document to a collection with an optional document ID and returns a FirestoreDocument.
        If the document ID is provided and already exists, it raises an exception.
        """
        if doc_id:
            if self.document_exists(collection, doc_id):
                raise ValueError(f"Document with ID {doc_id} already exists in collection {collection}")
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_ref.set(data)
        else:
            doc_ref = self.db.collection(collection).add(data)[1]
        
        return FirestoreDocument(id=doc_ref.id, data=data)
    

    def get_document(self, collection: str, doc_id: str) -> Optional[FirestoreDocument]:
        """
        Obtiene un documento por su ID.
        """
        doc_ref = self.db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        return FirestoreDocument(id=doc_id, data=doc.to_dict()) if doc.exists else None

    def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> None:
        """
        Actualiza un documento existente.
        """
        self.db.collection(collection).document(doc_id).update(data)

    def delete_document(self, collection: str, doc_id: str) -> None:
        """
        Elimina un documento por su ID.
        """
        self.db.collection(collection).document(doc_id).delete()

    def query_collection(self, collection: str, filters: List[tuple]) -> List[FirestoreDocument]:
        """
        Realiza una consulta en una colección con filtros dados.
        """
        query = self.db.collection(collection)
        for field, op, value in filters:
            query = query.where(field, op, value)
        docs = query.stream()
        return [FirestoreDocument(id=doc.id, data=doc.to_dict()) for doc in docs]
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from google.cloud import firestore
from classes.users_class import Users
from google.cloud.firestore_v1.base_query import FieldFilter, Or, And

@dataclass
class FirestoreDocument:
    id: str
    data: Dict[str, Any]

@dataclass
class Firestore:
    db: Any = field(default_factory=firestore.Client)
    
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
            self.db.collection(collection).document(doc_ref.id).update({'cloud_id':doc_ref.id})

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

        filter_list = []
        for field, op, value in filters:
            filter_list.append(FieldFilter(field, op, value))
        
        filters_summary = And(filters=filter_list)
        docs = self.db.collection(collection).where(filter=filters_summary).stream()
        
        return [FirestoreDocument(id=doc.id, data=doc.to_dict()) for doc in docs]

    def auth_firestore(self, email: str, password: str) -> Optional[Users]:
        try:
            query = self.db.collection('users_collection')
            email_filter = FieldFilter("email", "==", email)
            password_filter = FieldFilter("password", "==", password)

            combined_filter = And(filters=[email_filter, password_filter])
            
            results = list(query.where(filter=combined_filter).limit(2).stream())
            
            if len(results) == 0 or len(results) > 1:
                return None
            else:
                user_data = results[0].to_dict()
                return user_data
        except Exception as e:
            print(f"Error in authentication: {str(e)}")
            return None
    
    @staticmethod
    def hide_characters(element):
            """
            Hide Characters to Secure & Remind User's Account 
            """
            exposed_field = element
            hidden_field = exposed_field[3:-3]
            return exposed_field.replace(hidden_field,'*'*(len(hidden_field) + 2))

    def signup_preauth(self,app_email:str, app_id_user:str,app_phone_number:str):
        """
        Authenticate (Sign Up) Before Instance On Firestore
        """
        try: 
                id_filter = FieldFilter('id_user','==',app_id_user)
                phone_filter = FieldFilter('phone_number','==',app_phone_number)
                email_filter = FieldFilter('email','==',app_email)
                signup_filter = Or(filters=[id_filter, phone_filter, email_filter])
                
                query_auth = (
                        self.db.collection('users_collection')
                        .where(filter=signup_filter)
                        .stream()
                )

                firestore_fetched = {value.id: value.to_dict() for value in query_auth}
                cloud_id = list(firestore_fetched.keys())[0]
                data_fetched = list(firestore_fetched.values())[0]                        

                return {'status':'signup_disapproved',
                        'D.I.':self.hide_characters(data_fetched['id_user']),
                        'Teléfono':self.hide_characters(data_fetched['phone_number']),
                        'Correo':self.hide_characters(data_fetched['email'])}

        except IndexError as e:
                return {'status':'sigup_approved'}
        


    def update_firestore_profile(self,connection):
                """
                Update Users Profile Atributes On Firestore
                """
                return connection.collection('users_collection').document(self.cloud_id).set(asdict(self))
                        

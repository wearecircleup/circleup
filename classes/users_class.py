from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from dataclasses import dataclass, field, fields, asdict
from typing import List
import streamlit as st

@dataclass
class Users:        
        first_name: str = None
        last_name: str = None
        email: str = None
        password: str = None
        address: str = None
        phone_number: str = None
        dob: str = None
        gender: str = None
        nationality:str = None
        id_user: int = None
        id_user_type: str = None
        is_ethnic:str = None
        city_residence: str = None
        guardian_fullname: str = None
        guardian_relationship: str = None
        guardian_id: int = None
        guardian_id_type: str = None
        emergency_phone: int = None
        education_level: str = None
        data_sharing: bool = None
        user_status: str = 'Activo'
        user_role: str = 'Learner'
        strengths: List[str] = field(default_factory=list)
        weaknesses: List[str] = field(default_factory=list)
        topics_interest: List[str] = field(default_factory=list)
        disability: List[str] = field(default_factory=list) 
        ethnic_affiliation: List[str] = field(default_factory=list) 
        skills: List[str] = field(default_factory=list)
        how_to_learn: List[str] = field(default_factory=list)
        cloud_id:str = None
        autho:str = None
        parental_consent:str = 'Pending'

        # NotApplicable = "Not Applicable"
        # Pending = "Pending",
        # Authorized = "Authorized"

        def as_dict(self):
                """
                Alternative Method To Dict Instances
                """
                # return asdict(self)   
                return {field.name: getattr(self,field.name) for field in fields(self)}

        def user_authentication(self,app_email:str, app_password:str,connection):
                """
                Authenticate (Log In) Before Let User's In
                """
                try: 
                        query_auth = (
                                connection.collection('users_collection')
                                .where(filter=FieldFilter('email','==',app_email))
                                .where(filter=FieldFilter('password','==',app_password))
                                .stream()
                        )

                        firestore_fetched = {value.id: value.to_dict() for value in query_auth}
                        cloud_id = list(firestore_fetched.keys())[0]
                        data_authenticated = list(firestore_fetched.values())[0]
                        data_authenticated['cloud_id'] = cloud_id
                        
                        return self.update_profile(**data_authenticated)

                except IndexError as e:
                        return 'Log In Error'

        @staticmethod
        def hide_characters(element):
                """
                Hide Characters to Secure & Remind User's Account 
                """
                exposed_field = element
                hidden_field = exposed_field[3:-3]
                return exposed_field.replace(hidden_field,'*'*(len(hidden_field) + 2))

        def signup_authentication(self,app_email:str, app_id_user:str,app_phone_number:str,connection):
                """
                Authenticate (Sign Up) Before Instance On Firestore
                """
                try: 
                        id_filter = FieldFilter('id_user','==',app_id_user)
                        phone_filter = FieldFilter('phone_number','==',app_phone_number)
                        email_filter = FieldFilter('email','==',app_email)
                        signup_filter = Or(filters=[id_filter, phone_filter, email_filter])
                        
                        query_auth = (
                                connection.collection('users_collection')
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
        

        @staticmethod
        def successful_signup(data, connection):
                """
                Upload Profile Attributes On Firestore (Sign Up) and Update cloud_id
                """
                doc_ref = connection.collection('users_collection').add(data)
                cloud_id = doc_ref[1].id
                doc_ref[1].update({'cloud_id': cloud_id})
                
                return doc_ref


        def update_firestore_profile(self,connection):
                """
                Update Users Profile Atributes On Firestore
                """
                return connection.collection('users_collection').document(self.cloud_id).set(asdict(self))
                        
        def update_profile(self,**kwargs):
                """
                Update Users Profile Atributes On Session
                """
                for key,value in kwargs.items():
                        if hasattr(self,key):
                                setattr(self,key,value)

        def catch_profile_updates(self,**kwargs):
                """
                Update Users Profile Atributes On Session
                """
                catch_changes = {}
                for key,value in kwargs.items():
                        if hasattr(self,key):        
                                catch_changes[key] = [value,getattr(self,key)]
                for _ ,value in catch_changes.items():
                        if value[0] == value[1]:
                                value.append(False)
                        else: value.append(True)
                return catch_changes               


        
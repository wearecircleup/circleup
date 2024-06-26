from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from dataclasses import dataclass, field, fields, asdict
from dataclasses import dataclass, field
from typing import List,Dict

@dataclass
class Course:
        user_profile: Dict[str,str] = field(default_factory=dict)
        press_title: str = None
        press_slogan: str = None
        course_name: str = None
        course_description: str = None
        course_categories: List[str] = field(default_factory=list)
        target_population: List[str] = field(default_factory=list)
        course_prerequisites: Dict[str,bool] = field(default_factory=dict)
        course_status: str = 'Proposal Mode'
        course_notification_status: str = 'No Required'
        course_place:str = 'To Assign'
        date_specs:str = 'To Assign'
        min_audience: int = None
        max_audience: int = None
        cloud_id:str = None

        def update_course(self,**kwargs):
                """
                Update Course Atributes On Session
                """
                for key,value in kwargs.items():
                        if hasattr(self,key):
                                setattr(self,key,value)

        def update_firestore_course(self,connection):
                """
                Update Course Atributes On Firestore
                """
                return connection.collection('course_collection').document(self.cloud_id).set(asdict(self))

        def upload_course(self,connection,course,mail):
                """
                Upload Course Atributes On Firestore (Instance Course) 
                """
                enrollattr = {
                                'course_name':course,
                                'email':mail,
                                'counter':0
                        }
                
                query_auth = (
                                connection.collection('course_collection')
                                .where(filter=FieldFilter('user_profile.email','==',self.user_profile['email']))
                                .where(filter=FieldFilter('course_name','==',self.course_name))
                                .stream()
                        )
                fetched_data = {value.id: value.to_dict() for value in query_auth}

                if len(fetched_data) > 0:
                        raise PermissionError('disapprove_reupload')
                else:
                        connection.collection('counter_collection').add(enrollattr)
                        connection.collection('course_collection').add(asdict(self))
        
        

        @staticmethod
        def search_courses(app_email:str,app_user_id:str,app_role:str,connection):
                """
                Search Courses Filter User Preferences
                """
                try: 
                        query_auth = (
                                connection.collection('course_collection')
                                .where(filter=FieldFilter('user_profile.email','==',app_email))
                                .where(filter=FieldFilter('user_profile.id_user','==',app_user_id))
                                .where(filter=FieldFilter('user_profile.user_role','==',app_role))
                                .stream()
                        )
                        firestore_fetched = {value.id: value.to_dict() for value in query_auth}
                        
                        return firestore_fetched

                except IndexError as e:
                        return {}

        @staticmethod
        def available_courses(connection):
                """
                Search Courses Filter User Preferences
                """
                try: 
                        query_auth = (connection.collection('course_collection').stream())
                        firestore_fetched = {value.id: value.to_dict() for value in query_auth}
                        return firestore_fetched

                except IndexError as e:
                        return {}
                
        def catch_course_updates(self,**kwargs):
                """
                Find Course Changes On Session
                """
                alter_values = {}
                catch_changes = {}

                for key,value in kwargs.items():
                        if hasattr(self,key):        
                                alter_values[key] = [value,getattr(self,key)]
                        
                        for key,value in alter_values.items():
                                if value[0] != value[1]:
                                        catch_changes[key] = value       

                return catch_changes               
        
        @staticmethod
        def delete_course(id,connection):
                """
                Delete Course @Nomad Session
                """
                connection.collection('course_collection').document(id).delete()
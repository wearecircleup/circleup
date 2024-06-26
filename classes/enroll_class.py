from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from dataclasses import dataclass, field, fields, asdict
from dataclasses import dataclass, field
from typing import List,Dict

@dataclass
class Enrollment:
        user_profile: Dict[str,str] = field(default_factory=dict)
        volunteer_profile:Dict[str,str] = field(default_factory=dict)
        course_content: Dict[str,str] = field(default_factory=dict)
        cloud_id:str = None

        def update_enrollment(self,**kwargs):
                """
                Update Course Atributes On Session
                """
                for key,value in kwargs.items():
                        if hasattr(self,key):
                                setattr(self,key,value)

        @staticmethod
        def unrollment(course_id,course_name,email,connection):
                """
                Uneroll Course Atributes From Firestore
                """
                #Update Counter
                query_counter = (
                                connection.collection('counter_collection')
                                .where(filter=FieldFilter('email','==',email))
                                .where(filter=FieldFilter('course_name','==',course_name))
                                .stream()
                        )
                        
                
                counter_fetched = {value.id: value.to_dict() for value in query_counter}
                data_counter = list(counter_fetched.values())[0]

                document_id = list(counter_fetched.keys())[0]
                data_counter['counter'] -= 1 

                connection.collection('counter_collection').document(document_id).set(data_counter)

                #Delete Enrollment
                connection.collection('enrollment_collection').document(course_id[0]).delete()
        
        def upload_enrollment(self,counter,connection):
                """
                Upload Course Atributes On Firestore (Instance Course)
                """
                counter_ref = connection.collection('counter_collection').document(counter).get().to_dict()
                counter_ref['counter'] += 1 

                connection.collection('enrollment_collection').add(asdict(self))
                connection.collection('counter_collection').document(counter).set(counter_ref)

        def get_enrollments(self,email,connection):
                query_enrollmet = (
                        connection.collection('enrollment_collection')
                        .where(filter=FieldFilter('user_profile.email','==',email))
                        .stream()
                )

                courses_fetched = {value.id: value.to_dict() for value in query_enrollmet}
                return courses_fetched
                

        def enroll_authentication(self,app_target_age,email,course,connection):
                """
                Authenticate Enrollment Before Let User's In
                """
                auth_message = {}
                try: 
                        # max_audience = self.course_content['max_audience'] # Crear un Contador Interno 
                        query_counter = (
                                connection.collection('counter_collection')
                                .where(filter=FieldFilter('email','==',email))
                                .where(filter=FieldFilter('course_name','==',course))
                                .stream()
                        )
                        
                        counter_fetched = {value.id: value.to_dict() for value in query_counter}
                        if len(counter_fetched) > 0:
                                data_counter = list(counter_fetched.values())[0]
                                document_id = list(counter_fetched.keys())[0]
                
                                if int(self.course_content['max_audience']) >= int(data_counter['counter']) + 1:
                                        auth_message['audience'] = document_id
                                else:
                                        auth_message['audience'] = None
                        else:
                                auth_message['audience'] = None

                        query_enrollmet = (
                                connection.collection('enrollment_collection')
                                .where(filter=FieldFilter('user_profile.email','==',self.user_profile['email']))
                                .where(filter=FieldFilter('course_content.course_name','==',self.course_content['course_name']))
                                .stream()
                        )
                        enroll_fetched = {value.id: value.to_dict() for value in query_enrollmet}
                        
                        if app_target_age in self.course_content['target_population']:
                                auth_message['target_age'] = True
                        else:
                                auth_message['target_age'] = False
                        
                        if len(enroll_fetched) > 0:
                                if len(enroll_fetched) > 0 and enroll_fetched is not None:
                                        auth_message['enrolled'] = True
                                else: 
                                        auth_message['enrolled'] = False
                        else:
                                auth_message['enrolled'] = False

                                
                        
                        return auth_message

                except IndexError as e:
                        return 'Log In Error'
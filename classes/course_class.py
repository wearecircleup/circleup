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

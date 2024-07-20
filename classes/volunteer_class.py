from dataclasses import dataclass, field, asdict, astuple, fields
from typing import List
from classes.users_class import Users

@dataclass
class Volunteer(Users):
    education_experience: str = None
    work_experience: str = None
    skills: List[str] = field(default_factory=list)
    keywords_volunteer: List[str] = field(default_factory=list)
    # is_volunteer: bool = True # Conditionate rols by asking, Are you sure?

from dataclasses import dataclass, field, asdict, fields
from typing import List
from classes.users_class import Users

@dataclass
class Learner(Users):
    weaknesses: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    # is_learner: bool = True # Conditionate rols by asking, Are you sure?
from dataclasses import dataclass, field, asdict, fields
from typing import List
from classes.users_class import Users

@dataclass
class Admin(Users):
    assigned_deparment: str = None
    admin_level: str = None
    permissions: List[str] = field(default_factory=list)
    # is_admin: bool = True # Conditionate rols by asking, Are you sure?

from pydantic import BaseModel

class Enterprise_Item(BaseModel):
    full_name: str
    short_name: str
    objects_current_state: str
    code_of_enterprise: str
    date_of_creation: str
    age_of_enterprise: str

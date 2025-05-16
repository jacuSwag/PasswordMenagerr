from pydantic import BaseModel

class PasswordCreate(BaseModel):
    service: str
    login: str
    password: str

class PasswordOut(PasswordCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

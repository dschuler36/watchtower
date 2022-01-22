from pydantic import BaseModel


class Dataset(BaseModel):
    name: str
    storage_platform: str
    notification_email: str

    class Config:
        orm_mode = True

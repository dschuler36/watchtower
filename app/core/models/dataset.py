from pydantic import BaseModel


class AggStructure(BaseModel):
    name: str
    data_type: str


class Dataset(BaseModel):
    name: str
    notification_email: str
    agg_structure: list[AggStructure]

    class Config:
        orm_mode = True


class AggUpdate(BaseModel):
    dataset_name: str
    agg_values: list[dict]

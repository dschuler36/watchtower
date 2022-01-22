from sqlalchemy.orm import Session
from app.core import db_models 
from app.core.models.dataset import Dataset


def get_dataset_by_id(db: Session, dataset_id: int):
    return db.query(db_models.Dataset).filter(db_models.Dataset.id == dataset_id).first()


def get_dataset_by_name(db: Session, name: str):
    return db.query(db_models.Dataset).filter(db_models.Dataset.name == name).first()


def create_dataset(db: Session, dataset: Dataset):
    db_dataset = db_models.Dataset(**dataset.dict())
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

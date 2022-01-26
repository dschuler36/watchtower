from sqlalchemy.orm import Session
from app.core import db_models 
from app.core.models.dataset import Dataset, AggUpdate
from sqlalchemy import Table, Column, Integer, String, Float, MetaData


def get_dataset_by_id(db: Session, dataset_id: int):
    return db.query(db_models.Dataset).filter(db_models.Dataset.id == dataset_id).first()


def get_dataset_by_name(db: Session, name: str):
    return db.query(db_models.Dataset).filter(db_models.Dataset.name == name).first()


def create_dataset(db: Session, dataset: Dataset):
    db_dataset = db_models.Dataset(dataset.name, dataset.notification_email)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    create_agg_table(db, dataset)
    return db_dataset


def insert_agg_value(db: Session, agg_update: AggUpdate):
    table = _get_dynamic_table(db, agg_update.dataset_name)
    db.execute(table.insert(), agg_update.agg_values)
    db.commit()
    return


def create_agg_table(db: Session, dataset: Dataset):
    datatype_mapping = {
        "string": String,
        "integer": Integer,
        "float": Float
    }
    metadata = MetaData(bind=db.bind)
    columns = [Column(c.name, datatype_mapping.get(c.data_type)) for c in dataset.agg_structure]
    table = Table(dataset.name,
                  metadata,
                  *columns)
    table.create()
    return


def _get_dynamic_table(db: Session, table_name: str):
    meta = MetaData()
    meta.reflect(db.bind)
    table = meta.tables[table_name]
    return table

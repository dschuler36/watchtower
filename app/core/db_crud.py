import pandas as pd
from sqlalchemy.orm import Session
from app.core import db_models 
from app.core.models.dataset import Dataset, AggUpdate
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from fastapi import HTTPException


def get_dataset_by_id(db: Session, dataset_id: int):
    return db.query(db_models.Dataset).filter(db_models.Dataset.id == dataset_id).first()


def get_dataset_by_name(db: Session, name: str):
    return db.query(db_models.Dataset).filter(db_models.Dataset.name == name).first()


def create_dataset(db: Session, dataset: Dataset):
    try:
        create_agg_table(db, dataset)
    except Exception as e:
        raise HTTPException(status_code=422,
                            detail=f"Problem creating agg table for {dataset}. Error: {e}")

    try:
        db_dataset = db_models.Dataset(dataset.name, dataset.notification_email)
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
    except Exception as e:
        raise HTTPException(status_code=422,
                            detail=f"Problem inserting new dataset record into dataset table. Error: {e}")

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


def get_aggs(db: Session, dataset_name: str):
    table = _get_dynamic_table(db, dataset_name)
    return db.query(table).all()


def get_agg_as_pdf(db: Session, dataset_name: str):
    return pd.read_sql_table(dataset_name, db.bind)


def _get_dynamic_table(db: Session, table_name: str):
    meta = MetaData()
    meta.reflect(db.bind)
    table = meta.tables[table_name]
    return table

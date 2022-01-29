from fastapi import HTTPException
from fastapi import APIRouter
from app.core import db_crud
from app.core.anomaly_detection import knn_scan
from app.core.models.dataset import Dataset, AggUpdate
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/dataset/{dataset_name}", response_model=Dataset)
def get_dataset_by_name(dataset_name: str, db: Session = Depends(get_db)):
    return db_crud.get_dataset_by_name(db, dataset_name)


@router.post("/dataset/")
def create_dataset(dataset: Dataset, db: Session = Depends(get_db)):
    dataset_exists = db_crud.get_dataset_by_name(db, dataset.name)
    if dataset_exists:
        raise HTTPException(status_code=400, detail="Dataset name already taken.")
    return db_crud.create_dataset(db=db, dataset=dataset)


@router.post("/agg_update/")
def add_agg_update(aggs: AggUpdate, db: Session = Depends(get_db)):
    return db_crud.insert_agg_value(db, aggs)


@router.post("/perform_scan/")
def perform_scan(dataset_name: str, db: Session = Depends(get_db)):
    return knn_scan(dataset_name, db)

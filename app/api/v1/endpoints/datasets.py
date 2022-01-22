from fastapi import HTTPException
from fastapi import APIRouter
from app.core import db_crud
from app.core.db_crud import get_dataset_by_name
from app.core.models.dataset import Dataset
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/dataset/{dataset_name}", response_model=Dataset)
def get_dataset_by_name(dataset_name: str, db: Session = Depends(get_db)):
    return db_crud.get_dataset_by_name(db, dataset_name)


@router.post("/dataset/")
def create_dataset(dataset: Dataset, db: Session = Depends(get_db)):
    dataset_exists = get_dataset_by_name(db, dataset.name)
    if dataset_exists:
        raise HTTPException(status_code=400, detail="Dataset name already taken.")
    return db_crud.create_dataset(db=db, dataset=dataset)

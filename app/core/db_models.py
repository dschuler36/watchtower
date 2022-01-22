from app.database import Base
from sqlalchemy import Column, Integer, String


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    storage_platform = Column(String)
    notification_email = Column(String)

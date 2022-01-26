from app.database import Base
from sqlalchemy import Column, Integer, String


class Dataset(Base):
    __tablename__ = "datasets"

    def __init__(self, name, notification_email):
        self.name = name
        self.notification_email = notification_email

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    notification_email = Column(String)

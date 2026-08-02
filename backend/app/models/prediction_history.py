from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String

from app.database.database import Base


class PredictionHistory(Base):

    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True)

    zone = Column(String)

    rainfall = Column(Float)

    depth = Column(Float)

    risk = Column(Float)

    level = Column(String)
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.database import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    zone = Column(String)

    description = Column(String)

    severity = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
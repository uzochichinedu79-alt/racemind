from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    team_name = Column(String, nullable=False)
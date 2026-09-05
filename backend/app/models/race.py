from sqlalchemy import Column, Integer, String, Date

from app.core.database import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, nullable=False)
    grand_prix = Column(String, nullable=False)
    circuit = Column(String, nullable=False)
    country = Column(String, nullable=False)
    date = Column(Date, nullable=False)
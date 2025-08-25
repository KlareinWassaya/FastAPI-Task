from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey

from src.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    priority = Column(Integer, index=True)
    done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        CheckConstraint('priority >= 0 AND priority <= 5', name='priority_range'),
    )
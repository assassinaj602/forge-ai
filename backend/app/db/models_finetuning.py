"""
Fine-tuning Jobs Database Models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class FineTuningJob(Base):
    __tablename__ = "fine_tuning_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    model_name = Column(String(100), nullable=False)
    dataset_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")  # pending, training, completed, failed
    epochs = Column(Integer, default=3)
    batch_size = Column(Integer, default=4)
    learning_rate = Column(String(50), default="2e-5")
    metrics = Column(JSON, nullable=True)  # loss, accuracy history
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="fine_tuning_jobs")

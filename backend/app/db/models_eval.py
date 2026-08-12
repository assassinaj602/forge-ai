import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.db.models import generate_uuid

class EvalSuite(Base):
    __tablename__ = "eval_suites"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    test_cases = relationship("EvalTestCase", back_populates="suite", cascade="all, delete-orphan")
    runs = relationship("EvalRun", back_populates="suite", cascade="all, delete-orphan")

class EvalTestCase(Base):
    __tablename__ = "eval_test_cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    suite_id: Mapped[str] = mapped_column(String(36), ForeignKey("eval_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=True)
    assertion_type: Mapped[str] = mapped_column(String(50), default="contains")  # contains, exact_match, regex, length
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    suite = relationship("EvalSuite", back_populates="test_cases")

class EvalRun(Base):
    __tablename__ = "eval_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    suite_id: Mapped[str] = mapped_column(String(36), ForeignKey("eval_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), default="mock-v1")
    provider: Mapped[str] = mapped_column(String(50), default="mock")
    score: Mapped[float] = mapped_column(Float, default=0.0)
    passed_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    results: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    suite = relationship("EvalSuite", back_populates="runs")

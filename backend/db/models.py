from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, func , Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
 
from .base import Base


EMBEDDING_DIM = 384

class Knowledge_base(Base):
    __tablename__ = "knowledge_chunks"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True) , primary_key=True , default=uuid.uuid4)
    role : Mapped[str] = mapped_column(String , index=True , nullable=False)
    source : Mapped[str] = mapped_column(String , nullable=False)
    chunk : Mapped[str] = mapped_column(Text , nullable=False)
    chunk_index : Mapped[int] = mapped_column(Integer , nullable=False)
    embedding : Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM) , nullable=False)




class Interview_question(Base):
    __tablename__ = "interview_question"
    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True) , primary_key=True , nullable=False , default=uuid.uuid4)
    question_text : Mapped[str] = mapped_column(Text , nullable=False )
    answer_text : Mapped[str | None] = mapped_column(Text , nullable=True)
    source_chunk_ids: Mapped[str | None] = mapped_column(Text, nullable=True) 
    session : Mapped[Interview_session] = relationship(back_populates="questions")
    session_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_session.id") , nullable=False)

class Interview_session(Base):
    __tablename__ = "interview_session"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True) , primary_key=True , nullable=False , default=uuid.uuid4)
    candidate_resume : Mapped[str] = mapped_column(Text , nullable=False)
    resume_status : Mapped[str] = mapped_column(String , default="in_progress") 
    candidate_role : Mapped[str] = mapped_column(String , nullable=False)
    candidate_score : Mapped[float | None] = mapped_column(Float , nullable=True)
    questions : Mapped[list[Interview_question]] = relationship( back_populates="session" , cascade="all, delete-orphan")


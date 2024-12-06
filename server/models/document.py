from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.extensions import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    chunks: Mapped[List["Chunk"]] = relationship(
        back_populates="document",
        order_by="desc(Chunk.id)",
        cascade="all,delete,delete-orphan",
    )

    def to_json(self):
        return {
            "id": f"{self.id}",
            "text": self.text,
        }


class Chunk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    vectors = db.Column(Vector(384))

    document_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    document: Mapped["Document"] = relationship(back_populates="chunks")

    def to_json(self):
        return {
            "id": f"{self.id}",
            "text": self.text,
        }

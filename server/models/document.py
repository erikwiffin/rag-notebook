from server.extensions import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    def to_json(self):
        return {
            "id": f"{self.id}",
            "text": self.text,
        }

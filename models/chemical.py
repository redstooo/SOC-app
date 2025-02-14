from db import db


class ChemicalModel(db.Model):
    __tablename__ = "chemicals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    state = db.Column(db.String(256), unique=True, nullable=False)

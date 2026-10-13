from core import db
from typing import List, Dict

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ServerName = db.Column(db.String())
    Amount = db.Column(db.Integer())
    LastUpdated = db.Column(db.String())
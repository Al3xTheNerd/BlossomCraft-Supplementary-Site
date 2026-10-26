from core.extensions import db
from typing import List, Dict

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ItemData = db.Column(db.String(100000))
    Extension = db.Column(db.String())

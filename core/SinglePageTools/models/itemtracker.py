from core.extensions import db
from typing import List, Dict

class ItemTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    Code = db.Column(db.String(10))
    ItemList = db.Column(db.String(10000))


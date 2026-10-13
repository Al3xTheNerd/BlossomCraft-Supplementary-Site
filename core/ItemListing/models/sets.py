from core.extensions import db
from typing import List, Dict

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    ItemList = db.Column(db.String(10000))
    SetOrder = db.Column(db.Integer())
    Type = db.Column(db.String())
    SetDescription = db.Column(db.String())

    def to_dict(self, includes: List[str]) -> Dict[str, str]:
        retItem = {}
        if includes[0] == "*":
            includes = [x for x in vars(self).keys() if not x.startswith("_")]
        for inc in includes:
            retItem[inc] = vars(self)[inc]
        return retItem
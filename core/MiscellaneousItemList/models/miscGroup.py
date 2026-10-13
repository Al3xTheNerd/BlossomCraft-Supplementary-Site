from core.extensions import db
from typing import List, Dict
class MiscellaneousGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    GroupName = db.Column(db.String())
    ReleaseDate = db.Column(db.String())
    URLTag = db.Column(db.String())
    GroupType = db.Column(db.String())
    Notes = db.Column(db.String())
    
    GroupOrder = db.Column(db.Integer)


    
    
    def to_dict(self, includes: List[str] | str) -> Dict[str, str]:
        retItem = {}
        if includes == "*" or includes[0] == "*":
            includes = [x for x in vars(self).keys() if not x.startswith("_")]
        for inc in includes:
            retItem[inc] = vars(self)[inc]
        return retItem 
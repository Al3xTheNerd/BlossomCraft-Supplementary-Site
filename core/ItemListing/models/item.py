from core.extensions import db
from typing import List, Dict
class Item(db.Model):
    """Minecraft Item"""
    id = db.Column(db.Integer(), primary_key=True) # Integer
    
    CrateID = db.Column(db.String())
    TagPrimary = db.Column(db.String())
    TagSecondary = db.Column(db.String())
    TagTertiary = db.Column(db.String())
    TagQuaternary = db.Column(db.String())
    TagQuinary = db.Column(db.String())
    TagSenary = db.Column(db.String())
    TagSeptenary = db.Column(db.String())
    WinPercentage = db.Column(db.String())
    RarityHuman = db.Column(db.String())
    RarityHTML = db.Column(db.String())
    ItemName = db.Column(db.String())    
    ItemNameHTML = db.Column(db.String())
    Notes = db.Column(db.String())
    RawData = db.Column(db.String())
    ItemHuman = db.Column(db.String())
    ItemHTML = db.Column(db.String())
    
    ItemOrder = db.Column(db.Integer())
    # This will be a jsonified list of db.Item.id's
    ConnectedItems = db.Column(db.String()) 
    
    EfficiencyLevel = db.Column(db.Integer())
    
    SubmergedMiningSpeedAttribute = db.Column(db.Float())
    ImageType = db.Column(db.String())
    
    
    def to_dict(self, includes: List[str] | str) -> Dict[str, str]:
        retItem = {}
        if includes == "*":
            includes = [x for x in vars(self).keys() if not x.startswith("_")]
        for inc in includes:
            retItem[inc] = vars(self)[inc]
        return retItem
        



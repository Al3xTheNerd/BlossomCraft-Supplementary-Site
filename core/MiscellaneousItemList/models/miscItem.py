from core.extensions import db
from typing import List, Dict
from flask import url_for
class MiscellaneousItem(db.Model):
    """Minecraft Item"""
    id = db.Column(db.Integer(), primary_key=True) # Integer
    
    GroupID = db.Column(db.String())

    ItemName = db.Column(db.String())    
    ItemNameHTML = db.Column(db.String())
    Notes = db.Column(db.String())
    RawData = db.Column(db.String())
    ItemHuman = db.Column(db.String())
    ItemHTML = db.Column(db.String())
    
    ItemOrder = db.Column(db.Integer())
    ImageType = db.Column(db.String())
    
    
    def to_dict(self, includes: List[str] | str) -> Dict[str, str]:
        retItem = {}
        if includes == "*":
            includes = [x for x in vars(self).keys() if not x.startswith("_")]
        for inc in includes:
            retItem[inc] = vars(self)[inc]
        return retItem
    
    def icon_based_image(self) -> str:
        return f"""<img class="w-100" src="{url_for('static', filename = f"images/Misc_Icons/{self.id}.{self.ImageType}")}" data-bs-toggle="tooltip" data-bs-html="true" data-bs-placement="bottom" data-bs-title="<div class='give-preview-text-outer marker'><div class='give-preview-text w-100'><div class='give-preview-text-inner text-start'>{self.ItemHTML.replace('"', '&quot;')}</div></div></div>">"""
        
        



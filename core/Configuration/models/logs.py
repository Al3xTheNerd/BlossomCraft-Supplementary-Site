from core.extensions import db
from typing import List, Dict
from datetime import datetime

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String())
    Username = db.Column(db.String())
    PermissionLevel = db.Column(db.Integer())
    Message = db.Column(db.String())
    RelatedID = db.Column(db.Integer())
    Time = db.Column(db.String())

def uploadLog(currentUser, messageType, message, relatedID):
    new_log = Logs()
    new_log.Username = currentUser.username
    new_log.PermissionLevel = currentUser.permissions
    new_log.Message = message
    new_log.Type = messageType
    new_log.RelatedID = relatedID
    new_log.Time = str(datetime.now().strftime("%m/%d/%Y %H:%M"))
    
    db.session.add(new_log)
    db.session.commit()
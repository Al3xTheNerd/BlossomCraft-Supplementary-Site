from flask_login import UserMixin
from core.extensions import db, login_manager

from core.permissions import getFlattenedPermissions
from json import loads, dumps

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    permissions = db.Column(db.Integer)
    permissionNodes = db.Column(db.String(4000))
    bio = db.Column(db.String(2000))
    staffRole = db.Column(db.String(32))
    hasProfileImage = db.Column(db.String(64))
    maintainerStatus = db.Column(db.String(32))
    
    def _verifyValidPermissionNodes(self):
        current_permissions = loads(self.permissionNodes if self.permissionNodes else "{}")
        if not isinstance(current_permissions, dict): current_permissions = {}
        
        changes = 0
        for node in getFlattenedPermissions():
            if node not in current_permissions.keys():
                changes += 1
                current_permissions[node] = False
        if changes > 0:
            self.permissionNodes = dumps(current_permissions)
            db.session.commit()
        
    def get_permissions(self):
        self._verifyValidPermissionNodes()
        return loads(self.permissionNodes)
        
    def has_permission(self, perm_key) -> bool:
        if self.permissions >= 90:
            return True
        if perm_key == None:
            return True
        current_permissions = self.get_permissions()
        return current_permissions[perm_key]
    
    def set_permission(self, perm_key: str, value: bool) -> bool:
        self._verifyValidPermissionNodes()
        if perm_key in getFlattenedPermissions():
            current_permissions = loads(self.permissionNodes)
            current_permissions[perm_key] = value
            self.permissionNodes = dumps(current_permissions)
            db.session.commit()
            return True
        else:
            return False
        
    def set_image_link(self, bypass: bool = False) -> bool:
        disabled = "https://vzge.me/head/256/X-Steve"
        if self.hasProfileImage != disabled or bypass == True:
            username: str = self.username
            if username.startswith("BR_"):
                username = "." + username.removeprefix("BR_")
            self.hasProfileImage = f"https://api.mcheads.org/ioshead/{username}/right/512"
        else: 
            self.hasProfileImage = disabled
        db.session.commit()
        return True
    
    def profile_image(self) -> str:
        return self.hasProfileImage
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
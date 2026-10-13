from typing import Any

RegisteredPermissions: dict[str, Any] = {}

def getFlattenedPermissions():
    return [node[0] for nodes in RegisteredPermissions.values() for node in nodes if node is not None]
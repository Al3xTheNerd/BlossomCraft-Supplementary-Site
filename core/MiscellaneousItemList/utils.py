from typing import List, Tuple
from sqlalchemy import desc
from core.MiscellaneousItemList.models import MiscellaneousGroup, MiscellaneousItem
from flask import Response, jsonify



def currentItemsByGroup():
    groups: List[MiscellaneousGroup]= MiscellaneousGroup.query.order_by(MiscellaneousGroup.GroupOrder).all()
    items: List[MiscellaneousItem] = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
    sortedItems = {}
    groupIDToName = {}
    for group in groups:
        sortedItems[group.GroupName] = []
        groupIDToName[group.id] = group.GroupName
    for item in items:
        sortedItems[groupIDToName[int(item.GroupID)]].append(item)
    return sortedItems

def currentGroupData():
    groups = MiscellaneousGroup.query.order_by(desc(MiscellaneousGroup.id))
    formattedGroups = {}
    for group in groups.all():
        formattedGroups[group.id] = {
            "GroupName" : group.GroupName,
            "ReleaseDate" : group.ReleaseDate,
            "URLTag" : group.URLTag,
            "GroupType" : group.GroupType,
            "Notes" : group.Notes
            
        }
    if formattedGroups:
        return formattedGroups
    return None

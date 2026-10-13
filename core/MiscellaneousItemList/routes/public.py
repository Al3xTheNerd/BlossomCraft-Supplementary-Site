from flask import render_template, flash, url_for, redirect
from typing import List

from core.MiscellaneousItemList import bp
from core.MiscellaneousItemList.models import MiscellaneousGroup, MiscellaneousItem
from core.ItemListing.models import Item
from core.config import validMiscGroupTypes

@bp.route("/")
def Index():
    return render_template("MiscellaneousItemList/public/index.html")

@bp.route('/rawmiscitem/<itemID>')
def rawMiscitem(itemID):
    try:
        item = MiscellaneousItem.query.filter_by(id = itemID).first() # type: ignore
    except:
        flash("Item not found.")
        return redirect(url_for("all"))
    return render_template("MiscellaneousItemList/public/singleItemRaw.html", item = item)


@bp.route('/group/<groupTag>')
def SingleGroup(groupTag):
    try:
        group = MiscellaneousGroup.query.filter_by(URLTag = groupTag).first()
        if not group:
            flash("Group not found.")
            return redirect('/groups')
        parentItems = Item.query.filter_by(ConnectedItems = group.id).all()
        items = MiscellaneousItem.query.filter_by(GroupID = group.id).order_by(MiscellaneousItem.ItemOrder)
        if not items:
            flash("No items found in group.")
            return redirect('/groups')
    except:
        flash("Something went wrong.")
        return redirect('/groups')

    return render_template("MiscellaneousItemList/public/group.html", Items = items, Group = group, ParentItems = parentItems)

@bp.route('/groups')
def GroupList():
    groups: List[MiscellaneousGroup] = MiscellaneousGroup.query.order_by(MiscellaneousGroup.GroupOrder).all()
    groupList = {
        "" : []
        }
    for groupType in validMiscGroupTypes:
        groupList[groupType] = []
    for group in groups:
        for key in groupList.keys():
            if group.GroupType == key:
                groupList[key].append(group)
    for key in list(groupList.keys()):
        if len(groupList[key]) == 0:
            del groupList[key]
    return render_template("MiscellaneousItemList/public/groups.html", SortedGroups = groupList)

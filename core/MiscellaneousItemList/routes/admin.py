from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import func
from typing import List
from sys import platform

import json, os
from flask_login import current_user

from core.MiscellaneousItemList import bp
from core.Configuration.decorators import has_permission
from core.Configuration.models import uploadLog
from core.utils import intParser
from core.extensions import db
from core.MiscellaneousItemList.models import MiscellaneousItem, MiscellaneousGroup
from core.MiscellaneousItemList.utils import currentItemsByGroup, currentGroupData
from core.config import validMiscGroupTypes, server_folder_name

@bp.route('/admin/additem', methods=['POST', 'GET']) # type: ignore
@has_permission("view_add_misc_item")
def AddMiscItem():
    formattedGroups = currentGroupData()
    if request.method == 'POST':
        form = request.form.to_dict()
        newItem = MiscellaneousItem()
        newItem.GroupID = form["Group"]
        newItem.ItemName = form["ItemName"]
        newItem.ItemNameHTML = form["ItemNameHTML"]
        newItem.Notes = form["Notes"]
        newItem.RawData = form["RawData"]
        newItem.ItemHuman = form["HumanData"]
        newItem.ItemHTML = form["HTMLData"]
        newItem.ImageType = None
        try:
            newItem.ItemOrder = (db.session.query(func.max(MiscellaneousItem.ItemOrder)).scalar() + 1)
        except:
            newItem.ItemOrder = 1
        try:
            db.session.add(newItem)
            db.session.commit()
            uploadLog(current_user, "Misc Item", f"{newItem.ItemName} added to db.", newItem.ItemOrder)
            flash(f"{newItem.ItemNameHTML} added to {formattedGroups[int(newItem.GroupID)]['GroupName']} ({MiscellaneousItem.query.filter(MiscellaneousItem.GroupID == newItem.GroupID).count()})", "dark") # type: ignore
        except Exception as e:
            flash(f"Someting went wrong ({e})", "dark")
    return render_template("MiscellaneousItemList/admin/addItem.html",
                           currentGroups = formattedGroups)

@bp.route('/admin/itemlist', methods=['POST', 'GET']) # type: ignore
@has_permission("view_misc_item_list")
def MiscItemList():
    currentItems = currentItemsByGroup()
    return render_template('MiscellaneousItemList/admin/itemList.html', currentItems = currentItems)

@bp.route('/admin/itemorder', methods=['GET', 'POST']) # type: ignore
@has_permission("view_reorder_misc_items")
def MiscItemOrder():
    items: List[MiscellaneousItem] = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
    if not items:
        flash('No items in database.', "dark")
        return redirect(url_for("MiscellaneousItemList.AddMiscItem"))
    
    if request.method == 'POST':
        forms = request.form.to_dict()
        ItemOrders = json.loads(forms["ItemOrder"], object_hook=intParser)
        changes = 0
        for item in items:
            oldItemOrder = item.ItemOrder
            newItemOrder = ItemOrders[item.id]
            if oldItemOrder == newItemOrder:
                pass
            else:
                changes += 1
                item.ItemOrder = ItemOrders[item.id]
        db.session.commit()
        uploadLog(current_user, "Misc Item", f"{changes} items reordered.", None)
        items: List[MiscellaneousItem] = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
        flash(str(changes), "dark")
    return render_template('MiscellaneousItemList/admin/itemOrder.html', currentItems = items, name="Item")

@bp.route('/admin/grouporder', methods=['GET', 'POST']) # type: ignore
@has_permission("view_reorder_misc_groups")
def MiscGroupOrder():
    groups: List[MiscellaneousGroup] = MiscellaneousGroup.query.order_by(MiscellaneousGroup.GroupOrder).all()
    if not groups:
        flash('No groups in database.', "dark")
        return redirect(url_for("MiscellaneousItemList.ManageGroups"))
    
    if request.method == 'POST':
        forms = request.form.to_dict()
        ItemOrders = json.loads(forms["ItemOrder"], object_hook=intParser)
        changes = 0
        for group in groups:
            oldItemOrder = group.GroupOrder
            newItemOrder = ItemOrders[group.id]
            if oldItemOrder == newItemOrder:
                pass
            else:
                changes += 1
                group.GroupOrder = ItemOrders[group.id]
        db.session.commit()
        uploadLog(current_user, "Misc Item", f"{changes} items reordered.", None)
        groups: List[MiscellaneousGroup] = MiscellaneousGroup.query.order_by(MiscellaneousGroup.GroupOrder).all()
        flash(str(changes), "dark")

    return render_template('MiscellaneousItemList/admin/itemOrder.html', currentItems = groups, name="Group")


@bp.route('/admin/manageitem/<itemID>', methods=['GET', 'POST'])
@has_permission("view_edit_misc_item")
def ManageMiscItem(itemID):
    formattedGroups = currentGroupData()
    item: MiscellaneousItem = MiscellaneousItem.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect(url_for("MiscellaneousItemList.MiscItemList"))
    else:
        if request.method == 'POST':
            if "FileForm" in request.form.to_dict():
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                
                if file and file.filename:
                    if file.filename.endswith(".png"):
                        filename = f"{itemID}.png"
                        item.ImageType = "png"
                    elif file.filename.endswith(".gif"):
                        filename = f"{itemID}.gif"
                        item.ImageType = "gif"
                    else:
                        filename = None
                    if filename:
                        if platform == "win32":
                            loc = f"core/_Shared/static/images/Misc_Icons/"
                        else:
                            loc = f"/home/alexthenerd/{server_folder_name}/core/_Shared/static/images/Misc_Icons/"
                            # TODO: get this fixed for beaver's hosting
                        
                        db.session.commit()
                        file.save(os.path.join(loc, filename))
                        uploadLog(current_user, "Misc Item", "icon image uploaded.", itemID)
                        flash("Image saved successfully.")
            else:
                old = item.to_dict("*")
                item.GroupID = request.form.get("Group", item.GroupID)
                item.Notes = request.form.get("Notes", item.Notes)
                item.ItemName = request.form.get("ItemName", item.ItemName)
                new = item.to_dict("*")
                db.session.commit()
                for key in old.keys():
                    if old[key] != new[key]:
                        uploadLog(current_user, "Misc Item", f"{item.ItemName} | {key} | '{old[key]}'-->'{new[key]}'.", item.id)
                    
                flash(f"{item.ItemNameHTML} updated successfully!", "dark")
    return render_template("MiscellaneousItemList/admin/manageItem.html", 
                           item = item,
                           currentGroups = formattedGroups)
        
@bp.route('/admin/deleteitem/<itemID>', methods=['GET', 'POST'])
@has_permission("delete_misc_item")
def DeleteMiscItem(itemID):
    item: MiscellaneousItem = MiscellaneousItem.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect(url_for("MiscellaneousItemList.MiscItemList"))
    try:
        db.session.delete(item)
        db.session.commit()
        flash(f"Item #{itemID} - {item.ItemNameHTML} deleted successfully.", "dark")
        uploadLog(current_user, "Misc Item", f"{item.ItemName} deleted from db.", None)
    except:
        db.session.rollback()
        flash(f"Error deleteing #{item.id} - {item.ItemNameHTML}")
    return redirect(url_for("MiscellaneousItemList.MiscItemList"))

@bp.route('/admin/managegroups', methods=['POST', 'GET'])
@has_permission("view_manage_misc_groups")
def ManageGroups():
    queries = 0
    if request.method == 'POST':
        forms = request.form.to_dict()
        if "New" in forms and current_user.has_permission("create_misc_group"):
            newGroup = MiscellaneousGroup()
            newGroup.GroupName = forms["GroupName"]
            newGroup.ReleaseDate = forms["ReleaseDate"]
            newGroup.URLTag = forms["GroupTag"]
            newGroup.GroupType = forms["GroupType"]
            newGroup.Notes = forms["Notes"]
            
            try:
                newGroup.GroupOrder = (db.session.query(func.max(MiscellaneousGroup.GroupOrder)).scalar() + 1)
            except:
                newGroup.GroupOrder = 1
            
            db.session.add(newGroup)
            db.session.commit()
            uploadLog(current_user, "Group", f"added to db..", newGroup.id)
            queries += 1
        if "Edit" in forms and current_user.has_permission("edit_misc_group_existing"):
            groupToEdit: MiscellaneousGroup = MiscellaneousGroup.query.filter_by(id = forms['Group']).one()
            old = groupToEdit.to_dict(["*"])
            groupToEdit.GroupName = forms["GroupName"]
            groupToEdit.ReleaseDate = forms["ReleaseDate"]
            groupToEdit.URLTag = forms["GroupTag"]
            groupToEdit.GroupType = forms["GroupType"]
            groupToEdit.Notes = forms["Notes"]
            new = groupToEdit.to_dict(["*"])
            db.session.commit()
            
            for key in old.keys():
                if old[key] != new[key]:
                    uploadLog(current_user, "Group", f"{key} | '{old[key]}'-->'{new[key]}'.", groupToEdit.id)
            queries += 2
        if "Delete" in forms and forms['Group'] and current_user.has_permission("delete_misc_group"):
            group = MiscellaneousGroup.query.filter_by(id=forms['Group']).first().to_dict(["*"]) # type: ignore
            MiscellaneousGroup.query.filter_by(id=forms['Group']).delete()
            itemsToDelete = MiscellaneousItem.query.filter(MiscellaneousItem.GroupID == forms["Group"]).all()
            db.session.execute(
                db.delete(MiscellaneousItem).filter_by(GroupID = forms["Group"])
            )
            db.session.commit()
            uploadLog(current_user, "Group", f"{group['GroupName']} deleted from db.", None) # type: ignore
            if itemsToDelete:
                for item in itemsToDelete:
                    uploadLog(current_user, "Misc Item", f"{item.ItemName} deleted from db with {group['GroupName']}.", None) # type: ignore
            queries += 1
        if queries == 0:
            flash("Something Went Wrong.", "dark")
    formattedGroups = currentGroupData()
    queries += 1

    return render_template("MiscellaneousItemList/admin/manageGroups.html", currentGroups = formattedGroups, validGroupTypes = validMiscGroupTypes)

@bp.route('/admin/missingimages')
@has_permission("view_misc_missing_images")
def MissingImages():
    miscItems: List[MiscellaneousItem] = MiscellaneousItem.query.filter(MiscellaneousItem.ImageType == None).all()

    return render_template("MiscellaneousItemList/admin/missingImages.html", MissingMiscIcons = miscItems)

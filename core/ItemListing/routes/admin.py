from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import not_, or_, func
from core import config
import json, os

from flask_login import current_user
from typing import List
from sys import platform

from core.ItemListing import bp
from core.utils import intParser
from core.Configuration.decorators import has_permission
from core.Configuration.models import uploadLog
from core.ItemListing.models import Crate, Item, Set
from core.ItemListing.utils import verifyCrate, currentItemsByCrate, currentCrateData
from core.MiscellaneousItemList.models import MiscellaneousGroup
from core.extensions import db


@bp.route('/admin/additem', methods=['POST', 'GET']) # type: ignore
@has_permission("view_add_item")
def AddItem():
    formattedCrates = currentCrateData()
    if request.method == 'POST':
        form = request.form.to_dict()
        newItem = Item()
        newItem.CrateID = form["Crate"]
        newItem.TagPrimary = form["PrimaryTag"]
        newItem.TagSecondary = form["SecondaryTag"]
        newItem.TagTertiary = form["TertiaryTag"]
        newItem.TagQuaternary = form["QuaternaryTag"]
        newItem.TagQuinary = form["QuinaryTag"]
        newItem.TagSenary = form["SenaryTag"]
        newItem.TagSeptenary = form["SeptenaryTag"]
        newItem.WinPercentage = form["WinPercentage"]
        newItem.RarityHuman = form["Rarity"]
        newItem.RarityHTML = form["RarityHTML"]
        newItem.ItemName = form["ItemName"]
        newItem.ItemNameHTML = form["ItemNameHTML"]
        newItem.Notes = form["Notes"]
        newItem.RawData = form["RawData"]
        newItem.ItemHuman = form["HumanData"]
        newItem.ItemHTML = form["HTMLData"]
        newItem.ImageType = None
        itemTags = set([newItem.TagPrimary, newItem.TagSecondary, newItem.TagTertiary, newItem.TagQuaternary, newItem.TagQuinary, newItem.TagSenary, newItem.TagSeptenary])
        if len(itemTags.intersection(set(["Pickaxe", "Axe", "Hoe", "Shovel", "Shears"]))) > 0:
            itemNBT = json.loads(newItem.RawData)
            if "components" in itemNBT:
                if "minecraft:enchantments" in itemNBT["components"]:
                    if "minecraft:efficiency" in itemNBT["components"]["minecraft:enchantments"]:
                        newItem.EfficiencyLevel = itemNBT["components"]["minecraft:enchantments"]["minecraft:efficiency"]
                if "minecraft:attribute_modifiers" in itemNBT["components"]:
                    if "modifiers" in itemNBT["components"]["minecraft:attribute_modifiers"]:
                        for modifier in itemNBT["components"]["minecraft:attribute_modifiers"]["modifiers"]:
                            if modifier["type"] == "minecraft:submerged_mining_speed":
                                newItem.SubmergedMiningSpeedAttribute = modifier["amount"]
        try:
            newItem.ItemOrder = (db.session.query(func.max(Item.ItemOrder)).scalar() + 1)
        except:
            newItem.ItemOrder = 1
        try:
            db.session.add(newItem)
            db.session.commit()
            uploadLog(current_user, "Item", f"{newItem.ItemName} added to db.", newItem.ItemOrder)
            flash(f"{newItem.ItemNameHTML} added to {formattedCrates[int(newItem.CrateID)]['CrateName']} ({Item.query.filter(Item.CrateID == newItem.CrateID).count()})", "dark") # type: ignore
        except Exception as e:
            flash(f"Someting went wrong ({e})", "dark")
    return render_template("ItemListing/admin/addItem.html", 
                           validTags = config.validTags,
                           currentCrates = formattedCrates)

@bp.route('/admin/itemlist', methods=['POST', 'GET']) # type: ignore
@has_permission("view_item_list")
def ItemList():
    currentItems = currentItemsByCrate()
    return render_template('ItemListing/admin/itemList.html', currentItems = currentItems)

@bp.route('/admin/itemorder', methods=['GET', 'POST']) # type: ignore
@has_permission("view_reorder_items")
def ItemOrder():
    items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
    if not items:
        flash('No items in database.', "dark")
        return redirect(url_for("ItemListing.AddItem"))
    
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
        uploadLog(current_user, "Item", f"{changes} items reordered.", None)
        items: List[Item] = Item.query.order_by(Item.ItemOrder).all()
        flash(str(changes), "dark")

    return render_template('ItemListing/admin/itemOrder.html', currentItems = items)

@bp.route('/admin/manageitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@has_permission("view_edit_item")
def ManageItem(itemID):
    formattedCrates = currentCrateData()
    currentMiscGroups = MiscellaneousGroup.query.order_by(MiscellaneousGroup.GroupOrder.desc()).all()
    item: Item = Item.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect(url_for("ItemListing.ItemList"))
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
                            loc = f"core/_Shared/static/images/Icons/"
                        else:
                            loc = f"/home/blossomcraft/BlossomCraft/core/_Shared/static/images/Icons/"
                        
                        db.session.commit()
                        file.save(os.path.join(loc, filename))
                    uploadLog(current_user, "Item", "icon image uploaded.", itemID)
                    flash("Image saved successfully.")
            else:
                old = item.to_dict("*")
                item.CrateID = request.form.get("Crate", item.CrateID)
                item.TagPrimary = request.form.get("PrimaryTag", item.TagPrimary)
                item.TagSecondary = request.form.get("SecondaryTag", item.TagSecondary)
                item.TagTertiary = request.form.get("TertiaryTag", item.TagTertiary)
                item.TagQuaternary = request.form.get("QuaternaryTag", item.TagQuaternary)
                item.TagQuinary = request.form.get("QuinaryTag", item.TagQuinary)
                item.TagSenary = request.form.get("SenaryTag", item.TagSenary)
                item.TagSeptenary = request.form.get("SeptenaryTag", item.TagSeptenary)
                item.WinPercentage = request.form.get("WinPercentage", item.WinPercentage)
                item.Notes = request.form.get("Notes", item.Notes)
                item.ItemName = request.form.get("ItemName", item.ItemName)
                item.ConnectedItems = request.form.get("ConnectedItems", item.ConnectedItems)
                new = item.to_dict("*")
                db.session.commit()
                for key in old.keys():
                    if old[key] != new[key]:
                        uploadLog(current_user, "Item", f"{item.ItemName} | {key} | '{old[key]}'-->'{new[key]}'.", item.id)
                    
                flash(f"{item.ItemNameHTML} updated successfully!", "dark")
    return render_template("ItemListing/admin/manageItem.html", 
                           item = item,
                           validTags = config.validTags,
                           currentCrates = formattedCrates,
                           currentMiscGroups = currentMiscGroups)
        
@bp.route('/admin/deleteitem/<itemID>', methods=['GET', 'POST']) # type: ignore
@has_permission("delete_item")
def DeleteItem(itemID):
    item: Item = Item.query.filter_by(id = itemID).one()
    if not item:
        flash("Could Not Find Item.", "warning")
        return redirect(url_for("ItemListing.ItemList"))
    try:
        db.session.delete(item)
        db.session.commit()
        flash(f"Item #{itemID} - {item.ItemNameHTML} deleted successfully.", "dark")
        uploadLog(current_user, "Item", f"{item.ItemName} deleted from db.", None)
    except:
        db.session.rollback()
        flash(f"Error deleteing #{item.id} - {item.ItemNameHTML}")
    return redirect(url_for("ItemListing.ItemList"))

@bp.route('/admin/managecrates', methods=['POST', 'GET'])
@has_permission("view_manage_crate")
def ManageCrates():
    queries = 0
    if request.method == 'POST':
        forms = request.form.to_dict()
        if "New" in forms and verifyCrate(forms) and current_user.has_permission("create_crate"):
            newCrate = Crate(CrateName=forms["CrateName"], ReleaseDate=forms["ReleaseDate"], URLTag=forms["CrateTag"], CrateType=forms["CrateType"]) # type: ignore
            db.session.add(newCrate)
            db.session.commit()
            uploadLog(current_user, "Crate", f"added to db..", newCrate.id)
            queries += 1
        if "Edit" in forms and verifyCrate(forms) and current_user.has_permission("edit_crate_existing"):
            crateToEdit: Crate = Crate.query.filter_by(id = forms['crate']).one()
            old = crateToEdit.to_dict(["*"])
            crateToEdit.CrateName = forms['CrateName']
            crateToEdit.ReleaseDate = forms['ReleaseDate']
            crateToEdit.URLTag = forms["CrateTag"]
            crateToEdit.CrateType = forms["CrateType"]
            new = crateToEdit.to_dict(["*"])
            db.session.commit()
            
            for key in old.keys():
                if old[key] != new[key]:
                    uploadLog(current_user, "Crate", f"{key} | '{old[key]}'-->'{new[key]}'.", crateToEdit.id)
            queries += 2
        if "Delete" in forms and forms['crate'] and current_user.has_permission("delete_crate"):
            crate = Crate.query.filter_by(id=forms['crate']).first()
            if isinstance(crate, Crate):
                cratename = str(crate.CrateName)
                Crate.query.filter_by(id=forms['crate']).delete()
                itemsToDelete = Item.query.filter(Item.CrateID == forms["crate"]).all()
                db.session.execute(
                    db.delete(Item).filter_by(CrateID = forms["crate"])
                )
                db.session.commit()
                uploadLog(current_user, "Crate", f"{cratename} deleted from db.", None) # type: ignore
                if itemsToDelete:
                    for item in itemsToDelete:
                        uploadLog(current_user, "Item", f"{item.ItemName} deleted from db with {crate.CrateName}.", None) # type: ignore
                queries += 1
            if queries == 0:
                flash("Something Went Wrong.", "dark")
    formattedCrates = currentCrateData()
    queries += 1

    return render_template("ItemListing/admin/manageCrates.html", currentCrates = formattedCrates)

@bp.route('/admin/setManagement', methods=['GET', 'POST']) # type: ignore
@has_permission("view_set_management")
def SetManagement():
    sets: List[Set] = Set.query.order_by(Set.SetOrder).all()
    if not sets:
        flash('No sets in database.', "dark")
    if request.method == 'POST' and has_permission("edit_set_order"):
        forms = request.form.to_dict()
        ItemOrders = json.loads(forms["ItemOrder"], object_hook=intParser)
        changes = 0
        for set in sets:
            oldItemOrder = set.SetOrder
            newItemOrder = ItemOrders[set.id]
            if oldItemOrder == newItemOrder:
                pass
            else:
                changes += 1
                set.SetOrder = ItemOrders[set.id]
        db.session.commit()
        uploadLog(current_user, "Set", f"{changes} sets reordered.", None)
        sets: List[Set] = Set.query.order_by(Set.SetOrder).all()
        flash(str(changes), "dark")
    return render_template('ItemListing/admin/setOrder.html', currentSets = sets)

@bp.route('/admin/setMaker', methods=('GET', 'POST'))
@has_permission("create_new_set")
def SetMaker():
    if request.method == 'POST':
        code = json.loads(request.form['importCode'])
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        if len(code) < 2:
            flash("Set must have at least two items to create.")
        else:
            new_entry = Set(ItemList = str(code), Type = type, Name = name, SetDescription = description) # type: ignore
            try:
                new_entry.SetOrder = (db.session.query(func.max(Set.SetOrder)).scalar() + 1)
            except:
                new_entry.SetOrder = 1
            
            db.session.add(new_entry)
            db.session.commit()
            uploadLog(current_user, "Set", f"{new_entry.Name} added to db.", new_entry.SetOrder)
            setItems = Item.query.filter(Item.id.in_(code)).all()
            itemStrings = [item.ItemNameHTML for item in setItems]
            flash(f"Set <code>{name}</code>(<code>{type}</code>) with items <code>{str(itemStrings)}</code> created successfully.")

    sortedItems = {}
    idToCrateList = {}
    items: List[Item] = Item.query.filter(
        not_(or_(col.contains("Repeat Appearance") for col in [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary])) #type:ignore
    ).all()
    
    crateList: List[Crate] = Crate.query.order_by(Crate.id).all()
    for crate in crateList:
        for item in items:
            formattedItem = {
                "Name" : item.ItemNameHTML,
                "id" : item.id,
                "Tags" : [tag for tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSeptenary, item.TagSenary] if tag]
            }
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    idToCrateList[crate.CrateName].append(item.id)
                    sortedItems[crate.CrateName].append(formattedItem)
                else:
                    idToCrateList[crate.CrateName] = [item.id]
                    sortedItems[crate.CrateName] = [formattedItem]
    return render_template("ItemListing/admin/setMaker.html", sortedItems = sortedItems, idCrateList = idToCrateList, validTags = config.validTags, page="newtracker")

@bp.route('/admin/setEditor/<setID>', methods=('GET', 'POST'))
@has_permission("edit_set")
def EditSet(setID):
    setp: Set | None = Set.query.filter(Set.id == setID).first()
    if not setp:
        flash("Set does not exist to edit. Try again.")
        return redirect(url_for("ItemListing.SetManagement"))
    if request.method == 'POST':
        old = setp.to_dict(["*"])
        code = json.loads(request.form['importCode'])
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        if len(code) < 2:
            flash("Set must have at least two items to create.")
        else:
            setp.ItemList = str(code)
            setp.Type = type
            setp.Name = name
            setp.SetDescription = description
            new = setp.to_dict(["*"])
            db.session.commit()
            for key in old.keys():
                if old[key] != new[key]:
                    uploadLog(current_user, "Set", f"{setp.Name} | {key} | '{old[key]}'-->'{new[key]}'.", setp.id)
            flash(f"Set <code>{name}</code>(<code>{type}</code>) with items {str(code)} updates successfully.")

    sortedItems = {}
    idToCrateList = {}
    items: List[Item] = Item.query.filter(
        not_(or_(col.contains("Repeat Appearance") for col in [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary])) #type:ignore
    ).all()
    
    crateList: List[Crate] = Crate.query.order_by(Crate.id).all()
    for crate in crateList:
        for item in items:
            formattedItem = {
                "Name" : item.ItemNameHTML,
                "id" : item.id,
                "Tags" : [tag for tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSeptenary, item.TagSenary] if tag]
            }
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    idToCrateList[crate.CrateName].append(item.id)
                    sortedItems[crate.CrateName].append(formattedItem)
                else:
                    idToCrateList[crate.CrateName] = [item.id]
                    sortedItems[crate.CrateName] = [formattedItem]
    return render_template("ItemListing/admin/editSet.html", sortedItems = sortedItems, idCrateList = idToCrateList, validTags = config.validTags, page="newtracker", oldSet = setp)

@bp.route('/admin/deleteset/<setID>', methods=['GET', 'POST']) # type: ignore
@has_permission("delete_set")
def DeleteSet(setID):
    set: Set = Set.query.filter_by(id = setID).one()
    if not set:
        flash("Could Not Find Set.", "warning")
        return redirect(url_for("ItemListing.SetManagement"))
    try:
        db.session.delete(set)
        db.session.commit()
        flash(f"Set #{setID} - {set.Name} deleted successfully.", "dark")
        uploadLog(current_user, "Set", f"{set.Name} deleted from db.", None)
    except:
        db.session.rollback()
        flash(f"Error deleteing #{set.id} - {set.Name}")
    return redirect(url_for("ItemListing.SetManagement"))

@bp.route('/admin/missingimages')
@has_permission("view_missing_images")
def MissingImages():
    items: List[Item] = Item.query.filter(Item.ImageType == None).order_by(Item.ItemOrder).all()

    return render_template("ItemListing/admin/missingImages.html", MissingIcons = items)
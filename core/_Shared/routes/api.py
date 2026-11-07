from flask import render_template, request, flash, jsonify, Response
from sqlalchemy import or_, and_, func
from core import app
from core import config as c
from core.ItemListing.models import Item, Crate
from core.ItemListing.models import Set as ItemSet
from core.MiscellaneousItemList.models import MiscellaneousItem, MiscellaneousGroup
from core.SinglePageTools.models import ItemTracker
from core.Votes.models import Votes
from typing import List, Tuple
from core import db
import json

import base64
import os
from sys import platform
from pathlib import Path
from core.Configuration.decorators import api_permission_level_required
from core.Configuration.models.logs import uploadLog
from atn import server_name, server_folder_name

def get_icon_directory() -> str:
    if platform == "win32":
        loc = os.path.join(app.root_path, "_Shared", "static", "images", "Icons")
    else:
        loc = "/home/blossomcraft/BlossomCraft/core/_Shared/static/images/Icons"
    os.makedirs(loc, exist_ok=True)
    return loc

def get_misc_icon_directory() -> str:
    if platform == "win32":
        loc = os.path.join(app.root_path, "_Shared", "static", "images", "Misc_Icons")
    else:
        loc = "/home/blossomcraft/BlossomCraft/core/_Shared/static/images/Misc_Icons"
    os.makedirs(loc, exist_ok=True)
    return loc

TagCols = [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary]
class APIErrors():
    NO_RESULTS = (0, "No Results Found.")
    INVALID_COLUMN = (1, "[{}] is not a valid column.")
    
    
    def process(self, error: Tuple[int, str], var: str):
        toReturn = error
        return {toReturn[0] : toReturn[1].format(var)}
APIErrorHandler = APIErrors()


def determineIncludedInfo(headers: dict):
    inc = headers.get("I-INCLUDED-INFO")
    messages = []
    if inc:
        if inc != "*":
            eventualReturn = str(inc).split(";")
            toRemove = []
            for ret in eventualReturn:
                if ret not in vars(Item).keys():
                    toRemove.append(ret)
                    messages.append(APIErrorHandler.process(APIErrors.INVALID_COLUMN, ret))
            eventualReturn = [x for x in eventualReturn if x not in toRemove]
        else: eventualReturn = "*"
        return eventualReturn, messages
    else:
        return [
        "id",
        "ItemName"
        ], messages

def determineMiscIncludedInfo(headers: dict):
    inc = headers.get("I-INCLUDED-INFO")
    messages = []
    if inc:
        if inc != "*":
            eventualReturn = str(inc).split(";")
            toRemove = []
            for ret in eventualReturn:
                if ret not in vars(MiscellaneousItem).keys():
                    toRemove.append(ret)
                    messages.append(APIErrorHandler.process(APIErrors.INVALID_COLUMN, ret))
            eventualReturn = [x for x in eventualReturn if x not in toRemove]
        else: eventualReturn = "*"
        return eventualReturn, messages
    else:
        return [
        "id",
        "ItemName"
        ], messages


def buildResponse(data: List[dict] | None, messages: List[str]) -> Response:
    return jsonify({
        "messages" : messages,
        "data" : data
    })


@app.route('/api/items') # type: ignore
def ItemsAPI():
    """Get all items."""
    inc, messages = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.order_by(Item.ItemOrder).all()]
    return buildResponse(items, messages)

@app.route('/api/crates') # type: ignore
def CratesAPI():
    """Get all crates."""
    inc = [
        "id",
        "CrateName",
        "ReleaseDate",
        "URLTag",
        "CrateType"
    ]
    crates = [x.to_dict(inc) for x in Crate.query.order_by(Crate.id).all()]
    return jsonify(crates)

@app.route('/api/miscitems') # type: ignore
def MiscItemsAPI():
    """Get all items."""
    inc, messages = determineMiscIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()]
    return buildResponse(items, messages)

@app.route('/api/miscgroups') # type: ignore
def MiscGroupsAPI():
    """Get all crates."""
    inc = [
        "id",
        "GroupName",
        "ReleaseDate",
        "URLTag",
        "GroupType",
        "Notes",
        "GroupOrder",
    ]
    crates = [x.to_dict(inc) for x in MiscellaneousGroup.query.order_by(MiscellaneousGroup.id).all()]
    return jsonify(crates)

@app.route('/api/sets') # type: ignore
def SetsAPI():
    """Get all crates."""
    inc = [
        "id",
        "Name",
        "ItemList",
        "Type",
        "SetDescription",
        "SetOrder"
    ]
    crates = [x.to_dict(inc) for x in ItemSet.query.order_by(ItemSet.id).all()]
    return jsonify(crates)


@app.route('/api/search/itemname/<term>') # type: ignore
def ItemNameSearchAPI(term : str):
    """Search for items by name."""
    inc, messages = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.filter(Item.ItemName.ilike(f"%{term}%")).order_by(Item.ItemOrder).all()]
    if not items:
        items = None
        messages.append(APIErrors.NO_RESULTS)
    
    return buildResponse(items, messages)


@app.route('/api/search/itemid/<id>') # type: ignore
def ItemIDSearchAPI(id : int):
    """Search for items by name."""
    inc, messages = determineIncludedInfo(request.headers)
    item = Item.query.filter(Item.id == id).one_or_none()
    if isinstance(item, Item):
        item = [item.to_dict(inc)] # type: ignore
    return buildResponse(item, messages)


@app.route('/api/search/tag/<tag>') # type: ignore
def TagSearchAPI(tag : str):
    """Search for items by name."""
    inc, messages = determineIncludedInfo(request.headers)
    items = [x.to_dict(inc) for x in Item.query.filter(or_(col.is_(tag) for col in TagCols)).order_by(Item.ItemOrder).all()] # type: ignore
    if not items:
        items = None
    return buildResponse(items, messages)




@app.route('/api/tags') # type: ignore
def TagListAPI():
    """Search for items by name."""
    return jsonify(c.validTags)

@app.route('/api/itemCount')
def ItemCountAPI():
    return jsonify(Item.query.count())

@app.route('/api/max')
def MaxAPI():
    itemID = Item.query.all()[-1].id
    return jsonify(itemID)

from datetime import datetime
@app.route('/api/vote/set/<server>/<amount>/<lastupdated>') # type: ignore 
def setVote(server: str, amount: int, lastupdated: int):
    obj: Votes | None = Votes.query.filter_by(ServerName = server).first() # type: ignore

    if obj:
        obj.Amount = amount
        obj.LastUpdated = lastupdated
    else:
        obj = Votes(ServerName = server, Amount = amount, LastUpdated = lastupdated) # type: ignore
        db.session.add(obj)
    db.session.commit()
    return jsonify(True)

@app.route('/api/vote/get/<server>') # type: ignore
def getVote(server: str):
    try:
        obj: Votes | None = Votes.query.filter_by(ServerName = server).first() # type: ignore
        if obj:
            return jsonify({
                "Server" : obj.ServerName,
                "Amount" : obj.Amount,
                "LastUpdated" : obj.LastUpdated
            })
        else:
            return jsonify(None)
    except Exception as e:
        print(e)

@app.route('/api/itemtracker/<code>') # type: ignore
def getItemTracker(code: str):
    try:
        obj: Votes | None = ItemTracker.query.filter_by(Code = code).first() # type: ignore
        if obj:
            return jsonify(json.loads(obj.ItemList))
        else:
            return jsonify(None)
    except Exception as e:
        print(e)

# =====================================================================
# ItemDatabase Fabric Mod — In-Game Admin API Endpoints
# Enables staff to verify credentials, upload held items, edit attributes,
# and manage display order directly from Minecraft.
# =====================================================================

@app.route('/api/v1/admin/verify', methods=['GET'])
@api_permission_level_required(90)
def api_admin_verify(authenticated_user):
    """Health check and token authentication for the Fabric mod."""
    return jsonify({
        "success": True,
        "username": authenticated_user.username,
        "permissions": authenticated_user.permissions
    }), 200


@app.route('/api/v1/admin/item', methods=['POST'])
@api_permission_level_required(90)
def api_admin_add_item(authenticated_user):
    """Creates a new crate item or misc item from the Fabric mod."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    item_name = data.get("ItemName")
    if not item_name:
        return jsonify({"success": False, "error": "Missing required field: 'ItemName'"}), 400

    is_misc = "GroupID" in data or not data.get("CrateID")

    if is_misc:
        group_id = data.get("GroupID") or 1
        new_item = MiscellaneousItem()
        new_item.GroupID = str(group_id)
        new_item.ItemName = item_name
        new_item.ItemNameHTML = data.get("ItemNameHTML", item_name)
        new_item.RarityHuman = data.get("RarityHuman", "Common")
        new_item.RarityHTML = data.get("RarityHTML", "<span>Common</span>")
        new_item.Notes = data.get("Notes", "")
        new_item.RawData = data.get("RawData", "")
        new_item.ItemHuman = data.get("ItemHuman", "")
        new_item.ItemHTML = data.get("ItemHTML", "")
        new_item.ImageType = data.get("ImageType", None)

        try:
            new_item.ItemOrder = (db.session.query(func.max(MiscellaneousItem.ItemOrder)).filter_by(GroupID=str(group_id)).scalar() or 0) + 1
        except Exception:
            new_item.ItemOrder = 1

        db.session.add(new_item)
        db.session.commit()
        log_type = "MiscItem"

    else:
        new_item = Item()
        new_item.CrateID = str(data.get("CrateID"))
        new_item.TagPrimary = data.get("TagPrimary")
        new_item.TagSecondary = data.get("TagSecondary")
        new_item.TagTertiary = data.get("TagTertiary")
        new_item.TagQuaternary = data.get("TagQuaternary")
        new_item.TagQuinary = data.get("TagQuinary")
        new_item.TagSenary = data.get("TagSenary")
        new_item.TagSeptenary = data.get("TagSeptenary")
        new_item.WinPercentage = str(data.get("WinPercentage", "0%"))
        new_item.RarityHuman = data.get("RarityHuman", "Common")
        new_item.RarityHTML = data.get("RarityHTML", "<span>Common</span>")
        new_item.ItemName = item_name
        new_item.ItemNameHTML = data.get("ItemNameHTML", item_name)
        new_item.Notes = data.get("Notes", "")
        new_item.RawData = data.get("RawData", "")
        new_item.ItemHuman = data.get("ItemHuman", "")
        new_item.ItemHTML = data.get("ItemHTML", "")
        new_item.ImageType = data.get("ImageType", None)

        item_tags = {
            new_item.TagPrimary, new_item.TagSecondary, new_item.TagTertiary,
            new_item.TagQuaternary, new_item.TagQuinary, new_item.TagSenary, new_item.TagSeptenary
        }
        tool_set = {"Pickaxe", "Axe", "Hoe", "Shovel", "Shears"}

        if len(item_tags.intersection(tool_set)) > 0 and new_item.RawData:
            try:
                item_nbt = json.loads(new_item.RawData)
                components = item_nbt.get("components", {})
                enchants = components.get("minecraft:enchantments", {})
                if "minecraft:efficiency" in enchants:
                    new_item.EfficiencyLevel = enchants["minecraft:efficiency"]
            except Exception:
                pass

        try:
            new_item.ItemOrder = (db.session.query(func.max(Item.ItemOrder)).filter_by(CrateID=str(new_item.CrateID)).scalar() or 0) + 1
        except Exception:
            new_item.ItemOrder = 1

        db.session.add(new_item)
        db.session.commit()
        log_type = "Item"

    image_b64 = data.get("image_base64")
    if image_b64:
        try:
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(image_b64)

            loc = get_misc_icon_directory() if is_misc else get_icon_directory()
            target_path = os.path.join(loc, f"{new_item.id}.png")

            with open(target_path, "wb") as f:
                f.write(img_bytes)

            new_item.ImageType = "png"
            db.session.commit()
        except Exception as e:
            app.logger.error(f"Error saving item image: {e}")

    try:
        uploadLog(authenticated_user, log_type, f"Added item '{new_item.ItemName}' via Fabric mod", new_item.id)
    except Exception:
        pass

    return jsonify({
        "success": True,
        "message": f"Item '{new_item.ItemName}' added successfully.",
        "item_id": new_item.id
    }), 201


@app.route('/api/v1/admin/item/<int:item_id>', methods=['PATCH'])
@api_permission_level_required(90)
def api_admin_update_item(authenticated_user, item_id):
    """Updates editable metadata on an existing crate or misc item."""
    item = Item.query.filter_by(id=item_id).first()
    is_misc = False

    if not item:
        item = MiscellaneousItem.query.filter_by(id=item_id).first()
        is_misc = True

    if not item:
        return jsonify({"success": False, "error": f"Item with ID {item_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    updatable_fields = [
        "CrateID", "GroupID", "TagPrimary", "TagSecondary", "TagTertiary",
        "TagQuaternary", "TagQuinary", "TagSenary", "TagSeptenary",
        "WinPercentage", "RarityHuman", "RarityHTML", "ItemName",
        "ItemNameHTML", "Notes", "ItemHuman", "ItemHTML", "ItemOrder",
        "RawData"
    ]

    for field in updatable_fields:
        if field in data and hasattr(item, field):
            setattr(item, field, data[field])

    if not is_misc and item.RawData:
        item_tags = {
            getattr(item, "TagPrimary", None), getattr(item, "TagSecondary", None),
            getattr(item, "TagTertiary", None), getattr(item, "TagQuaternary", None),
            getattr(item, "TagQuinary", None), getattr(item, "TagSenary", None),
            getattr(item, "TagSeptenary", None)
        }
        tool_set = {"Pickaxe", "Axe", "Hoe", "Shovel", "Shears"}

        if len(item_tags.intersection(tool_set)) > 0:
            try:
                item_nbt = json.loads(item.RawData)
                components = item_nbt.get("components", {})
                enchants = components.get("minecraft:enchantments", {})
                if "minecraft:efficiency" in enchants:
                    item.EfficiencyLevel = enchants["minecraft:efficiency"]
            except Exception:
                pass

    db.session.commit()

    try:
        log_type = "MiscItem" if is_misc else "Item"
        uploadLog(authenticated_user, log_type, f"Updated item #{item.id} via Fabric mod", item.id)
    except Exception:
        pass

    return jsonify({
        "success": True,
        "message": f"Item #{item.id} updated successfully."
    }), 200


@app.route('/api/v1/admin/crate/<int:crate_id>/items', methods=['GET'])
@api_permission_level_required(90)
def api_admin_get_crate_items(authenticated_user, crate_id):
    """Fetches all items belonging to a crate ordered by ItemOrder."""
    try:
        items = Item.query.filter(
            or_(Item.CrateID == crate_id, Item.CrateID == str(crate_id))
        ).order_by(Item.ItemOrder.asc()).all()

        out = []
        for it in items:
            out.append({
                "id": it.id,
                "name": it.ItemName or "Unknown",
                "rarity": it.RarityHuman or "Common",
                "order": it.ItemOrder or 0,
                "win_percentage": it.WinPercentage or "0%",
                "primary_tag": it.TagPrimary or "None",
                "secondary_tag": it.TagSecondary or "None",
                "tertiary_tag": it.TagTertiary or "None",
                "quaternary_tag": it.TagQuaternary or "None",
                "quinary_tag": it.TagQuinary or "None",
                "senary_tag": it.TagSenary or "None",
                "septenary_tag": it.TagSeptenary or "None",
                "notes": it.Notes or ""
            })

        return jsonify({
            "success": True,
            "crate_id": crate_id,
            "count": len(out),
            "items": out
        }), 200
    except Exception as e:
        app.logger.error(f"Error fetching crate items: {e}")
        return jsonify({"success": False, "error": str(e), "items": []}), 500


@app.route('/api/v1/admin/item/<int:item_id>', methods=['DELETE'])
@api_permission_level_required(90)
def api_admin_delete_item(authenticated_user, item_id):
    """Deletes an item record and cleans up its icon file from disk."""
    item_type = request.args.get('type', '').lower()
    item = None
    is_misc = False

    if item_type == 'misc':
        item = MiscellaneousItem.query.filter_by(id=item_id).first()
        is_misc = True
    elif item_type == 'crate':
        item = Item.query.filter_by(id=item_id).first()
        is_misc = False
    else:
        item = Item.query.filter_by(id=item_id).first()
        if not item:
            item = MiscellaneousItem.query.filter_by(id=item_id).first()
            is_misc = True

    if not item:
        return jsonify({"success": False, "error": f"Item with ID {item_id} not found"}), 404

    try:
        loc = get_misc_icon_directory() if is_misc else get_icon_directory()

        for ext in (".png", ".gif", ".jpg", ".jpeg", ".webp"):
            icon_file = os.path.join(loc, f"{item_id}{ext}")
            if os.path.exists(icon_file):
                try:
                    os.remove(icon_file)
                except Exception as img_err:
                    app.logger.warning(f"Could not remove icon {icon_file}: {img_err}")

        item_name = item.ItemName
        db.session.delete(item)
        db.session.commit()

        try:
            log_type = "MiscItem" if is_misc else "Item"
            uploadLog(authenticated_user, log_type, f"Deleted item #{item_id} ('{item_name}') via Fabric mod", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Item #{item_id} deleted successfully."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting item {item_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/item/<int:item_id>/icon', methods=['POST'])
@api_permission_level_required(90)
def api_admin_upload_item_icon(authenticated_user, item_id):
    """Multipart/form-data upload endpoint for replacing an item's icon."""
    try:
        # Check explicit type query parameter first (?type=misc or ?type=crate)
        target_type = request.args.get('type', '').lower()

        item = None
        is_misc = False

        if target_type == 'misc':
            item = MiscellaneousItem.query.filter_by(id=item_id).first()
            is_misc = True
        elif target_type == 'crate':
            item = Item.query.filter_by(id=item_id).first()
            is_misc = False
        else:
            # Fallback auto-detection: check MiscellaneousItem first if not specified
            item = MiscellaneousItem.query.filter_by(id=item_id).first()
            if item:
                is_misc = True
            else:
                item = Item.query.filter_by(id=item_id).first()
                is_misc = False

        if not item:
            app.logger.error(f"[AdminApi] Item ID {item_id} not found in database (type={target_type})")
            return jsonify({"success": False, "error": f"Item with ID {item_id} not found"}), 404

        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "error": "Empty filename"}), 400

        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'png'
        if ext not in ['png', 'gif', 'jpg', 'jpeg', 'webp']:
            return jsonify({"success": False, "error": "Unsupported image format"}), 400

        icon_dir = get_misc_icon_directory() if is_misc else get_icon_directory()
        folder_name = "Misc_Icons" if is_misc else "Icons"

        target_filename = f"{item_id}.{ext}"
        target_path = os.path.join(icon_dir, target_filename)

        for old_ext in ('.png', '.gif', '.jpg', '.jpeg', '.webp'):
            old_file = os.path.join(icon_dir, f"{item_id}{old_ext}")
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                except Exception:
                    pass

        file.save(target_path)
        item.ImageType = ext
        db.session.commit()

        app.logger.info(f"[AdminApi] Saved icon for item #{item_id} to {target_path} (is_misc={is_misc})")

        return jsonify({
            "success": True,
            "item_id": item_id,
            "image_type": ext,
            "url": f"/static/images/{folder_name}/{target_filename}"
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to upload icon for item {item_id}: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/crate/<int:crate_id>/reorder', methods=['POST'])
@api_permission_level_required(90)
def api_admin_reorder_crate_items(authenticated_user, crate_id):
    """Updates the sequence order of items inside a crate."""
    data = request.get_json()
    if not data or 'item_ids' not in data:
        return jsonify({"success": False, "error": "Missing item_ids list"}), 400

    item_ids = data.get('item_ids', [])
    if not isinstance(item_ids, list):
        return jsonify({"success": False, "error": "item_ids must be a list"}), 400

    try:
        for index, item_id in enumerate(item_ids, start=1):
            Item.query.filter_by(id=item_id).update({"ItemOrder": index})

        db.session.commit()

        try:
            uploadLog(authenticated_user, "Item", f"Reordered {len(item_ids)} items in Crate #{crate_id} via Fabric mod", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Successfully reordered {len(item_ids)} items."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to reorder items for crate {crate_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/miscgroup/<int:group_id>/reorder', methods=['POST'])
@api_permission_level_required(90)
def api_admin_reorder_misc_group_items(authenticated_user, group_id):
    """Updates display order for items within a miscellaneous group."""
    group = MiscellaneousGroup.query.filter_by(id=group_id).first()
    if not group:
        return jsonify({"success": False, "error": f"Misc group with ID {group_id} not found"}), 404

    data = request.get_json()
    if not data or "item_ids" not in data:
        return jsonify({"success": False, "error": "Missing 'item_ids' list in payload"}), 400

    item_ids = data.get("item_ids", [])
    if not isinstance(item_ids, list):
        return jsonify({"success": False, "error": "'item_ids' must be a list of integer IDs"}), 400

    try:
        group_items = {
            item.id: item
            for item in MiscellaneousItem.query.filter(
                (MiscellaneousItem.GroupID == str(group_id)) |
                (MiscellaneousItem.GroupID == group.GroupName) |
                (MiscellaneousItem.GroupID == group.URLTag)
            ).all()
        }

        for order_idx, item_id in enumerate(item_ids, start=1):
            if item_id in group_items:
                group_items[item_id].ItemOrder = order_idx

        db.session.commit()

        try:
            uploadLog(authenticated_user, "MiscGroup", f"Reordered {len(item_ids)} items in group '{group.GroupName}' via Fabric mod", group.id)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Successfully updated display order for group '{group.GroupName}'."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error reordering items for misc group {group_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/v1/admin/miscgroup', methods=['POST'])
@api_permission_level_required(90)
def api_admin_create_miscgroup(authenticated_user):
    """Creates a new miscellaneous group container."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    group_name = (data.get("GroupName") or "").strip()
    release_date = (data.get("ReleaseDate") or "").strip()
    url_tag = (data.get("URLTag") or data.get("GroupTag") or "").strip()
    group_type = (data.get("GroupType") or "Furniture").strip()
    notes = (data.get("Notes") or "").strip()

    if not group_name or not release_date or not url_tag:
        return jsonify({"success": False, "error": "GroupName, ReleaseDate, and URLTag are required"}), 400

    existing = MiscellaneousGroup.query.filter(func.lower(MiscellaneousGroup.URLTag) == url_tag.lower()).first()
    if existing:
        return jsonify({"success": False, "error": f"Group Tag '{url_tag}' is already in use"}), 400

    try:
        new_group = MiscellaneousGroup()
        new_group.GroupName = group_name
        new_group.ReleaseDate = release_date
        new_group.URLTag = url_tag
        new_group.GroupType = group_type
        new_group.Notes = notes

        try:
            new_group.GroupOrder = (db.session.query(func.max(MiscellaneousGroup.GroupOrder)).scalar() or 0) + 1
        except Exception:
            new_group.GroupOrder = 1

        db.session.add(new_group)
        db.session.commit()

        try:
            uploadLog(authenticated_user, "Group", f"added to db via Fabric mod..", new_group.id)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Group '{group_name}' created successfully.",
            "group_id": new_group.id
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating misc group: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/miscgroup/<int:group_id>', methods=['PATCH'])
@api_permission_level_required(90)
def api_admin_update_miscgroup(authenticated_user, group_id):
    """Updates metadata on an existing miscellaneous group container."""
    group = MiscellaneousGroup.query.filter_by(id=group_id).first()
    if not group:
        return jsonify({"success": False, "error": f"Group #{group_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    new_tag = (data.get("URLTag") or data.get("GroupTag") or "").strip()
    if new_tag and new_tag.lower() != (group.URLTag or "").lower():
        existing = MiscellaneousGroup.query.filter(
            func.lower(MiscellaneousGroup.URLTag) == new_tag.lower(),
            MiscellaneousGroup.id != group_id
        ).first()
        if existing:
            return jsonify({"success": False, "error": f"Group Tag '{new_tag}' is already in use"}), 400

    try:
        old_data = group.to_dict(["*"])

        if "GroupName" in data and data["GroupName"].strip():
            group.GroupName = data["GroupName"].strip()
        if "ReleaseDate" in data and data["ReleaseDate"].strip():
            group.ReleaseDate = data["ReleaseDate"].strip()
        if new_tag:
            group.URLTag = new_tag
        if "GroupType" in data and data["GroupType"].strip():
            group.GroupType = data["GroupType"].strip()
        if "Notes" in data:
            group.Notes = data["Notes"].strip()

        new_data = group.to_dict(["*"])
        db.session.commit()

        for key in old_data.keys():
            if old_data.get(key) != new_data.get(key):
                try:
                    uploadLog(authenticated_user, "Group", f"{key} | '{old_data[key]}'-->'{new_data[key]}'.", group.id)
                except Exception:
                    pass

        return jsonify({
            "success": True,
            "message": f"Group #{group.id} updated successfully."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating misc group {group_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/miscgroup/<int:group_id>', methods=['DELETE'])
@api_permission_level_required(90)
def api_admin_delete_miscgroup(authenticated_user, group_id):
    """Deletes a misc group and all its associated items."""
    group = MiscellaneousGroup.query.filter_by(id=group_id).first()
    if not group:
        return jsonify({"success": False, "error": f"Group #{group_id} not found"}), 404

    group_name = group.GroupName
    try:
        items_to_delete = MiscellaneousItem.query.filter(
            or_(
                MiscellaneousItem.GroupID == str(group_id),
                MiscellaneousItem.GroupID == group.GroupName,
                MiscellaneousItem.GroupID == group.URLTag
            )
        ).all()

        MiscellaneousItem.query.filter(
            or_(
                MiscellaneousItem.GroupID == str(group_id),
                MiscellaneousItem.GroupID == group.GroupName,
                MiscellaneousItem.GroupID == group.URLTag
            )
        ).delete(synchronize_session=False)

        db.session.delete(group)
        db.session.commit()

        try:
            uploadLog(authenticated_user, "Group", f"{group_name} deleted from db.", None)
            for it in items_to_delete:
                uploadLog(authenticated_user, "Misc Item", f"{it.ItemName} deleted from db with {group_name}.", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Group #{group_id} ('{group_name}') and {len(items_to_delete)} associated items deleted."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting misc group {group_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/v1/admin/crate', methods=['POST'])
@api_permission_level_required(90)
def api_admin_create_crate(authenticated_user):
    """Creates a new crate container."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    crate_name = (data.get("CrateName") or "").strip()
    release_date = (data.get("ReleaseDate") or "").strip()
    url_tag = (data.get("URLTag") or data.get("CrateTag") or "").strip()
    crate_type = (data.get("CrateType") or "Seasonal").strip()

    if not crate_name or not release_date or not url_tag:
        return jsonify({"success": False, "error": "CrateName, ReleaseDate, and CrateTag are required"}), 400

    existing = Crate.query.filter(func.lower(Crate.URLTag) == url_tag.lower()).first()
    if existing:
        return jsonify({"success": False, "error": f"Crate Tag '{url_tag}' is already in use"}), 400

    try:
        new_crate = Crate(
            CrateName=crate_name,
            ReleaseDate=release_date,
            URLTag=url_tag,
            CrateType=crate_type
        )
        db.session.add(new_crate)
        db.session.commit()

        try:
            uploadLog(authenticated_user, "Crate", "added to db..", new_crate.id)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Crate '{crate_name}' created successfully.",
            "crate_id": new_crate.id
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating crate: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/crate/<int:crate_id>', methods=['PATCH'])
@api_permission_level_required(90)
def api_admin_update_crate(authenticated_user, crate_id):
    """Updates metadata on an existing crate container."""
    crate = Crate.query.filter_by(id=crate_id).first()
    if not crate:
        return jsonify({"success": False, "error": f"Crate #{crate_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    new_tag = (data.get("URLTag") or data.get("CrateTag") or "").strip()
    if new_tag and new_tag.lower() != (crate.URLTag or "").lower():
        existing = Crate.query.filter(func.lower(Crate.URLTag) == new_tag.lower(), Crate.id != crate_id).first()
        if existing:
            return jsonify({"success": False, "error": f"Crate Tag '{new_tag}' is already in use by crate #{existing.id}"}), 400

    try:
        old_data = crate.to_dict(["*"])

        if "CrateName" in data and data["CrateName"].strip():
            crate.CrateName = data["CrateName"].strip()
        if "ReleaseDate" in data and data["ReleaseDate"].strip():
            crate.ReleaseDate = data["ReleaseDate"].strip()
        if new_tag:
            crate.URLTag = new_tag
        if "CrateType" in data and data["CrateType"].strip():
            crate.CrateType = data["CrateType"].strip()

        new_data = crate.to_dict(["*"])
        db.session.commit()

        for key in old_data.keys():
            if old_data.get(key) != new_data.get(key):
                try:
                    uploadLog(authenticated_user, "Crate", f"{key} | '{old_data[key]}'-->'{new_data[key]}'.", crate.id)
                except Exception:
                    pass

        return jsonify({
            "success": True,
            "message": f"Crate #{crate.id} updated successfully."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating crate {crate_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/crate/<int:crate_id>', methods=['DELETE'])
@api_permission_level_required(90)
def api_admin_delete_crate(authenticated_user, crate_id):
    """Deletes a crate container and its associated items."""
    crate = Crate.query.filter_by(id=crate_id).first()
    if not crate:
        return jsonify({"success": False, "error": f"Crate #{crate_id} not found"}), 404

    crate_name = crate.CrateName
    try:
        items_to_delete = Item.query.filter(
            or_(Item.CrateID == crate_id, Item.CrateID == str(crate_id))
        ).all()

        Item.query.filter(
            or_(Item.CrateID == crate_id, Item.CrateID == str(crate_id))
        ).delete(synchronize_session=False)

        db.session.delete(crate)
        db.session.commit()

        try:
            uploadLog(authenticated_user, "Crate", f"{crate_name} deleted from db.", None)
            for it in items_to_delete:
                uploadLog(authenticated_user, "Item", f"{it.ItemName} deleted from db with {crate_name}.", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Crate #{crate_id} ('{crate_name}') and {len(items_to_delete)} associated items deleted."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting crate {crate_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/set', methods=['POST'])
@api_permission_level_required(90)
def api_admin_create_set(authenticated_user):
    """Creates a new armor or item set."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    name = (data.get("Name") or "").strip()
    set_type = (data.get("Type") or "Armor Set").strip()
    description = (data.get("SetDescription") or "").strip()
    item_list = data.get("ItemList")

    if not name or not description or item_list is None:
        return jsonify({"success": False, "error": "Name, Description, and ItemList are required"}), 400

    if isinstance(item_list, list):
        item_list_str = json.dumps(item_list)
    else:
        try:
            item_list_str = json.dumps(json.loads(str(item_list)))
        except Exception:
            return jsonify({"success": False, "error": "ItemList must be a valid array of item IDs"}), 400

    try:
        max_order = db.session.query(func.max(ItemSet.SetOrder)).scalar() or 0
        new_set = ItemSet(
            Name=name,
            Type=set_type,
            SetDescription=description,
            ItemList=item_list_str,
            SetOrder=max_order + 1
        )
        db.session.add(new_set)
        db.session.commit()

        try:
            uploadLog(authenticated_user, "Set", f"{new_set.Name} added to db.", new_set.SetOrder)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Set '{name}' created successfully.",
            "set_id": new_set.id
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating set: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/set/<int:set_id>', methods=['PATCH'])
@api_permission_level_required(90)
def api_admin_update_set(authenticated_user, set_id):
    """Updates an existing item set."""
    set_entry = ItemSet.query.filter_by(id=set_id).first()
    if not set_entry:
        return jsonify({"success": False, "error": f"Set #{set_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    try:
        old_data = set_entry.to_dict(["*"])

        if "Name" in data and data["Name"].strip():
            set_entry.Name = data["Name"].strip()
        if "Type" in data and data["Type"].strip():
            set_entry.Type = data["Type"].strip()
        if "SetDescription" in data:
            set_entry.SetDescription = data["SetDescription"].strip()
        if "ItemList" in data:
            item_list = data["ItemList"]
            if isinstance(item_list, list):
                set_entry.ItemList = json.dumps(item_list)
            else:
                set_entry.ItemList = json.dumps(json.loads(str(item_list)))

        new_data = set_entry.to_dict(["*"])
        db.session.commit()

        for key in old_data.keys():
            if old_data.get(key) != new_data.get(key):
                try:
                    uploadLog(authenticated_user, "Set", f"{set_entry.Name} | {key} | '{old_data[key]}'-->'{new_data[key]}'.", set_entry.id)
                except Exception:
                    pass

        return jsonify({
            "success": True,
            "message": f"Set #{set_entry.id} updated successfully."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating set {set_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/set/<int:set_id>', methods=['DELETE'])
@api_permission_level_required(90)
def api_admin_delete_set(authenticated_user, set_id):
    """Deletes an item set record."""
    set_entry = ItemSet.query.filter_by(id=set_id).first()
    if not set_entry:
        return jsonify({"success": False, "error": f"Set #{set_id} not found"}), 404

    set_name = set_entry.Name
    try:
        db.session.delete(set_entry)
        db.session.commit()

        try:
            uploadLog(authenticated_user, "Set", f"{set_name} deleted from db.", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Set #{set_id} ('{set_name}') deleted successfully."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting set {set_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/set/reorder', methods=['POST'])
@api_permission_level_required(90)
def api_admin_reorder_sets(authenticated_user):
    """Reorders sets according to a list of IDs."""
    data = request.get_json()
    if not data or 'set_ids' not in data:
        return jsonify({"success": False, "error": "Missing set_ids list"}), 400

    set_ids = data.get('set_ids', [])
    try:
        for index, set_id in enumerate(set_ids, start=1):
            ItemSet.query.filter_by(id=set_id).update({"SetOrder": index})

        db.session.commit()

        try:
            uploadLog(authenticated_user, "Set", f"{len(set_ids)} sets reordered.", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Successfully reordered {len(set_ids)} sets."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error reordering sets: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/crates/reorder', methods=['POST'])
@api_permission_level_required(90)
def api_admin_reorder_crates(authenticated_user):
    """Reorders crate categories."""
    data = request.get_json()
    if not data or 'crate_ids' not in data:
        return jsonify({"success": False, "error": "Missing crate_ids list"}), 400

    crate_ids = data.get('crate_ids', [])
    if not isinstance(crate_ids, list):
        return jsonify({"success": False, "error": "crate_ids must be a list"}), 400

    try:
        order_attr = 'CrateOrder' if hasattr(Crate, 'CrateOrder') else ('Order' if hasattr(Crate, 'Order') else None)

        if order_attr:
            for index, c_id in enumerate(crate_ids, start=1):
                Crate.query.filter_by(id=c_id).update({order_attr: index})
            db.session.commit()

        try:
            uploadLog(authenticated_user, "Crate", f"Reordered {len(crate_ids)} crates via Fabric mod", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Successfully reordered {len(crate_ids)} crates."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to reorder crates: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/v1/admin/miscgroups/reorder', methods=['POST'])
@api_permission_level_required(90)
def api_admin_reorder_miscgroups(authenticated_user):
    """Reorders miscellaneous group categories."""
    data = request.get_json()
    if not data or 'group_ids' not in data:
        return jsonify({"success": False, "error": "Missing group_ids list"}), 400

    group_ids = data.get('group_ids', [])
    if not isinstance(group_ids, list):
        return jsonify({"success": False, "error": "group_ids must be a list"}), 400

    try:
        for index, g_id in enumerate(group_ids, start=1):
            MiscellaneousGroup.query.filter_by(id=g_id).update({"GroupOrder": index})

        db.session.commit()

        try:
            uploadLog(authenticated_user, "MiscGroup", f"Reordered {len(group_ids)} misc groups via Fabric mod", None)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Successfully reordered {len(group_ids)} misc groups."
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error reordering misc groups: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/admin/missing_images', methods=['GET'])
@api_permission_level_required(90)
def api_missing_images(authenticated_user):
    """Scans static icon directories and returns IDs for items lacking files on disk."""
    crate_dir = Path(get_icon_directory())
    misc_dir = Path(get_misc_icon_directory())

    crate_files = set(p.name for p in crate_dir.iterdir() if p.is_file()) if crate_dir.exists() else set()
    misc_files = set(p.name for p in misc_dir.iterdir() if p.is_file()) if misc_dir.exists() else set()

    missing_crate_ids = []
    items = Item.query.order_by(Item.ItemOrder).all()
    for item in items:
        if not item.ImageType or (f"{item.id}.png" not in crate_files and f"{item.id}.gif" not in crate_files):
            missing_crate_ids.append(item.id)

    missing_misc_ids = []
    misc_items = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
    for item in misc_items:
        if not item.ImageType or (f"{item.id}.png" not in misc_files and f"{item.id}.gif" not in misc_files):
            missing_misc_ids.append(item.id)

    return jsonify({
        "missing_crate_ids": missing_crate_ids,
        "missing_misc_ids": missing_misc_ids
    }), 200
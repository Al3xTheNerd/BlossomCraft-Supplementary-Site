from flask import render_template, request, flash, url_for, redirect
from sqlalchemy import or_, not_, and_
from json import loads
from typing import List
from sys import platform
from random import choices
from collections import defaultdict

from core.SinglePageTools import bp
from core.ItemListing.models import Item, Crate
from core.ItemListing.utils import TagCols
from core.SinglePageTools.models import ItemTracker
from core.MiscellaneousItemList.models import MiscellaneousItem, MiscellaneousGroup
from core.utils import randomCode
import core.config as c
from core.extensions import db


try:
    from config import jobsInfo, JobsSecrets
except:
    jobsInfo = None
    JobsSecrets = None

@bp.route('/')
def Index():
    return render_template("SinglePageTools/public/index.html")

@bp.route('/jobspayouts')
def JobsPayouts():
    return render_template("SinglePageTools/public/jobspayout.html", Info = jobsInfo, Secrets = JobsSecrets)

@bp.route('/blockspeed')
def BlockSpeed():
    sortedItems = {
        "Pickaxe" : [],
        "Axe" : [],
        "Hoe" : [],
        "Shovel" : [],
        "Shears" : []}
    fullList = []
    items: List[Item] = Item.query.filter(
        and_(
            not_(or_(col.contains("Repeat Appearance") for col in TagCols)), #type:ignore
            or_(
                or_(col.contains("Pickaxe") for col in TagCols),#type: ignore
                or_(col.contains("Axe") for col in TagCols),#type: ignore
                or_(col.contains("Hoe") for col in TagCols),#type: ignore
                or_(col.contains("Shovel") for col in TagCols), #type: ignore
                or_(col.contains("Shears") for col in TagCols), # type: ignore
            ))).order_by(Item.ItemOrder).all()
    toolSpeeds = {
        "golden" : 12,
        "netherite" : 9,
        "diamond" : 8,
        "iron" : 6,
        "copper" : 5,
        "stone" : 4,
        "wooden" : 2
    }
    for item in items:
        breakSpeed = 1
        for material, speed in toolSpeeds.items():
            if material in loads(item.RawData)["id"]:
                breakSpeed = speed
            if "Shears" in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuaternary]:
                breakSpeed = 2

        fullList.append({ "name": item.ItemName, "efficiency" : item.EfficiencyLevel, "submerged_mining_speed" : item.SubmergedMiningSpeedAttribute, "speed" : breakSpeed})
        toolTypes = list(set([item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuaternary]).intersection(set(["Pickaxe", "Axe", "Hoe", "Shovel", "Shears"])))
        for type in toolTypes:
            sortedItems[type].append({ "name": item.ItemName, "efficiency" : item.EfficiencyLevel, "submerged_mining_speed" : item.SubmergedMiningSpeedAttribute, "speed" : breakSpeed})
        
    return render_template("SinglePageTools/public/blockbreakspeed.html", itemList = sortedItems, fullList = fullList, blocksToCalculate = c.blocksForBreakSpeedCalculator)

@bp.route('/itemtracker', methods=('GET', 'POST'))
def ItemTrackerRoute():
    if request.method == 'POST':
        code = loads(request.form['importCode'])
        if len(code) < 1:
            flash("Code must have at least one item to upload.")
        else:
            attemptedSearch = ItemTracker.query.filter(ItemTracker.ItemList == str(code)).first()
            if attemptedSearch:
                flash(f"Your upload code is: <code>{attemptedSearch.Code}</code>. Please provide this code to the bot or service requesting it to import your item tracker information.")
            else:
                randCode = randomCode(6)
                if not ItemTracker.query.filter(ItemTracker.Code == randCode).first():
                    new_entry = ItemTracker(Code = randCode, ItemList = str(code)) # type: ignore
                    db.session.add(new_entry)
                    db.session.commit()
                    flash(f"Your upload code is: <code>{randCode}</code>. Please provide this code to the bot or service requesting it to import your item tracker information.")
                else:
                    flash("Something went wrong, please try again.")
    sortedItems = {}
    idToCrateList = {}
    items: List[Item] = Item.query.filter(
        not_(or_(col.contains("Repeat Appearance") for col in TagCols)) #type:ignore
    ).order_by(Item.ItemOrder).all()
    count = len(items)
    crateList: List[Crate] = Crate.query.order_by(Crate.id).all()
    for crate in crateList:
        itemNames = []
        for item in items:
            name = item.ItemName
            if item.ItemNameHTML in itemNames or "(" in item.ItemName:
                name = item.ItemName
            else:
                name= item.ItemNameHTML
                itemNames.append(item.ItemNameHTML)
            formattedItem = {
                "Name" : name,
                "id" : item.id,
                "Tags" : [tag for tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSeptenary, item.TagSenary] if tag],
                "ImageType" : item.ImageType if item.ImageType else ""
            }
            if int(item.CrateID) == int(crate.id):
                if crate.CrateName in sortedItems:
                    idToCrateList[crate.CrateName].append(item.id)
                    sortedItems[crate.CrateName].append(formattedItem)
                else:
                    idToCrateList[crate.CrateName] = [item.id]
                    sortedItems[crate.CrateName] = [formattedItem]
    return render_template("SinglePageTools/public/itemTracker.html", sortedItems = sortedItems, idCrateList = idToCrateList, validTags = c.validTags, page="newtracker", count=count)

@bp.route('/miscitemtracker', methods=('GET', 'POST'))
def MiscItemTracker():
    if request.method == 'POST':
        code = loads(request.form['importCode'])
        if len(code) < 1:
            flash("Code must have at least one item to upload.")
        else:
            attemptedSearch = ItemTracker.query.filter(ItemTracker.ItemList == str(code)).first()
            if attemptedSearch:
                flash(f"Your upload code is: <code>{attemptedSearch.Code}</code>. Please provide this code to the bot or service requesting it to import your item tracker information.")
            else:
                randCode = randomCode(6)
                if not ItemTracker.query.filter(ItemTracker.Code == randCode).first():
                    new_entry = ItemTracker(Code = randCode, ItemList = str(code)) # type: ignore
                    db.session.add(new_entry)
                    db.session.commit()
                    flash(f"Your upload code is: <code>{randCode}</code>. Please provide this code to the bot or service requesting it to import your item tracker information.")
                else:
                    flash("Something went wrong, please try again.")
    sortedItems = {}
    idToCrateList = {}
    items: List[MiscellaneousItem] = MiscellaneousItem.query.order_by(MiscellaneousItem.ItemOrder).all()
    count = len(items)
    
    groupList: List[MiscellaneousGroup] = MiscellaneousGroup.query.order_by(MiscellaneousGroup.GroupOrder).all()
    groupTypes = []
    for group in groupList:
        if group.GroupType not in groupTypes:
            groupTypes.append(group.GroupType)
        itemNames = []
        for item in items:
            name = item.ItemName
            #if item.ItemNameHTML in itemNames:
            #    name = item.ItemName
            #else:
            #    name= item.ItemNameHTML
            #    itemNames.append(item.ItemNameHTML)
            formattedItem = {
                "Name" : name,
                "id" : item.id,
                "Tags" : [group.GroupType],
                "ImageType" : item.ImageType if item.ImageType else ""
            }
            if int(item.GroupID) == int(group.id):
                if group.GroupName in sortedItems:
                    idToCrateList[group.GroupName].append(item.id)
                    sortedItems[group.GroupName].append(formattedItem)
                else:
                    idToCrateList[group.GroupName] = [item.id]
                    sortedItems[group.GroupName] = [formattedItem]
    return render_template("SinglePageTools/public/itemTracker.html", sortedItems = sortedItems, idCrateList = idToCrateList, validTags = groupTypes, page="miscitemtracker", count=count)

@bp.route('/inventory', methods=['POST', 'GET']) # type: ignore
def InventoryPlanner():
    items: List[Item] = Item.query.all()
    
    formattedItems = []
    blankSlot = f"""<img height='44' width='44' src="{url_for('static', filename = f"images/Icons/0.png")}">"""
    for item in items:
        hoverableHTML = f"""<img height='44' width='44' src="{url_for('static', filename = f"images/Icons/{item.id}.{item.ImageType}")}" data-bs-custom-class="wide-tooltip" data-bs-toggle="tooltip" data-bs-html="true" data-bs-placement="bottom" data-bs-title="<div class='give-preview-text-outer marker'><div class='give-preview-text w-100'><div class='give-preview-text-inner text-start'>{item.ItemHTML.replace('"', '&quot;')}</div></div></div>">"""
        formattedItems.append({
            "Name" : item.ItemName,
            "HTML" : hoverableHTML,
            "Tags" : [tag for tag in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSeptenary, item.TagSenary] if tag]
        })
    return render_template("SinglePageTools/public/inventory.html", items = formattedItems, validTags = c.validTags, blankSlot = blankSlot)

@bp.route('/gradient')
def GradientMaker():
    return render_template("SinglePageTools/public/gradientMaker.html")


@bp.route('/gamble', methods=['POST', 'GET'])
def Gambling():
    amount = request.form.get('amount')
    if not amount: amount = 1
    amount = int(amount)
    if platform != "win32" and amount > c.gambleLimit: amount = c.gambleLimit
    # TODO: Gambling limit should be in the editable configuration.
    crate = request.form.get("crate")
    if not crate or crate == "all":
        crate = "all"
        items: List[Item] | None = Item.query.order_by(Item.ItemOrder).all()
    else:
        try:
            crate = str(crate)
            items = Item.query.filter_by(CrateID = crate).order_by(Item.ItemOrder).all()
        except:
            flash("Something went wrong.")
            return redirect(url_for("gamble"))
    
    validItems = [item for item in items if item.WinPercentage not in (None, 0, '')]
    cleanWeights = [float(item.WinPercentage) for item in validItems]
    
    items = choices(validItems, cleanWeights, k = amount)
    
    resultCrates = list(set([int(item.CrateID) for item in items]))
    resultCrates.sort()
    
    crateNames = {
        crate.id: crate.CrateName for crate in Crate.query.all()
    }
    
    stats = defaultdict(lambda: defaultdict(int))
    for crateID, crateName in crateNames.items():
        stats[crateName] = defaultdict(int)
    
    
    for item in items:
        crateName = crateNames[int(item.CrateID)]
        stats[crateName][item.ItemNameHTML] += 1
    stats = {
        crate: dict(sorted(itemCounts.items(), key=lambda x: x[1]))
        for crate, itemCounts in stats.items()
    }
    
    for crateName in list(stats.keys()):
        if len(stats[crateName]) == 0:
            del stats[crateName]
    return render_template("SinglePageTools/public/gamble.html", Items = set(items), amount = amount, recentCrate = crate, stats = stats, Crates = dict(reversed(crateNames.items())))

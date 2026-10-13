from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from collections import Counter
from json import loads
from typing import List

from core.ItemListing import bp
from core.ItemListing.models import Item, Crate
from core.ItemListing.models import Set as ItemSets
from core.ItemListing.utils import getTermFilters, TagCols, SingleTagQuery, noDupes, currentCrateData

from core.MiscellaneousItemList.models import MiscellaneousGroup
from core.config import server_rarity_list


import core.config as c


@bp.route("/", methods = ["GET", "POST"])
def Index():
    items = None
    if request.method == 'POST':
        search = request.form['search']
        if not search: 
            flash("Try entering a query!")
        conditions = []
        
        conditions += getTermFilters(search, Item) # type: ignore
            
        items = Item.query.where(*conditions).order_by(Item.ItemOrder).all()
        if not items:
            items = None
            flash("No results found!")
    if items:
        items = noDupes(items)  
    return render_template("ItemListing/public/index.html", Items=items)


@bp.route('/all')
@bp.route('/all/<int:page>/')
@bp.route('/all/<int:page>/<int:quantity>')
def AllItems(page: int=1, quantity:int=25):
    pagination = Item.query.order_by(Item.ItemOrder).paginate(page=page, per_page=quantity, error_out=False)
    return render_template("ItemListing/public/allitems.html", Items = pagination.items, pagination = pagination)


@bp.route('/item/<itemID>')
def SingleItem(itemID):
    item: Item | None = Item.query.filter_by(id = itemID).one_or_none()
    if item:
        PrimaryCrate: Crate | None = Crate.query.filter_by(id = item.CrateID).first()
        PrimaryConnectedGroup = MiscellaneousGroup.query.filter_by(id = item.ConnectedItems).one_or_none()
        if PrimaryCrate:
            item.CrateName = PrimaryCrate.CrateName
    else:
        item = Item()
        item.ItemHTML = "<div class='mc-gold'>This is not a valid item id. Try again, or don't, it's not actually my problem.</div>"
        item.id = 0
        PrimaryCrate = None
        PrimaryConnectedGroup = None
    return render_template("ItemListing/public/singleItem.html", PrimaryItem = item, PrimaryGroup = PrimaryConnectedGroup)

@bp.route('/rawitem/<itemID>')
def SingleItemRaw(itemID):
    item = Item.query.filter_by(id = itemID).first()
    if item:
        return render_template("ItemListing/public/singleItemRaw.html", item = item)
    else:
        flash("Item not found.")
        return redirect(url_for("all"))



@bp.route('/crate/<crateTag>')
def SingleCrate(crateTag):
    crate: Crate | None = Crate.query.filter_by(URLTag = crateTag).first()
    if crate:
        items = Item.query.filter_by(CrateID = crate.id).order_by(Item.ItemOrder).all()
        return render_template("ItemListing/public/genericDisplay.html", Items = items, Crate = crate)
    else:
        flash("Crate not found.")
        return redirect(url_for("ItemListing.AllCrates"))
    

@bp.route('/crates')
def AllCrates():
    crates: List[Crate] = Crate.query.all()
    crateList = {
        "Seasonal" : [],
        "Side" : [],
        "Misc" : [],
        "" : []
        }
    for crate in crates:
        crateList[crate.CrateType].append(crate)
    for key in list(crateList.keys()):
        if len(crateList[key]) == 0:
            del crateList[key]
    return render_template("ItemListing/public/allCrates.html", SortedCrates = crateList)


@bp.route('/tags')
def AllTags():
    stats = Counter()

    rows = Item.query.with_entities(
        Item.TagPrimary,
        Item.TagSecondary,
        Item.TagTertiary,
        Item.TagQuaternary,
        Item.TagQuinary,
        Item.TagSenary,
        Item.TagSeptenary,
    ).all()

    for row in rows:
        for tag in row:
            if tag:
                stats[tag] += 1
    return render_template("ItemListing/public/allTags.html", stats=stats, tags = c.tags)

@bp.route('/tag/<cat>/<tag>')
def SingleTag(cat, tag):
    items = None
    if cat in c.tags:
        if tag == "all":
            items = Item.query.filter(
                or_(
                    or_(Item.TagPrimary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagSecondary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagTertiary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagQuaternary == x for x in c.tags[cat]), # type: ignore
                    or_(Item.TagQuinary == x for x in c.tags[cat]), #type: ignore
                    or_(Item.TagSenary == x for x in c.tags[cat]), #type: ignore
                    or_(Item.TagSeptenary == x for x in c.tags[cat]) #type: ignore
                )
            ).order_by(Item.ItemOrder).all()
        else:
            items = SingleTagQuery(tag) # type: ignore
    if cat == 'Misc':
        items = SingleTagQuery(tag) # type: ignore
    return render_template("ItemListing/public/genericDisplay.html", Items = noDupes(items) if tag != "Repeat Appearance" else items, Category = cat, Tag = tag) # type: ignore

@bp.route('/sets')
def AllSets():
    sets: List[ItemSets] = ItemSets.query.all()
    sortedSets = {"" : []}
    for setType in c.validSetTypes:
        sortedSets[setType] = []
    for set in sets:
        sortedSets[set.Type].append(set)
    return render_template("ItemListing/public/allSets.html", sets = sortedSets)

@bp.route('/set/<setID>')
def SingleSet(setID):
    set: ItemSets | None = ItemSets.query.filter(ItemSets.id == setID).first()
    if not set:
        flash("That set does not exist. Try again some other day.")
        return redirect('/sets')
    items: List[Item] = Item.query.filter(Item.id.in_(loads(set.ItemList))).all()
    return render_template("ItemListing/public/singleSet.html", Items = items, set = set)


@bp.route('/stats')
def Stats():
    stats = Counter()

    rows = Item.query.with_entities(
        Item.TagPrimary,
        Item.TagSecondary,
        Item.TagTertiary,
        Item.TagQuaternary,
        Item.TagQuinary,
        Item.TagSenary,
        Item.TagSeptenary,
    ).all()

    for row in rows:
        for tag in row:
            if tag:
                stats[tag] += 1
    stats["Crate"] = Crate.query.count()
    return render_template("ItemListing/public/stats.html", stats = stats, total=Item.query.count())

@bp.route('/search', methods = ['GET', 'POST']) # type: ignore
def Search():
    formattedCrates = currentCrateData()
    rarityList = server_rarity_list
    items = []
    recentTerm, recentCrate, recentTag, recentTagTwo, recentTagThree, recentRarity = ("", "", "", "", "", "")
    if request.method == 'POST':
        form = request.form.to_dict()
        conditions = []
        if form["Term"]:
            recentTerm = form["Term"]
            conditions += getTermFilters(recentTerm, Item)
        if form["Crate"]:
            recentCrate = form["Crate"]
            conditions.append(Item.CrateID == int(form["Crate"]))
        if form["Tag"]:
            recentTag = form["Tag"]
            conditions.append(or_(col.is_(form["Tag"]) for col in TagCols)) # type: ignore
        if form["TagTwo"]:
            recentTagTwo = form["TagTwo"]
            conditions.append(or_(col.is_(form["TagTwo"]) for col in TagCols)) # type: ignore
        if form["TagThree"]:
            recentTagThree = form["TagThree"]
            conditions.append(or_(col.is_(form["TagThree"]) for col in TagCols)) # type: ignore
        if form["Rarity"]:
            recentRarity = form["Rarity"]
            rarity = ""
            if form["Rarity"] in rarityList:
                rarity = form["Rarity"]
                conditions.append(Item.RarityHuman.ilike(f"%{rarity}%"))
            if form["Rarity"] == "0":
                conditions.append(Item.RarityHuman.is_(""))

        items: List[Item] = Item.query.where(*conditions).order_by(Item.ItemOrder).all()
        

        if len(items) == 0:
            flash("No Results Found!", "dark")
    return render_template("ItemListing/public/search.html",
                           validTags = c.validTags,
                           currentCrates = formattedCrates,
                           rarityList = rarityList,
                           Items = items,
                           recentTerm = recentTerm,
                           recentTag = recentTag,
                           recentTagTwo = recentTagTwo,
                           recentTagThree = recentTagThree,
                           recentCrate = recentCrate,
                           recentRarity = recentRarity,
                           numResults = len(items))
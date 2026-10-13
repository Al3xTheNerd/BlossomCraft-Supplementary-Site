from sqlalchemy import or_
from re import sub
from typing import List
from collections import defaultdict
from sqlalchemy import desc
from core.ItemListing.models import Item, Crate

from core.MiscellaneousItemList.models import MiscellaneousItem

def roman_to_int(numeral: str):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    # Additive approach: check if current is smaller than next, if so, subtract
    for i in range(len(numeral)):
        if i + 1 < len(numeral) and roman_map[numeral[i]] < roman_map[numeral[i+1]]:
            total -= roman_map[numeral[i]]
        else:
            total += roman_map[numeral[i]]
    return total

def convert_roman_in_string(text: str):
    # Matches roman numerals (I,V,X,L,C,D,M) only if they are separate words
    pattern = r'\b[IVXLCDM]+\b'
    
    def replacer(match):
        return str(roman_to_int(match.group(0)))
    
    return sub(pattern, replacer, text)

def convert_int_to_roman(text: str):
    newText = text
    map = {
        10 : "X",
        9 : "IX",
        8 : "VIII",
        7 : "VII",
        6 : "VI",
        5 : "V",
        4 : "IV",
        3 : "III",
        2 : "II",
        1 : "I"
    }
    for num, roman in map.items():
        newText = newText.replace(str(num), roman)
    return newText


TagCols = [Item.TagPrimary, Item.TagSecondary, Item.TagTertiary, Item.TagQuaternary, Item.TagQuinary, Item.TagSenary, Item.TagSeptenary]
def noDupes(items: list[Item]) -> list[Item]:
    returnItems = [item for item in items if "Repeat Appearance" not in [item.TagPrimary, item.TagSecondary, item.TagTertiary, item.TagQuaternary, item.TagQuinary, item.TagSenary, item.TagSeptenary]]
    return returnItems

def SingleTagQuery(tag: str) -> list[Item]:
    return Item.query.filter(or_(col.is_(tag) for col in TagCols)).order_by(Item.ItemOrder).all() # type: ignore

def getAlternateNumbers(input: str) -> List[str]:
    return [input, convert_int_to_roman(input), convert_roman_in_string(input)]

def getTermFilters(term: str, itemType: type[Item] | type[MiscellaneousItem]):
    terms = term.split("&")
    conditions = []
    for user_term in terms:
        user_term = user_term.strip()
    
        filters = or_(*[itemType.ItemHuman.contains(term) for term in getAlternateNumbers(user_term)])
        filters += or_(*[itemType.Notes.contains(term) for term in getAlternateNumbers(user_term)])
        conditions.append(filters)
    return conditions

def verifyCrate(form):
    if form["CrateName"] == "":
        return False
    if form["ReleaseDate"] == "": 
        return False
    if form["CrateTag"] == "":
        return False
    return True

def currentItemsByCrate():
    crates = Crate.query.order_by(Crate.id).all()
    items = Item.query.order_by(Item.ItemOrder).all()
    itemsByCrate = defaultdict(list)
    for item in items:
        itemsByCrate[int(item.CrateID)].append(item)
    return {
        crate.CrateName: itemsByCrate[int(crate.id)]
        for crate in crates
    }

def currentCrateData():
    crates = Crate.query.order_by(desc(Crate.id))
    formattedCrates = {}
    for crate in crates.all():
        formattedCrates[crate.id] = {
            "CrateName" : crate.CrateName,
            "ReleaseDate" : crate.ReleaseDate,
            "URLTag" : crate.URLTag,
            "CrateType" : crate.CrateType
        }
    if formattedCrates:
        return formattedCrates
    return None
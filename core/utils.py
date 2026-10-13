import re
from random import choice
from string import digits, ascii_lowercase
import importlib
import pkgutil
from core.permissions import RegisteredPermissions

def register_modules(app, package):
    for module_info in pkgutil.iter_modules(
        package.__path__,
        prefix=f"{package.__name__}."
    ):
        if not module_info.ispkg:
            continue

        module = importlib.import_module(module_info.name)

        # Register blueprint
        bp = getattr(module, "bp", None)

        if bp is not None:
            app.register_blueprint(bp)

            # Register permissions
            module_permissions = getattr(
                module,
                "RegisteredPermissions",
                None
            )

            if module_permissions:
                RegisteredPermissions[bp.name] = module_permissions





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
    
    return re.sub(pattern, replacer, text)

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

def intParser(numDict):
    newItems = {}
    for key, value in numDict.items():
        newItems[int(key)] = int(value)
    return newItems





def randomCode(length: int) -> str:
    return ''.join(choice(digits + ascii_lowercase) for _ in range(length))
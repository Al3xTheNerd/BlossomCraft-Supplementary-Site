from typing import List, Dict
# The name of the server
server_name: str = "BlossomCraft"
# What do items get called on this server
server_item_name: str = "Blossom Items"
# What rarities exist on this server
server_rarity_list: List[str] = ["Rare", "Legendary", "Mythic", "Immortal", "Exotic"]
server_folder_name = "BlossomCraft"
# A tag to include on pages where tracking is enabled
server_tracker_script: str = '<script data-goatcounter="https://blossomcraft.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
# Maximum limit for how many items can be rolled at once on the gambling page
gambleLimit: int = 10000
# Tags to be used by the site for sorting items
tags: Dict[str, List[str]] = {
    "Armor" : [
        "Hat",
        "Helmet",
        "Chestplate",
        "Leggings",
        "Boots",
        "Elytra"
    ],
    "Tools" : [
        "Pickaxe",
        "Axe",
        "Hoe",
        "Shovel",
        "Rod",
        "Shield",
        "Shears"
    ],
    "Weapons" : [
        "Crossbow",
        "Sword",
        "Axe",
        "Bow",
        "Trident",
        "Mace",
        "Spear"
    ],
    "Tool Features" : [
        "Treefeller",
        "Veinminer",
        "Axe Projectile",
        "Radius Breaking",
        "Block Counter",
        "Auto Replant"
    ],
    "Weapon Features" : [
        "Bleed",
        "Head Dropping",
        "Egg Dropping",
        "Mob Capturing",
        "Kill Counter"
    ],
    "Item Placement" : [
        "Offhand",
        "Hotbar",
        "Inventory"
    ],
    "Block Features" : [
        "Infinite",
        "Special Block",
        "Cooker",
        "Teleportation"
    ],
    "Quest Related" : [
        "Quest",
        "Quest Only"
    ],
    "Miscellaneous" : [
        "Disguise",
        "Repeat Appearance",
        "Unbreakable Kit",
        "Telekinesis",
        "Speed Attribute",
        "Custom Loot",
        "Furniture Dropping",
        "Reach Distance",
        "Pets"
    ]
}
# This auto generates a flat list of the tags, to be used in places such as advanced search as well as when adding new items
validTags: List[str] = []
for category, tagList in tags.items():
    for tag in tagList:
        if tag not in validTags:
            validTags.append(tag)
# How to sort the various Miscellaneous Groups
validMiscGroupTypes: List[str] = [
    "Voucher",
    "Event",
    "Furniture",
    "Crate Based Vouchers"
]
# What types of sets should be allowed to exist
validSetTypes: List[str] = [
    "Armor Set",
    "Upgrade"
]
# What blocks and tools should be used for the Break Speed Calculator?
# Block name can be whatever you like, and then the float value is the block hardness
# https://minecraft.wiki/w/Module:Hardness_values
blocksForBreakSpeedCalculator: Dict[str, Dict[str, float]] = {
    "Pickaxe" : {
        "Netherrack/Nylium" : 0.4,
        "Ice/Packed Ice" : 0.5,
        "Block of Quartz" : 0.8,
        "Sandstone/Red Sandstone" : 0.8,
        "Terracotta" : 1.25,
        "Basalt" : 1.25,
        "Glazed Terracotta" : 1.4,
        "Stone/Diorite/Andesite/Granite/Tuff" : 1.5,
        "Concrete" : 1.8,
        "Cobblestone" : 2.0,
        "Blue Ice" : 2.8,
        "Gold/Lapis/Copper Blocks" : 3.0,
        "Coal/Copper/Diamond/Emerald/Gold/Iron/Lapis/Redstone Ore Blocks" : 3,
        "Endstone" : 3,
        "Nether Quartz/Nether Gold Ore Blocks" : 3.0,
        "Blast Furnace" : 3.5,
        "Cobbled Deepslate" : 3.5,
        "Deepslate Coal/Copper/Diamond/Emerald/Gold/Iron/Lapis/Redstone Ore Blocks" : 4.5,
        "Coal/Diamond/Emerald/Iron/Redstone Blocks" : 5.0,
        "Raw Gold/Raw Copper/Raw Iron Blocks" : 5.0,
        "Ender Chest" : 22.5,
        "Ancient Debris" : 30.0,
        "Obsidian/Crying Obsidian/Block of Netherite" : 50.0
    },
    "Axe" : {
        "Mushroom Block" : 0.2,
        "Bee Nest" : 0.3,
        "Mangrove Roots" : 0.7,
        "Bamboo/Pumpkin/Melon" : 1.0,
        "Logs/Planks" : 2.0,
        "Chest" : 2.5
    },
    "Hoe" : {
        "Moss Blocks" : 0.1,
        "Leaves/Sculk" : 0.2,
        "Hay Bale" : 0.5,
        "Sponge" : 0.6,
        "Nether/Warped Wart Block/Shroomlight" : 1.0,
        "Sculk Sensor" : 1.5,
        "Sculk Catalyst/Sculk Shrieker" : 3.0
    },
    "Shovel" : {
        "Snow Block" : 0.2,
        "Coarse Dirt/Dirt/Mud/Podzol" : 0.5,
        "Concrete Powder" : 0.5,
        "Sand/Red Sand" : 0.5,
        "Soul Sand/Soul Soil" : 0.5,
        "Clay/Farmland/Grass Block/Gravel/Mycelium" : 0.6 
    },
    "Shears" : {
        "Leaves/Vines" : 0.2,
        "Wool" : 0.8,
        "Cobweb" : 4.0
    }
}
# Not really a secret, but used to calculate XP gain speed for jobs
JobsSecrets: Dict[str, int] = {
    "Miner" : 5,
    "Smither" : 5,
    "Digger" : 4,
    "Hunter" : 3,
    "Woodcutter" : 3,
    "Fisher" : 3,
    "Florist" : 3,
    "Rancher" : 2,
    "Farmer" : 2
}
# Jobs Information
jobsInfo: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {
    "Miner": {
        "Break": {
            "Stone": {
                "xp": 0.05,
                "basepay": 0.05
            },
            "Andesite": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Granite": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Diorite": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Deepslate": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Tuff": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Calcite": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Sandstone": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Red Sandstone": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Mossy Cobblestone": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Amethyst Block": {
                "xp": 1.00,
                "basepay": 1.00
            },
            "Coal Ore": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Deepslate Coal Ore": {
                "xp": 0.30,
                "basepay": 0.33
            },
            "Iron Ore": {
                "xp": 1.00,
                "basepay": 1.00
            },
            "Deepslate Iron Ore": {
                "xp": 1.10,
                "basepay": 1.10
            },
            "Copper Ore": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Deepslate Copper Ore": {
                "xp": 0.90,
                "basepay": 0.90
            },
            "Redstone Ore": {
                "xp": 2.00,
                "basepay": 2.00
            },
            "Deepslate Redstone Ore": {
                "xp": 2.20,
                "basepay": 2.20
            },
            "Gold Ore": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Deepslate Gold Ore": {
                "xp": 6.60,
                "basepay": 6.60
            },
            "Lapis Lazuli Ore": {
                "xp": 11.00,
                "basepay": 11.00
            },
            "Deepslate Lapis Ore": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Diamond Ore": {
                "xp": 15.00,
                "basepay": 15.00
            },
            "Deepslate Diamond Ore": {
                "xp": 16.50,
                "basepay": 16.50
            },
            "Dripstone Block": {
                "xp": 0.12,
                "basepay": 0.12
            },
            "Pointed Dripstone": {
                "xp": 0.12,
                "basepay": 0.12
            },
            "Netherrack": {
                "xp": 0.01,
                "basepay": 0.01
            },
            "Magma Block": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Basalt": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Blackstone": {
                "xp": 0.12,
                "basepay": 0.12
            },
            "Nether Gold Ore": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Emerald Ore": {
                "xp": 100.00,
                "basepay": 100.00
            },
            "Deepslate Emerald Ore": {
                "xp": 110.00,
                "basepay": 110.00
            },
            "Nether Quartz Ore": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Obsidian": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Crying Obsidian": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Gilded Blackstone": {
                "xp": 5.00,
                "basepay": 5.00
            },
            "Endstone": {
                "xp": 0.05,
                "basepay": 0.05
            },
            "Terracotta": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Red Terracotta": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Orange Terracotta": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Yellow Terracotta": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Brown Terracotta": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "White Terracotta": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Light Gray Terracotta": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Ice": {
                "xp": 0.15,
                "basepay": 0.15
            },
            "Packed Ice": {
                "xp": 0.15,
                "basepay": 0.15
            },
            "Blue Ice": {
                "xp": 0.15,
                "basepay": 0.15
            }
        }
    },
    "Digger": {
        "Break": {
            "Dirt": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Grass Block": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Sand": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Soul Sand": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Soul Soil": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Gravel": {
                "xp": 0.15,
                "basepay": 0.15
            },
            "Snow Block": {
                "xp": 0.15,
                "basepay": 0.15
            },
            "Red Sand": {
                "xp": 0.13,
                "basepay": 0.13
            },
            "Coarse Dirt": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Podzol": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Rooted Dirt": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Mud": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Muddy Mangrove Roots": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Mycelium": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Clay": {
                "xp": 0.25,
                "basepay": 0.25
            }
        }
    },
    "Farmer": {
        "Break": {
            "Wheat": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Beetroots": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Carrots": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Potatoes": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Cocoa": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Pumpkin": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Melon Block": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Sugar Canes": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Cactus": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Nether Wart": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Chorus Plant": {
                "xp": 0.15,
                "basepay": 0.15
            },
            "Mushroom Stem": {
                "xp": 0.22,
                "basepay": 0.22
            },
            "Red Mushroom Block": {
                "xp": 0.22,
                "basepay": 0.22
            },
            "Brown Mushroom Block": {
                "xp": 0.22,
                "basepay": 0.22
            },
            "Chorus Flower": {
                "xp": 1.00,
                "basepay": 1.00
            }
        },
        "Collect": {
            "Sweet Berries": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Bone Meal": {
                "xp": 0.15,
                "basepay": 0.15
            }
        }
    },
    "Fisher": {
        "Fish": {
            "Raw Cod": {
                "xp": 15.00,
                "basepay": 15.00
            },
            "Raw Salmon": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Pufferfish": {
                "xp": 35.00,
                "basepay": 35.00
            },
            "Tropical Fish": {
                "xp": 60.00,
                "basepay": 60.00
            },
            "Bow": {
                "xp": 35.00,
                "basepay": 35.00
            },
            "Enchanted Book": {
                "xp": 35.00,
                "basepay": 35.00
            },
            "Fishing Rod": {
                "xp": 35.00,
                "basepay": 35.00
            },
            "Name Tag": {
                "xp": 35.00,
                "basepay": 35.00
            },
            "Saddle": {
                "xp": 35.00,
                "basepay": 35.00
            },
            "Nautilus Shell": {
                "xp": 60.00,
                "basepay": 60.00
            }
        }
    },
    "Florist": {
        "Break": {
            "Grass": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Short Dry Grass": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Tall Grass": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Tall Dry Grass": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Fern": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Large Fern": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Leaf Litter": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Lily Pad": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Poppy": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Dandelion": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Red Tulip": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Orange Tulip": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "White Tulip": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Pink Tulip": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Pink Petals": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Azure Bluet": {
                "xp": 0.50,
                "basepay": 0.50
            },
            "Oxeye Daisy": {
                "xp": 0.50,
                "basepay": 0.50
            },
            "Cornflower": {
                "xp": 0.50,
                "basepay": 0.50
            },
            "Allium": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Lily of the Valley": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Peony": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Rose Bush": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Sunflower": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Blue Orchid": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Closed Eyeblossom": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Open Eyeblossom": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Cactus Flower": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Firefly Bush": {
                "xp": 0.70,
                "basepay": 0.70
            },
            "Azalea": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Flowering Azalea": {
                "xp": 1.00,
                "basepay": 1.00
            },
            "Azalea Leaves": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Flowering Azalea Leaves": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Mangrove Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Acacia Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Birch Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Oak Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Spruce Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Jungle Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Dark Oak Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Cherry Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Pale Oak Leaves": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Small Dripleaf": {
                "xp": 3.00,
                "basepay": 3.00
            },
            "Big Dripleaf": {
                "xp": 0.50,
                "basepay": 0.50
            },
            "Spore Blossom": {
                "xp": 5.00,
                "basepay": 5.00
            },
            "Mangrove Roots": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Moss Block": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Pale Moss Block": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Moss Carpet": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Pale Moss Carpet": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Wildflowers": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Shroomlight": {
                "xp": 1.00,
                "basepay": 1.00
            },
            "Brown Mushroom": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Red Mushroom": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Bush": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Dead Bush": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Vines": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Hanging Roots": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Weeping Vines Plant": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Twisting Vines Plant": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Crimson Roots": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Crimson Fungus": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Nether Wart Block": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Warped roots": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Warped Fungus": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Warped Wart block": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Seagrass": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Sea Pickle": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Kelp": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Tube Coral": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Tube Coral Fan": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Brain Coral": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Brain Coral Fan": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Bubble Coral": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Bubble Coral Fan": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Fire Coral": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Fire Coral Fan": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Horn Coral": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Horn Coral Fan": {
                "xp": 0.30,
                "basepay": 0.30
            }
        }
    },
    "Hunter": {
        "Kill": {
            "Chicken": {
                "xp": 2.00,
                "basepay": 2.00
            },
            "Cow": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Mooshroom": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Pig": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Sheep": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Wolf": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Frog": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Tadpole": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Goat": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Fox": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Llama": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Bat": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Cod": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Salmon": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Pufferfish": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Tropical Fish": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Squid": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Glow Squid": {
                "xp": 6.00,
                "basepay": 6.00
            },
            "Rabbit": {
                "xp": 7.77,
                "basepay": 7.77
            },
            "Villager": {
                "xp": 8.00,
                "basepay": 8.00
            },
            "Bee": {
                "xp": 8.00,
                "basepay": 8.00
            },
            "Armadillo": {
                "xp": 10.00,
                "basepay": 10.00
            },
            "Panda": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Turtle": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Polar Bear": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Horse": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Donkey": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Mule": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Skeleton Horse": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Axolotl": {
                "xp": 12.00,
                "basepay": 12.00
            },
            "Dolphin": {
                "xp": 16.00,
                "basepay": 16.00
            },
            "Zombie": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Skeleton": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Spider": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Creeper": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Drowned": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Husk": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Stray": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Strider": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Camel": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Enderman": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Endermite": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Witch": {
                "xp": 8.00,
                "basepay": 8.00
            },
            "Guardian": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Shulker": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Hoglin": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Piglin": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Piglin Brute": {
                "xp": 2.00,
                "basepay": 2.00
            },
            "Zombified Piglin": {
                "xp": 2.00,
                "basepay": 2.00
            },
            "Zoglin": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Blaze": {
                "xp": 3.00,
                "basepay": 3.00
            },
            "Ghast": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Wither Skeleton": {
                "xp": 4.00,
                "basepay": 4.00
            },
            "Wither": {
                "xp": 30.00,
                "basepay": 30.00
            },
            "Elder Guardian": {
                "xp": 15.00,
                "basepay": 15.00
            },
            "Warden": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Ender Dragon": {
                "xp": 100.00,
                "basepay": 100.00
            }
        }
    },
    "Rancher": {
        "Breed": {
            "Cow": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Mooshroom": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Pig": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Sheep": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Wolf": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Llama": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Panda": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Goat": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Rabbit": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Fox": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Armadillo": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Strider": {
                "xp": 13.00,
                "basepay": 13.00
            },
            "Horse": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Donkey": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Camel": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Axolotl": {
                "xp": 20.00,
                "basepay": 20.00
            }
        },
        "Tame": {
            "Parrot": {
                "xp": 8.00,
                "basepay": 8.00
            },
            "Wolf": {
                "xp": 10.00,
                "basepay": 10.00
            },
            "Ocelot": {
                "xp": 20.00,
                "basepay": 20.00
            },
            "Horse": {
                "xp": 30.00,
                "basepay": 30.00
            },
            "Donkey": {
                "xp": 30.00,
                "basepay": 30.00
            },
            "Mule": {
                "xp": 30.00,
                "basepay": 30.00
            },
            "Llama": {
                "xp": 30.00,
                "basepay": 30.00
            }
        },
        "Shear": {
            "Red": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Orange": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Yellow": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Green": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Blue": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Light Blue": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Magenta": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Pink": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "White": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Light Gray": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Black": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Brown": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Purple": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Cyan": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Gray": {
                "xp": 0.80,
                "basepay": 0.80
            },
            "Lime": {
                "xp": 0.80,
                "basepay": 0.80
            }
        },
        "Milk": {
            "Cow": {
                "xp": 0.30,
                "basepay": 0.30
            }
        },
        "Collect": {
            "honey Bottle": {
                "xp": 1.50,
                "basepay": 1.50
            },
            "Honeycomb": {
                "xp": 1.50,
                "basepay": 1.50
            }
        }
    },
    "Smither": {
        "Smelt": {
            "Stone": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Smooth Stone": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Glass": {
                "xp": 0.10,
                "basepay": 0.10
            },
            "Copper Ingot": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Iron Ingot": {
                "xp": 0.36,
                "basepay": 0.36
            },
            "Gold Ingot": {
                "xp": 1.80,
                "basepay": 1.80
            },
            "Netherite Scrap": {
                "xp": 75.00,
                "basepay": 75.00
            },
            "Smooth Sandstone": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Smooth Red Sandstone": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Smooth Quartz": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Brick": {
                "xp": 0.12,
                "basepay": 0.12
            },
            "Nether Brick": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Smooth Basalt": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Cracked Polished Blackstone Bricks": {
                "xp": 0.35,
                "basepay": 0.35
            },
            "Deepslate": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Cracked Deepslate Bricks": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Cracked Deepslate Tiles": {
                "xp": 0.06,
                "basepay": 0.06
            },
            "Charcoal": {
                "xp": 0.08,
                "basepay": 0.08
            },
            "Sponge": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Resin Brick": {
                "xp": 0.15,
                "basepay": 0.15
            },
            "Baked Potato": {
                "xp": 0.05,
                "basepay": 0.05
            },
            "Steak": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Cooked Chicken": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Cooked Mutton": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Cooked Porkchop": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Cooked Rabbit": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Cooked Fish": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Cooked Salmon": {
                "xp": 0.07,
                "basepay": 0.07
            },
            "Popped Chorus Fruit": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "White Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Orange Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Magenta Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Light Blue Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Yellow Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Lime Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Pink Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Light Gray Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Gray Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Cyan Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Purple Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Blue Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Brown Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Green Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Red Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            },
            "Black Glazed Terracotta": {
                "xp": 0.18,
                "basepay": 0.18
            }
        }
    },
    "Woodcutter": {
        "Break": {
            "Bamboo": {
                "xp": 0.20,
                "basepay": 0.20
            },
            "Jungle Log": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Dark Oak Log": {
                "xp": 0.25,
                "basepay": 0.25
            },
            "Oak Log": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Spruce Log": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Birch Log": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Crimson Stem": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Warped Stem": {
                "xp": 0.30,
                "basepay": 0.30
            },
            "Acacia Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Cherry Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Mangrove Log": {
                "xp": 0.50,
                "basepay": 0.50
            },
            "Pale Oak Log": {
                "xp": 0.50,
                "basepay": 0.50
            }
        },
        "Strip-Logs": {
            "Stripped Jungle Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Dark Oak Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Oak Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Spruce Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Birch Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Acacia Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Cherry Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Mangrove Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Pale Oak Log": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Crimson Stem": {
                "xp": 0.40,
                "basepay": 0.40
            },
            "Stripped Warped Stem": {
                "xp": 0.40,
                "basepay": 0.40
            }
        }
    }
}

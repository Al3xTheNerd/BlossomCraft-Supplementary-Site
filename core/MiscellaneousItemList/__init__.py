from flask import Blueprint

bp = Blueprint(
    "MiscellaneousItemList",
    __name__,
    url_prefix="/miscitems",
    template_folder="templates"
)

RegisteredPermissions = [
    ("view_misc_item_list", "View the Misc. Item List"),
    ("delete_misc_item", "Delete a Misc. Item"),
    ("view_edit_misc_item", "View the <code>Edit Misc. Item</code> Page"),
    ("edit_misc_item_notes", "Edit a Misc. Item's Notes"),
    ("edit_misc_item_group", "Edit a Misc. Item's Group"),
    ("edit_misc_item_item_name", "Edit a Misc. Item's Item Name"),
    ("edit_misc_item_image", "Change the Icon image of a Misc. Item"),
    None,
    ("view_manage_misc_groups", "View the <code>Manage Misc. Groups</code> Page"),
    ("edit_misc_group_existing", "Edit an already existing Misc. Group"),
    ("create_misc_group", "Create a new Misc. Group"),
    ("delete_misc_group", "Delete a Misc. Group"),
    None,
    ("view_add_misc_item", "View and use the <code>Add Misc. Items</code> Page"),
    None,
    ("view_reorder_misc_items", "View and use the <code>Manage Misc. Item Order</code> Page"),
    None,
    ("view_reorder_misc_groups", "View and use the <code>Manage Misc. Item Order</code> Page"),
    None,
    ("view_misc_missing_images", "View and use the <code>Missing Misc. Images</code> Page"),

]

from core.MiscellaneousItemList import routes
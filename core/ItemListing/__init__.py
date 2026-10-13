from flask import Blueprint

bp = Blueprint(
    "ItemListing",
    __name__,
    url_prefix="/items",
    template_folder="templates"
)
RegisteredPermissions = [
    ("view_item_list", "View the Item List"),
    ("delete_item", "Delete an Item"),
    ("view_edit_item", "View the <code>Edit Item</code> Page"),
    ("edit_item_notes", "Edit an Item's Notes"),
    ("edit_item_tags", "Change the Tags of an Item"),
    ("edit_item_crate", "Edit an Item's Crate"),
    ("edit_item_grouped_items", "Edit an Item's Linked Miscellaneous Items"),
    ("edit_item_item_name", "Edit an Item's Item Name"),
    ("edit_item_win_percentage", "Edit an Item's Win Percentage"),
    ("edit_item_image", "Change the Icon image of an Item"),
    None,
    ("view_manage_crate", "View the <code>Manage Crates</code> Page"),
    ("edit_crate_existing", "Edit an already existing Crate"),
    ("create_crate", "Create a new Crate"),
    ("delete_crate", "Delete a Crate"),
    None,
    ("view_add_item", "View and use the <code>Add Items</code> Page"),
    None,
    ("view_reorder_items", "View and use the <code>Manage Item Order</code> Page"),
    None,
    ("view_missing_images", "View and use the <code>Missing Images</code> Page"),
    None,
    ("view_set_management", "View the <code>Set Management</code> page"),
    ("edit_set_order", "Update the order Sets appear in"),
    ("edit_set", "Edit a set"),
    ("delete_set", "Delete a set"),
    ("create_new_set", "Create a new Set"),
]

from core.ItemListing import routes
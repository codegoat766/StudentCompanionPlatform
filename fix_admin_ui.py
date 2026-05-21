import xml.etree.ElementTree as ET

ui_file = 'c:/workspace/stdcomp/Student-performance-analyzer-spa_db-/ui/admin.ui'
tree = ET.parse(ui_file)
root = tree.getroot()

# Find mainLayout
centralwidget = root.find(".//widget[@name='centralwidget']")
mainLayout = centralwidget.find(".//layout[@name='mainLayout']")

# mainLayout currently has headerFrame and an item containing the horizontal layout
# We want:
# mainLayout (QHBoxLayout)
#   - leftPanel
#   - rightContainer (QVBoxLayout)
#       - headerFrame
#       - contentStack

# Find elements
header_item = None
hlayout_item = None

for item in mainLayout.findall("item"):
    widget = item.find("widget")
    if widget is not None and widget.get("name") == "headerFrame":
        header_item = item
    layout = item.find("layout")
    if layout is not None:
        hlayout_item = item

if header_item and hlayout_item:
    hlayout = hlayout_item.find("layout")
    left_panel_item = hlayout.findall("item")[0]
    content_stack_item = hlayout.findall("item")[1]
    
    # Change mainLayout to QHBoxLayout
    mainLayout.set("class", "QHBoxLayout")
    
    # Clear mainLayout
    for item in mainLayout.findall("item"):
        mainLayout.remove(item)
        
    # Add leftPanel to mainLayout
    mainLayout.append(left_panel_item)
    
    # Create rightContainer QVBoxLayout
    right_item = ET.Element("item")
    right_layout = ET.SubElement(right_item, "layout", {"class": "QVBoxLayout", "name": "rightLayout"})
    right_layout.append(header_item)
    right_layout.append(content_stack_item)
    
    mainLayout.append(right_item)

# Remove the three buttons from leftLayout
leftLayout = tree.find(".//layout[@name='leftLayout']")
items_to_remove = []
for item in leftLayout.findall("item"):
    widget = item.find("widget")
    if widget is not None and widget.get("name") in ["createUserButton", "addSubjectButton", "toggleUserButton"]:
        items_to_remove.append(item)

for item in items_to_remove:
    leftLayout.remove(item)

tree.write(ui_file, encoding='utf-8', xml_declaration=True)
print("admin.ui updated successfully.")

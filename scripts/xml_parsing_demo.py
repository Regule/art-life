import xml.etree.ElementTree as ET

# Parsing an XML file
tree = ET.parse('config/xml_demo.xml')
root = tree.getroot()

# Accessing elements and attributes
print("Root tag:", root.tag)

# Iterating over child elements
for child in root:
    print("Child tag:", child.tag, "Child text:", child.text)

# Accessing specific elements
element1 = root.find('element1')
print("Element 1 text:", element1.text)

# Modifying element attributes
element2 = root.find('element2')
element2.set('attribute', 'new_value')
tree.write('example_modified.xml')  # Saving modified XML to a new file

# Creating new elements
new_element = ET.Element('new_element')
new_element.text = 'New element content'
root.append(new_element)

# Adding sub-elements with attributes
sub_element = ET.SubElement(new_element, 'sub_element')
sub_element.set('attribute', 'value')

# Removing elements
root.remove(element1)

# Generating XML from the modified tree
xml_string = ET.tostring(root, encoding='utf-8')
print(xml_string)

# Write modified tree to a file
# tree.write('example_modified.xml')


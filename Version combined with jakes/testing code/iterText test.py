import xml.etree.ElementTree as ET
##tree = ET.parse('DATA\\rooms.xml')
##root = tree.getroot()
###print(root[0][0][2].itertext())
##print(root.itertext())


##text = open('DATA\\rooms.xml').read()
##a = ''.join(ET.fromstring(text).itertext())
##print(a)

doc = ET.parse('DATA\\rooms.xml')
root = doc.getroot()
node = root[0][0].find('furnishings')
objects = []
print(node)
for elem in node:
    objects.append(elem.text)
print(objects)

#furnishings = [elem.text for elem in root[0][0].find('objects')]
furnishings = [elem.text for elem in root[0][0][2]]
print(furnishings)



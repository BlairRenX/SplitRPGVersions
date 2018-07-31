import xml.etree.ElementTree as ET
roomTree = ET.parse('DATA\\rooms.xml')
roomRoot = roomTree.getroot()
print(roomRoot.tag)
print(roomRoot.attrib)
for child in roomRoot:
    print(child.attrib["name"])
    for subchild in child:
        print(subchild.tag, subchild.attrib)
        print(subchild.text)

print("\n \n \n")

doorTree = ET.parse('DATA\\doors.xml')
doorRoot = doorTree.getroot()
for doorChild in doorRoot:
        for roomChild in roomRoot:
            print(str(doorChild[0].text), str(doorChild[1].text))
            print(str(roomChild.attrib["name"]))
            if str(doorChild[0].text) == str(roomChild.attrib["name"]) or str(doorChild[1].text) == str(roomChild.attrib["name"]):
                print("bepis")
                door = ET.SubElement(roomChild[1], "door")
                door.set("name", doorChild.attrib["name"])

roomTree.write('rooms.xml')


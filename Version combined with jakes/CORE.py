##import xml.etree.ElementTree as ET
##charTree = ET.parse('DATA\\characters.xml')
##charRoot = charTree.getroot()
##
##for child in charRoot:
##    print(charRoot[0][0].text)


##import sys
##sys.path.insert(0, 'CLASSES')
##
##import tkinter as tk
##
##main = tk.Tk()
##
##import UI_HUB
##
##ui = UI_HUB.UI(main)
##
##import charClass
##
##Scavenger = charClass.playerCharacter("Scavenger", "R1")
##Scavenger.whatsMine()

import sys
import random
import tkinter as tk
import UI_HUB
import xml.etree.ElementTree as ET
#from SPINE import *
sys.path.insert(0, 'CLASSES')
main = tk.Tk()
ui = UI_HUB.UI(main)
import charClass, placeClass, doorClass, invFurnClass

location = "miningPlatform01"





rooms = []
roomTree = ET.parse('DATA\\rooms.xml')
roomRoot = roomTree.getroot()
for child in roomRoot:
    if child.attrib["name"] == location:
        for subchild in child:
            currentPlace = placeClass.Place(subchild.attrib["name"], int(subchild[0].text), [elem.text for elem in subchild[1]], [elem.text for elem in subchild[2]], [elem.text for elem in subchild[3]],
                                          subchild[4].text, subchild[5].text)
            rooms.append(currentPlace)
            
            
            
#currentDoors = []
doorTree = ET.parse('DATA\\doors.xml')
doorRoot = doorTree.getroot()
checkVal = False #cuz if it creates an invalid door, I don't want to stuff to mess up, so if it's invalid it gets deleted

for child in doorRoot:
    if child.attrib["name"] == location:
        for subchild in child:
            temp = doorClass.Door(subchild.attrib["name"], subchild[0].text, subchild[1].text, int(subchild[2].text),
                                  [eval(subchild[3][0].text),subchild[3][1].text,subchild[3][2].text], [eval(subchild[4][0].text), subchild[4][1].text],
                                  eval(subchild[5].text), eval(subchild[6].text), subchild[7].text, eval(subchild[8].text))
            temp.hidden = False
            #print(temp.blocked)
            
            for room in rooms:
                if room.name in subchild.attrib["name"]:
                    if room.name == subchild[0].text:
                        temp.room1 = room
                    elif room.name == subchild[1].text:
                        temp.room2 = room
                    #establishes door connection
                        
                    room.doors.append(temp)
                    
                    checkVal = True
                    
            if checkVal == False:
                print("deleting door")
                del temp
#setting up doors. the deletion part helps to prevent the creation of invalid doors.



furnTree = ET.parse('DATA\\roomFurnishings.xml')
furnRoot = furnTree.getroot()
vitalFurns = {}
furnishingList = []
for room in rooms:
    for furn in room.furnishings:
        if furn is not None:
            vitalFurns[furn] = room

for child in furnRoot:
    if child.attrib["name"] in vitalFurns:
        currentRoom = vitalFurns[child.attrib["name"]]
        currentFurn = invFurnClass.roomFurnishing(child[0].text, child[1].text, child[2].text,
                                                                                        [eval(child[3][0].text), [elem.text for elem in child[3][1]]], [elem.text for elem in child[4]],
                                                                                        [eval(child[5][0].text), eval(child[5][1].text)], [eval(child[6][0].text),
                                                                                        [elem.text for elem in child[6][1]]],
                                                                                        [eval(child[7][0].text), child[7][1].text],
                                                                                        [eval(child[8][0].text), child[8][1].text, eval(child[8][2].text)])
       
        
        currentRoom.furnishings.append(currentFurn)
      
        vitalFurns[child.attrib["name"]].furnishings.remove(child.attrib["name"])
                                                         #note: currently does not access 'hidden'. I could change that later.
#setting up furnishings.

for room in rooms:
    if not room.furnishings == []:
        for furnishing in room.furnishings:
            furnishingList.append(furnishing)
            furnishing.loaction = room
#setting up the furnishing list since it's needed for items inside furnishings

npcTree = ET.parse('DATA\\NPCs.xml')
npcRoot = npcTree.getroot()
vitalNPCs = {} #note: this doesn't mean unkillable, it means 'the ones needed in the map'.
for room in rooms:
    if len(room.characters) > 0:
        for obj in room.characters:
            vitalNPCs[obj] = room
            

for child in npcRoot:
    if child.attrib["name"] in vitalNPCs:
        #dialogue will be in the form <element topic=""> [dialogue] </element> hence the array formatting.
        currentRoom = vitalInv[child.attrib["name"]]
        currentNPC = charClass.nonPlayerCharacter(child[0].text, child[1].text, child[2].text, child[3].text, eval(child[4].text),
                                                                                    [elem.text for elem in child[5]], [elem.text for elem in child[6]],
                                                                                    [elem.text for elem in child[7]], [elem.text for elem in child[8]],
                                                                                    [elem.text for elem in child[9]], [eval(child[10][0].text), child[10][1].text],
                                                                                    eval(child[11].text))
        currentRoom.characters.append(CurrentNPC)
        currentNPC.location = currentRoom
        
        vitalNPCs[child.attrib["name"]].objects.remove(child.attrib["name"])
#setting up NPCs. anything that has inventory objects should be set up before the inventory objects themselves.
        
npcList = []
for room in rooms:
    if not room.characters == []:
        for npc in room.characters:
            npcList.append(npc)
            npc.location = room
#same issue as furnishings.

            

invTree = ET.parse('DATA\\inventoryObjects.xml')
invRoot = invTree.getroot()
vitalInv = {}
for room in rooms:
    if len(room.objects) > 0:
        for obj in room.objects:
            vitalInv[obj] = room

for child in invRoot:
    if child.attrib["name"] in vitalInv:
        currentRoom = vitalInv[child.attrib["name"]]
        currentObj = invFurnClass.inventoryObject(child.attrib["name"], child[0].text, child[1].text, [eval(child[2][0].text), child[2][1].text],
                                                                                   [eval(child[3][0].text), child[3][1].text], eval(child[4].text),
                                                                                   [eval(child[5][0].text), [elem.text for elem in child[5][1]]], eval(child[6].text),
                                                                                   [eval(child[7][0].text), child[7][1].text], [child[8][0].text, child[8][1].text])
        currentRoom.objects.append(currentObj)
        currentObj.location = currentRoom
        
        vitalInv[child.attrib["name"]].objects.remove(child.attrib["name"])
#setting up inventory objects in rooms

vitalInv = {}
for furn in furnishingList:
    if len(furn.containedObjects) > 0:
        for obj in furn.containedObjects:
            vitalInv[obj] = furn

for child in invRoot:
    if child.attrib["name"] in vitalInv:
        currentFurn = vitalInv[child.attrib["name"]]
        currentObj = invFurnClass.inventoryObject(child.attrib["name"], child[0].text, child[1].text, [eval(child[2][0].text), child[2][1].text],
                                                                                   [eval(child[3][0].text), child[3][1].text], eval(child[4].text),
                                                                                   [eval(child[5][0].text), [elem.text for elem in child[5][1]]], eval(child[6].text),
                                                                                   [eval(child[7][0].text), child[7][1].text], [child[8][0].text, child[8][1].text])
        currentFurn.objects.append(currentObj)
        currentObj.location = currentFurn
        
        vitalInv[child.attrib["name"]].objects.remove(child.attrib["name"])
#setting up inventory objects inside furnishings

vitalInv = {}
for npc in npcList:
    if len(npc.inventory) > 0:
        for item in npc.inventory:
            vitalInv[item] = npc
            
for child in invRoot:
    if child.attrib["name"] in vitalInv:
        currentNPC = vitalInv[child.attrib["name"]]
        currentObj = invFurnClass.inventoryObject(child.attrib["name"], child[0].text, child[1].text, [eval(child[2][0].text), child[2][1].text],
                                                                                   [eval(child[3][0].text), child[3][1].text], eval(child[4].text),
                                                                                   [eval(child[5][0].text), [elem.text for elem in child[5][1]]], eval(child[6].text),
                                                                                   [eval(child[7][0].text), child[7][1].text], [child[8][0].text, child[8][1].text])
        currentNPC.objects.append(currentObj)
        currentObj.location = currentNPC
        
        vitalInv[child.attrib["name"]].objects.remove(child.attrib["name"])
#setting up npc inventories



for room in rooms:
    print("objects")
    print(room.objects)

for room in rooms:
    if not isinstance(room,placeClass.Place):
        exec("JakeError: Yo, There are some file reading problem here, %s doesn't look like an Place referance"%item)
    for item in room.objects:
        if not isinstance(item,invFurnClass.inventoryObject):
            exec("JakeError: Yo, There are some file reading problem here, %s doesn't look like an invObj referance"%item)
    for item in room.furnishings:
        if not isinstance(item,invFurnClass.roomFurnishing):
            exec("JakeError: Yo, There are some file reading problem here, %s doesn't look like an furnishing referance"%item)
    for item in room.characters:
        if not isinstance(item,charClass.nonPlayerCharacter):
            exec("JakeError: Yo, There are some file reading problem here, %s doesn't look like an npc referance"%item)

playerCharacter = charClass.playerCharacter("Scavenger", rooms[0])
playerCharacter.whatsMine()


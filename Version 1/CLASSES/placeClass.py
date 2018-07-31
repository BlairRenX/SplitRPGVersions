import random
class Place(object):
    def __init__(self, name, quality = 3, furnishings = None, objects = None, characters = None,search = "an empty room", investigation = "nothing of note here visually"):
        self.doors = []
        
        if furnishings is None or furnishings == ["None"]:
            furnishings = []

        if objects is None or objects == ["None"]:
            objects = []

        if characters is None or characters == ["None"]:
            characters = []

        self.name = name
        #should be of the format [canBeEntered, Description, leadsTo]
        #and because a room can have multiple doors, it'll be a 2D array
        self.quality = quality
        self.furnishings = furnishings
        self.objects = objects
        self.characters = characters

        self.search = search

        self.investigation = investigation
        #should be of the form [canBeInvestigated, Description, leadsTo]
        #'cept obviously you still get a description if you can't

        #for furnishing in self.furnishings:
            #furnishing.room = self

        #for character in self.characters:
            #character.room = self


    def Populate(self,furnishingList,objectList,characterList):
        
        if furnishingList is not None:
            for item in furnishingList:
                assert isinstance(item, roomFurnishing)
                self.furnishings.append(item)
                item.location = self
                
        if objectList is not None:
            for item in objectList:
                assert isinstance(item, inventoryObject)
                self.objects.append(item)
                item.location = self

        if characterList is not None:
            for item in characterList:
                assert isinstance(item, nonPlayerCharacter)
                self.characters.append(item)
                item.location = self

                

    def EnteredRoom(self): #Called as player enters room - wakes the room up and lets npcs interact with the room       
        for character in self.characters:
            character.Initialise()
        
            
    
    def showAllObjectsAndNames(self):
        from __main__ import playerCharacter
        thingList = [[[],[]],[[],[]],[[],[]],[[],[]]]
    
        for furnishing in self.furnishings:
            if not furnishing.hidden and not furnishing in thingList[0][1]:
                thingList[0][0].append(furnishing.name)
                thingList[0][1].append(furnishing)
        
        for anObject in self.objects:
            
            if not anObject.hidden and anObject not in thingList[1][1]:
                thingList[1][0].append(anObject.name)
                thingList[1][1].append(anObject)

        for character in self.characters:
            if not character.hidden and character not in thingList[2][1]:
                thingList[2][0].append(character.basicDesc)
                thingList[2][1].append(character)

        for door in self.doors:
            if not door.hidden and door not in thingList[3][1]:
                thingList[3][0].append(door.name)
                thingList[3][1].append(door)

        
        invList = [[[],[]]]
        for item in playerCharacter.inventory:
            invList[0][0].append(item.name)
            invList[0][1].append(item)
      
        return thingList,invList
        
            


    def DescribeRoom(self):
            
        roomDescription = ""
        roomDescription += "The room is " + self.search + ". "
        roomDescription += "There is "+self.investigation+".\n"
        randomSense = random.randint(0,3)
        if randomSense == 0:
            roomSight = []
            f = open("senses\\sights1.txt", "r")
            for row in f:
                roomSight.append(row)
            f.close()

            roomDescription += roomSight[self.quality-1]

        elif randomSense == 1:
            roomSound = []
            f = open("senses\\sounds1.txt", "r")
            for row in f:
                roomSound.append(row)
            f.close()

            roomDescription += roomSound[self.quality-1]


        elif randomSense == 2:
            roomFeel = []
            f = open("senses\\feels1.txt", "r")
            for row in f:
                roomFeel.append(row)
            f.close()

            roomDescription += roomFeel[self.quality-1]
            
                 
        else:
            roomSmell = []
            f = open("senses\\smells1.txt", "r")
            for row in f:
                roomSmell.append(row)
            f.close()

            roomDescription += roomSmell[self.quality-1]

            
        
        if len(self.furnishings) > 0:
            roomDescription += "The room is furnished with "
            for furnishing in self.furnishings:
                roomDescription += "a " +furnishing.name + ", "

            roomDescription = roomDescription[:-2] + ". "
                

        if len(self.objects) > 0:
            roomDescription += "In the room, there is "
            for roomObject in self.objects:
                if roomObject.hidden == False:
                    roomDescription += roomObject.basicDesc+", "
            roomDescription = roomDescription[:-2] + ". "

                    
        if len(self.characters) > 0:
            roomDescription += "You are not alone in the room, you can see "
            for character in self.characters:
                if character.hidden == False:
                    roomDescription += character.basicDesc
                    if character.doing[0] != '':
                        roomDescription += ", the %s appears to be %s the %s. "%(character.name,character.doing[0],character.doing[1].name)
                    else:
                        roomDescription+="."

        for door in self.doors:
            if door.hidden == False:
                roomDescription += "There is a door to the " + door.name[:-5] + ". "
        return roomDescription

from __main__ import ui
import invFurnClass
import doorClass

class Character(object):
    def __init__(self, name, startingRoom, inventory, doing = None):

        if doing is None:
            doing = ['',None,False]
            # ['verb' (plain english),object (pointer), IfActivityFullyOccupying (bool)]

        if inventory is None:
            inventory = []

        
            
        self.name = name
        self.inventory = inventory
        self.currentRoom = startingRoom
        self.doing = doing
        #an array of inventory objects
        import invFurnClass
        
        basicShirt = invFurnClass.inventoryObject(name ="basic shirt", basicDesc="A basic synth-cloth shirt", inspectDesc="There's a small rip in the armpit...", equippable=[True,"clothesTorso"])
        basicLegs = invFurnClass.inventoryObject(name= "basic legwear", basicDesc="Some basic synth-cloth legwear", inspectDesc="This could probably do with being washed.", equippable=[True, "clothesLegs"])
        basicShoes = invFurnClass.inventoryObject(name="basic shoes", basicDesc="A pair of basic synthetic fabric and rubber shoes", inspectDesc="You can feel a hole in your sock. Ugh.", equippable=[True, "footwear"])

        self.inventory.append(basicShirt)
        self.inventory.append(basicLegs)
        self.inventory.append(basicShoes)

        #in case we decide to add stats later

        self.equipped = {
            "clothesTorso" : basicShirt,
            "clothesLegs" : basicLegs,
            "armwear" : None,
            "headgear" : None,
            "footwear" : basicShoes,
            "armourTorso" : None,
            "armourLegs" : None,
            "accessories" : [],
            "weaponLeft" : None,
            "weaponRight" : None,
            "weaponBoth" : None
            }
        #this is more for a fantasy setting and it hasn't been tested cuz I wrote it at 00:37

        self.location = None

    def getName(self):
        return self.name

    def whatsMine(self):
        for item in self.equipped:
            if self.equipped[item] == None or self.equipped[item] == []:
                pass
            else:
                ui.write(self.equipped[item].basicDesc[0].upper()+self.equipped[item].basicDesc[1:])


 

#npc
class nonPlayerCharacter(Character):
    def __init__(self, ID, startingRoom, name, basicDesc, inspectDesc, hostile = False, talk = None, interest = None, inventory = None, equip = None, action = None, doing = None,    hidden = False):
        super(nonPlayerCharacter,self).__init__(name,startingRoom, inventory,doing)

       
        if talk is None:
            talk = []
        if interest is None:
            interest=[]
        if inventory is None:
            inventory = []
        if equip is None:
            equip = []
        if action is None:
            action = []
        if doing is None:
            doing = ['',None,False]  
            
        self.ID = ID #  "ID" = nonPlayerCharacter("ID"...)
        self.name = name # what user calls em
        self.basicDesc = basicDesc # describes them
        self.inspectDesc = inspectDesc # if inspected
        self.room = startingRoom # Where they are
        self.hostile = hostile # If character can interact with player in non-hostile/violent methods & if will attack player unprovoked
        self.talk = talk # gee, like all the text for a conversation
        self.interest = interest # not sure what this is?
        self.inventory = inventory # in their pockets and bag
        self.equip = equip # in their hands and on their body
        self.action = action # What the character will do as soon as all the shit for the room is made - allows character to be doing something as Player enters room
                             # Perhaps expand to do more things at certain triggers ToDo
        self.doing = doing # What is currently being done, ['verb' (plain english),object (pointer), IfActivityFullyOccupying (bool)]

        self.hidden = hidden

        

    def Initialise(self):
        for item in self.action:
            print(item) 
            exec(item)
            
##            try:
##                pass
##              #  exec(item) # put this in here
##            except:
##                pass
            
    def StopBlocking(self,tool): # Player is attempting to make the npc stop blocking the door
        if self.doing[0] == 'blocking':
            if self.doing[1].hidden:
                self.doing[1].hidden = False
                ui.write("The %s is moved out of the way, you can now see a %s behind it"%(self.name,self.doing[1].name.split()[-1]))
                ui.write("You can now see %s"%self.blocking[1].basicDesc)
            else:
                ui.write("%s stops blocking the %s"%((self.name[0].upper()+self.name[1:]),self.doing[1].name))
            self.doing = ['',None,False]
            return(True)
        else:
            ui.write("%s is not blocking anything!"%(self.name[0].upper()+self.name[1:]))
            return(False)
        

class playerCharacter(Character):
    def __init__(self, name, startingRoom, inventory = None,doing = None):
        super(playerCharacter,self).__init__(name, startingRoom, inventory, doing)

        if inventory is None:
            inventory = []
        if doing is None:
            doing = ['',None,False]
            
        #this should really be in the Character class but I want to make sure it's working first


    def MovedRoom(self): #call whenever character enters new room
        self.ShowLocation()
        self.currentRoom.EnteredRoom()
       
        

    
    def UseItem(self, item):
        #the actual use
        if item.expendable[0] == True:
            if item.expendable[1] <= 1:
                self.inventory.remove(item)
            else:
                item.expendable[1] = item.expendable[1] -1
            #if the item's expendable
            #a confirmation message should probably be put in here at some point

    def Inspect(self,item,using):

        
        if isinstance(item, invFurnClass.inventoryObject):
            ui.write("This " + item.name + " belongs to " + item.taken[0] + ".")
            ui.write(item.inspectDesc[0].upper()+item.inspectDesc[1:])
            if len(set(item.equippable[1]).intersection({"weaponRight","weaponLeft"})) > 0:
                ui.write('It can easily be held in one hand, the %s looks like it could be used as a weapon.'%item.name) # todo add weapon type here for description
            if "weaponBoth" in item.equippable[1]:
                ui.write('It is quite heavy, looks like you\'ll need both hands to use this. The %s would make a mighty weapon though.'%item.name)
            if "clothesTorso" in item.equippable[1]:
                ui.write('The %s is quite thin and lightweight, it won\'t provide much in the way of protection. It does make a fine shirt though.'%item.name)
            if "clothesLegs" in item.equippable[1]:
                ui.write('It is not very thick or heavy, it won\'t be much use as protection, but the %s looks to be a good fit as trousers.'%item.name)
            if "armwear" in item.equippable[1]:
                ui.write('This looks like it would fit snugly on your arm, would look quite good there too.')
            if "headgear" in item.equippable[1]:
                ui.write('You feel it would for your head quite well, it\'s almost begging to be put on.')
            if "footwear" in item.equippable[1]:
                ui.write('Looks like these would make some pretty good shoes, they seem they seem about the right size for you.'%item.name)
            if "armourTorso" in item.equippable[1]:
                ui.write('It looks really quite sturdy, the %s looks like it could offer some serious protection for your upper body.'%item.name)
            if "armourLegs" in item.equippable[1]:
                ui.write('These look like some heavy duty trousers, the %s could be used to protect your lower body in combat.'%item.name)
            if "accessories" in item.equippable[1]:
                ui.write('The %s won\'t be much good in the way of utility, you\'re sure it would look quite pretty on you none the less.'%item.name)

            
            if item.unlocks[0]:
                for action in item.unlocks[1]:
                    if action[0] == "K":
                        ui.write("The writing on this %s makes implies it opens some lock with the ID %s."%(item.name,item.unlocks[1][0][1:]))
                    else:
                        ui.write("This looks like it could be used to %s open weak or vunerable objects, or doors."%action)
                
        elif isinstance(item, invFurnClass.roomFurnishing):
            ui.write(item.inspectDesc[0].upper()+item.inspectDesc[1:])
            if item.opened[0]:
                if item.opened[1]:
                    ui.write('The %s is open'%item.name)
                    if len(item.containedObjects) > 0:
                        ui.write('It contains:')
                        for thing in item.containedObjects:
                            ui.write(thing.name[0].upper()+thing.name[1:])
                    else:
                        ui.write('The %s is empty.'%item.name)
                            
                else:
                    ui.write('The %s is closed'%item.name)
                    
                    if item.locked[0]:
                        ui.write('It appears to be locked.')
                        for action in item.locked[1]:
                            if action[0] == "K":
                                ui.write("It appears like a key or keycard of some kind could be used to unlock this")
                            else:
                                ui.write("Given the appropriate tool, it looks like it could be %sed open with some effort."%action)
                    else:
                        ui.write('It doesn\'t seem to be locked in any way')
                    
            if item.interactive[0] == True:
                for interaction in item.interactive[1]:
                    if interaction != "open":
                        ui.write("It looks like this could be " + interaction + "ed.")
            
                    
           
        elif isinstance(item, doorClass.Door):
            ui.write(item.description)
            ui.write('It is to your %s'%item.name[:-5])
            if item.opened:
                ui.write('The door is wide open')
                if self.currentRoom.name != item.room1.name and item.seeThrough:
                    ui.write('You can see this door leads to %s.'%item.room1.search)
                elif self.currentRoom.name != item.room2.name and item.seeThrough:
                    ui.write('You can see this door leads to %s.'%item.room2.search)
                else:
                    ui.write("It isn't clear where this leads")

            else:
                ui.write('The door is closed')
                if item.locked[0]:
                    ui.write("It seems to be locked. That or it's rusted shut.")
                    for action in item.locked[1]:
                        if action[0] == "K":
                            ui.write("It appears like a key or keycard of some kind could be used to unlock this")
                        else:
                            ui.write("Given the appropriate tool, it looks like it could be %sed open with some effort."%action)
                else:
                     ui.write("It doesn't appear to be locked. It looks as if it could be opened with a heafty pull.")
                     
                ui.write("You aren't sure where it leads.") # ToDo change this for previously visited rooms
                
            if item.locked[0] and item.locked[2]:
                ui.write("There is a sign next to the door, it is faded but you make out the number %s"%item.locked[1][0][1:])



        elif isinstance(item,nonPlayerCharacter):
            ui.write(item.inspectDesc)
            if item.hostile:
                ui.write("They don't look too friendly..")
            else:
                ui.write("They look quite approachable.")
                
            if item.doing[0] != '':
                if item.doing[2]:
                    ui.write("They seem rather occupied with %s the %s."%(item.doing[0],item.doing[1].name))
                else:
                    ui.write("They are %s the %s but that doesn’t seem to have their full attention."%(item.doing[0],item.doing[1].name))
            else:
                ui.write("They don't seem to be doing much at the moment.")

            if len(item.talk) > 0:
                ui.write(item.name + " might talk to you.")

            # ToDo impliment descriptions for equipt things




                

    def TakeItem(self, item):
    
        
        if item in self.currentRoom.objects:
            if item.taken[0] == "No-one" or item.taken[0] == "you":
                item.taken[0] = "you"
                self.inventory.append(item)
                item.location = self
                
                self.currentRoom.objects.remove(item)
                for furnishing in self.currentRoom.furnishings:
                    if item in furnishing.containedObjects:
                        furnishing.containedObjects.remove(item)
                        
                ui.write(item.taken[1][0].upper()+item.taken[1][1:] +' '+ item.name + ".")
            else:
                ui.write("That's not yours.")
        elif item in self.inventory:
            ui.write("That's already in your inventory")
        else:
            ui.write("That's not in the room.")

    def EquipItem(self,item):
        if item in self.inventory:
            if self.equipped[item.equippable[1][0]] == None:
                self.equipped[item.equippable[1][0]] = item
            elif self.equipped[item.equippable[1][0]] == [] or isinstance(self.equipped[item.equippable[1][0]], list):
                #NOTE: THIS MIGHT NOT WORK
                self.equipped[item.equippable[1][0]].append(item)
            else:
                self.equipped[item.equippable[1][0]] = item
                #I'll put a swap confirmation message here when I'm bothered enough by it
        else:
            ui.write("That item is not in your inventory.")

    def DropItem(self, item):
        if item.droppable == False:
            ui.write("You need this for something.")
        else:
            self.inventory.remove(item)
            self.currentRoom.objects.append(item)
                
    def DisplayInventory(self):
        ui.write("You have in your possession: ")
        for item in self.inventory:
            ui.write(item.basicDesc[0].upper()+item.basicDesc[1:])
            

    def MoveRooms(self, door):
        door.Open(None,self,True)
        if door.opened and not door.blocked[0]:
            door.goThrough(self)
            #self.opened()
               
                
    def ShowLocation(self):
        ui.write("You are in " + self.currentRoom.search)

    def SearchRoom(self):
        ui.write(self.currentRoom.DescribeRoom())

    def Talk(self, other):
        ui.talkWindow(self,other)

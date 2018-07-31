from __main__ import *
class Door(object):
    def __init__(self, doorID, room1, room2, direction, locked = None, blocked = None, canOpen = True, opened=False, seeThrough = True, description = 'A basic, nondescript door. It looks quite old.', hidden = False):

        
##        if interactive is None:
        interactive = [True,set(['Search'])]
            
        if locked is None:
            locked = [False,[],False]
            #[Is locked, [what unlocks/locks it], if it has indication of what locks it]
        if blocked is None:
            blocked = [False,None]
            #[Is blocked, what is blocking it]

        self.doorID = doorID
        self.room1 = room1
        self.room2 = room2
        self.name = ""
        self.description = description
        self.opened = opened
        self.locked = locked
        self.blocked = blocked
        
        self.interactive = interactive
        
        self.canOpen = self.locked[0] or self.blocked[0]


        #if it's locked, and if so, what's used to unlock it  #this comment is in the wrong place
        
        self.seeThrough = seeThrough
        #If door is open, can player see into the connected room

        self.hidden = hidden
        self.direction = direction
        self.directionList = ['north door','east door','south door','west door']
        self.opositeDirectionList = ['south door','west door','north door','east door']
        self.name = self.directionList[self.direction]
        self.basicDesc = "a "+self.name
        #the direction RELATIVE TO ROOM1

        self.UpdateInteractions()

    def UpdateInteractions(self):
    
        if not self.opened:
            self.interactive[1].add('Open')
            self.interactive[1].discard('Close')
        else:
            self.interactive[1].add('Close')
            self.interactive[1].discard('Open')


        if self.blocked[0]:
            self.interactive[1].add('Unblock')

        
        if self.locked[0]:
            if len(self.locked[1])>0:
                self.interactive[1].add('Unlock')
                self.interactive[1].discard('Lock')
                
        else:
            if self.locked[1] is not None and self.locked[1] != {}:
                self.interactive[1].add('Lock')
                self.interactive[1].discard('Unlock')

            else:
                self.interactive[1].discard('Unlock')


                
        if not self.hidden:
            self.interactive[0] = True
            self.interactive[1].add('Search')
        else:
            self.interactive[0] = False # you cant interact with what you don't know is broken, potential bug
            self.interactive[1].discard('Search')




    def goThrough(self, player):
        print("REACHED goThrough (doorClass)")
        if player.currentRoom == self.room1:
            player.currentRoom = self.room2
            self.name = self.opositeDirectionList[self.direction]
        else:
            player.currentRoom = self.room1
            self.name = self.directionList[self.direction]
        player.MovedRoom()

##all mentioned direction relative to the centre of the room
##0 is south
##2 is north
##1 is west
##3 is east
##4 is above
##5 is below
##others might be added at some point if jake yaks at me enough
##
##and obviously for an overworld this either ain't gonna be necessary or will need to be changed, but we'll get to that


    def Open(self, openTool,traveling):

        if self.opened == True:
            ui.write("The door is already open.")
            
        elif self.opened == False and self.locked[0] == False and self.blocked[0] == False:
            self.opened = True
            ui.write("The " + self.name + " is not locked. You open it.")
             
        elif self.locked[0] == True and self.opened == False and self.blocked[0] == False:
            if openTool is not None and openTool != '':
                self.Unlock(openTool)
                if self.locked[0] == False:
                    self.opened[1] = True
            elif self.locked[0] == True and self.blocked[0] == False:
                ui.write("The door is locked, or perhaps it is only stuck. You can't get it open anyhow.")

        if self.blocked[0]:
            ui.write("The door is blocked by %s. You can't get close to it."%self.blocked[1].name)
                
        if self.opened and not traveling:                
            if playerCharacter.currentRoom.name != self.room1.name and self.seeThrough:
                ui.write('Through this door you can make out %s.'%self.room1.search)
            elif playerCharacter.currentRoom.name != self.room2.name and self.seeThrough:
                ui.write('Through this door you can see %s.'%self.room2.search)
            else:
                ui.write('It isn\'t clear where this leads.')
            ui.write('You stay standing in the doorway.')

    def Close(self,using):
        if self.opened == True:
            self.opened = False
            ui.write("You close the " + self.name)
        elif self.opened == False:
            ui.write("The " + self.name + " is already closed.")
            
    def Lock(self,key): #door
        locks = False
        if  self.locked[0]:
            ui.write("This is already locked")
            return()

        
        if self.opened:
            ui.write("The %s isn't closed."%self.name)
            return()

        if not isinstance(key,invFurnClass.inventoryObject):
            if key is None or key == '':
                ui.write("You're going to need something to lock this with.")
            else:
                ui.write("This isn't something that can be used that way.")
            return()

        if key not in playerCharacter.inventory:
            ui.write("You do not possess the %s"%key.name)
            return()

        ui.write("You attempt to lock the %s using the %s."%(self.name,key.name))

        if not key.unlocks[0]:
            ui.write("You won't be able to lock anything with that")
            return()

        for item in key.unlocks[1]:
            if item in self.locked[1]:
                locks = True

        if not locks:
            ui.write("This won't be able to lock the %s with this %s."%(self.name,key.name))
            return()

        ui.write("The %s is now locked firmly shut."%self.name)
        self.locked[0] = True

    def Unlock(self,key): #door
        specificUnlock = False
        generalUnlock = [False,None]
        if self.locked[0]:
            if isinstance(key,invFurnClass.inventoryObject):
                if key in playerCharacter.inventory:
                    ui.write("You attempt to open the %s using the %s"%(self.name,key.name))
                    if key.unlocks[0]:
                        for item in key.unlocks[1]:
                            if item in self.locked[1]:
                                if item[0] == "K":
                                    specificUnlock = True
                                else:
                                    generalUnlock = [True,item]

                        if specificUnlock:
                            self.locked[0] = False
                            ui.write("You insert the %s and the %s effortlessly clicks unlocked"%(key.name,self.name))
                            return()
                            
                        elif generalUnlock[0]:
                            self.locked[0] = False
                            self.locked[1] = []
                            self.opened = True
                            ui.write("You %s using the %s on the %s for some time untill it finally swings open. It is rather damaged now, doesn't look like that can be locked again"%(generalUnlock[1],key.name,self.name))
                            
                        else:
                            ui.write("Looks like that didn't do the job, the %s is still firmly shut"%self.name)
                    else:
                        ui.write("You won't be able to open anything with that")
                else:
                    ui.write("You do not possess the %s"%key.name)
            else:
                if key is None or key == '':
                    ui.write("You're going to need something to get this open...")
                else:
                    ui.write("This isn't something that can be used that way.")
        else:
            ui.write("The %s isn't locked..."%self.name)

        if self.locked[0]:
            for action in self.locked[1]:
                if action[0] == "K":
                    ui.write("You think some kind of key or keycard could be used to unlock this.")
                else:
                    ui.write("It looks like it could be %sed open with the appropriate tool."%action)



    def Block(self,thing, hides = False):
        
        if isinstance(thing,invFurnClass.inventoryObject):
            if thing.canBlock:
                self.blocked = [True,thing]
                self.hidden = hides
            else:
                ui.write("That cannot be used to block this")

        elif isinstance(thing,nonPlayerCharacter) or isinstance(thing,playerCharacter):
            self.blocked = [True,thing]
            self.hidden = hides
            thing.doing = ['blocking',self,True]

        elif isinstance(thing,roomFurnishing):
            self.blocked = [True,thing]
            self.hidden = hides
            thing.blocking = [True,self,hides]
            

    def Unblock(self,tool):
        if self.blocked[0]:
            if self.blocked[1].StopBlocking(tool):
                self.blocked = [False,None]

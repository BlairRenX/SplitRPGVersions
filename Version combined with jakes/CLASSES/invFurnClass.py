from __main__ import ui
class gameObject(object):
    def __init__(self, basicDesc, inspectDesc):
        self.basicDesc = basicDesc
        #a description that displays when you look at it

        self.inspectDesc = inspectDesc
        #a description that displays when you inspect it
        self.hidden = False
        #in case it's locked away and shouldn't be found immediately

        self.usable = []
        #gonna need to talk a lot of this over with jake when we get to integration

    def getDesc(self):
        
        return self.basicDesc




class roomFurnishing(gameObject): 
    def __init__(self, name, basicDesc, inspectDesc, interactive=None, containedObjects=None, opened=None, locked=None, blocked = None,blocking = None):
        super(roomFurnishing, self).__init__(basicDesc, inspectDesc)
        self.name = name

        if interactive is None:
            interactive = [False,[]]
            #[Can be interacted with,[what can be done]]

        if containedObjects is None or containedObjects == [None]:
            containedObjects = []

        if opened is None:
            opened = [False,None]
            #[Can be opened, if is opened]

        if locked is None:
            locked = [False,[]]
            #[Is locked, [what unlocks/locks it]

        if blocked is None:
            blocked = [False,None]
            #[Is being blocked, what by] obsolete?

        if blocking is None:
            blocking = [False,None,False]
            #[Is blocking, what is blocking, if obscures thing]

        self.investigation = []
        #as with the place investigation, but on a single furnishing within a room
        
        self.interactive = interactive
        
        
        
        self.containedObjects = containedObjects
        self.location = None
        for item in self.containedObjects:
            item.hidden = True

        self.opened = opened
        
        if len(self.containedObjects) > 0:
            self.interactive[0] = True
            self.interactive[1].append('open')
            self.opened = [True,False]


        self.locked = locked
        self.blocked = blocked
        
        self.canOpen = self.locked[0] or self.blocked[0]

        self.blocking = blocking

        if self.blocking[0]:
            self.blocking[1].Block(self,self.blocking[2])


        
        
    def Open(self,openTool,player,UsedWhenCalledOnDoor_ignoreButDontRemove):
        if self.opened[0] == True:
            if self.opened[1] == False:
                if self.locked[0] == False:
                    self.opened[1] = True
                    ui.write("The " + self.basicDesc + " is not locked. You open it.")
            
                elif self.locked[0] == True:
                    if openTool is not None and openTool != '':
                        self.Unlock(openTool)
                        if self.locked[0] == False:
                            self.opened[1] = True
                    else:
                        ui.write("The %s won't open. It is locked tight shut, or perhaps only stuck."%self.name)


                if self.opened[1] == True: # if was closed but now open
                    if len(self.containedObjects) == 0:
                        ui.write("There was nothing inside.")
                    else:
                        ui.write("The " + self.basicDesc + " contains:")
                        for item in self.containedObjects:
                            item.hidden = False
                            self.location.objects.append(item)
                            ui.write(item.basicDesc)
                    
       
            elif self.opened[1] == True:
                ui.write("The door is already open.")
                if len(self.containedObjects) == 0:
                    ui.write("There was nothing inside.")
                else:
                    ui.write("The " + self.basicDesc + " contains:")
                    for item in self.containedObjects:
                        ui.write(item.basicDesc)
                
            
        else:
            ui.write('The ' + self.basicDesc + ' cannot be opened.') 
                    
    def Close(self,using):
        if self.opened[0] == True:
            if self.opened[1] == True:
                for item in self.containedObjects:
                    item.hidden = True
                    self.location.objects.remove(item)
                self.opened[1] = False
                ui.write("You close the "+ self.basicDesc)
            else:
                ui.write("This " + self.basicDesc + " is already closed.")
        else:
            ui.write("This " + self.basicDesc + " cannot be closed.")

    def Lock(self,key): # furnishing 
        ui.write('lock not (fully?) implemented')

        if not self.locked[0]:
            ui.write("It doesn't look like this can be locked at all")
            return()

        if not isinstance(key,inventoryObject):
            if key is None or key == '':
                ui.write("You're going to need something to lock this with")
            else:
                ui.write("This isn't something that can be used that way.")
            return()

        if key not in jeremy.inventory:
            ui.write("You do not possess the %s"%key.name)
            return()

        ui.write("You attempt to lock the %s using the %s."%(self.name,key.name))

        if key.unlocks[0]:
            for item in key.unlocks[1]:
                print(item, self.locked[1])
        else:
            ui.write("You won't be able to lock anything with that")
            return()
            
        
            

    def Unlock(self,key): # furnishing
        specificUnlock = False
        generalUnlock = [False,None]
        if self.locked[0]:
            if isinstance(key,inventoryObject):
                if key in jeremy.inventory:
                    ui.write("You attempt to open the %s using the %s."%(self.name,key.name))
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
                            
                        elif generalUnlock[0]:
                            self.locked[0] = False
                            self.locked[1] = []
                            ui.write("You %s using the %s on the %s for some time until it can finally be opened. It is rather damaged now, doesn't look like that can be locked again"%(generalUnlock[1],key.name,self.name))
                            
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

        if self.locked[0] and key in jeremy.inventory:
            for action in self.locked[1]:
                if action[0] == "K":
                    ui.write("You think some kind of key or keycard could be used to unlock this.")
                else:
                    ui.write("It looks like it could be %sed open with the appropriate tool."%action)



class inventoryObject(gameObject):
    def __init__(self, name, basicDesc, inspectDesc, unlocks = None, expendable = None, droppable=True, equippable = None, canBlock = False, doing=None, taken=None):
        super(inventoryObject,self).__init__(basicDesc, inspectDesc)

        if unlocks is None:
            unlocks = [False,[]]
            #[if unlocks anything, [what it unlocks]] (uses lock code)
            
        if expendable is None:
            expendable = [False,None]

        if equippable is None:
             equippable = [False,[]]
             #[Can be equipped,[Where]]

        if doing is None:
            doing = [False,None]
            #[doing something,what]

        if taken is None:
            taken = ["No-one","You pick up the"]
        

        self.name = name

        self.unlocks = unlocks 
        
        self.taken = taken
        #include things about ownership, a description when you pick it up, etc...

        self.droppable = droppable
        #removing itself from the bag, and so on...
        
        self.expendable = expendable
        #if it's expendable, and if so, how many uses it has

        self.equippable = equippable
        #currently using a simple numerical value for quality

        self.canBlock = canBlock
        # if item can block sommit

        self.doing = doing
        #if it is doing somethhing like blocking a door

        self.location = None

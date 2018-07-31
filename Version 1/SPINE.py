import sys
import random
from pprint import pprint
sys.path.insert(0, 'CLASSES')
#import charClass, placeClass, doorClass, invFurnClass
from charClass import *
from placeClass import *
from doorClass import *
from invFurnClass import *



##  Interpret is called first,
##  Interpret calls Simplify before it does anything serious,
##  At the end of interpret, Execute is called
##  Execute calls match input before doing anything important


def Execute(text, player):
    action = {}

    #text in form {'verb':Object,'using/do': Object}
    
    error = False

    if 'error' in text:
        error = True
        ui.write(text['error'])
    else:    
        for item in text:
            action[item] = MatchInput({item:text[item]},player)
            
        #ui.write(action) # Writes action done ToDO maybe remove this
        
        if error in action: # if any prev functions didn't suceed
            error = True
        for key in action: # double check nothing fucked up
            if isinstance(action[key],dict):
                error = True
            
    if not error: 
        if 'using' not in action: # if ya use nothing
            action['using'] = None # passes None when nothing is used
            
        
        allowed = {Place:['debug','search'],
                   Door:['debug','search','open','close','go','lock','unlock','block','unblock'],   # all the shit that can be done to a type
                   roomFurnishing:['debug','open','close','search','lock','unlock'],
                   inventoryObject:['debug','search','using','take','give','equip'],
                   nonPlayerCharacter:['debug','search','attack','talk','block','unblock'],
                   playerCharacter:['debug','search'],
                   str:['search','open']} # inventory (this is fuck ik, but haden didn't want the inventory to be a seperate class for pretty gd reasons)

        if player.doing[2]: # Certain things like blocking a doorway will prevent the player from doing other things within the room (causing attempts to do them to fail)
            toDel = []   
            ui.write("You are still %s the %s. Doing this requires will prevent you from doing certain things until you stop."%(player.doing[0],player.doing[1].name))
            for key in allowed:
                if not isinstance(key,(Place,playerCharacter,inventoryObject,str,type(player.doing[1]))): # keep an eye on this here, potential bug (because it's never (24/7/18) been tested)
                    toDel.append(key)
                    
            for key in action:
                if isinstance(key,inventoryObject):
                    if action[key] not in playerCharacter.inventory:
                        toDel.append(inventoryObject)
            for key in toDel:
                del allowed[key]
                        
                                  # honetsly i don't remember writing that section but we haven't (24/7/18) implemented a situation where it will come up yet so...
            
                

        # spine
        for key in action:
            allow = False
            for thing in allowed:
                if key in allowed[thing] and isinstance(action[key],thing):
                    allow = True
                    print(key)
                    
                    if key == 'search'  :
                        
                        if action[key] == player.currentRoom:
                            ui.write('You search the room.')
                            player.SearchRoom()
                        elif action[key] == 'inventory' or action[key] == player:
                            ui.write('You look in your bag.')
                            player.DisplayInventory()
                        else:
                            ui.write('You look closely at the %s.'%action[key].name)
                            player.Inspect(action[key],action['using'])
                            
                    elif key == 'go'  :
                        ui.write('You try to go through the %s.'%action[key].name)
                        print(action[key].room1.name)
                        print("from SPINE")
                        player.MoveRooms(action[key])
                        
                    elif key == 'attack'  :
                        ui.write('You try to attack at the %s!'%action[key].name)
                        action[key].Attack(action['using'])
                        
                    elif key == 'talk'  :
                        ui.write('You try to talk to %s.'%action[key].name)
                        action[key].Talk(action['using'])
                        
                    elif key == 'take'  :
                        ui.write('You try to take the %s.'%action[key].name)
                        player.TakeItem(action[key])
                        
                    elif key == 'open'  :
                        if action[key] == 'inventory':
                            ui.write('You look in your bag.')
                            player.DisplayInventory()
                        else:
                            ui.write('You try to open the %s.'%action[key].name)
                            action[key].Open(action['using'],False)
                            
                    elif key == 'close'  :
                        ui.write('You try to close the %s.'%action[key].name)
                        action[key].Close(action['using'])

                    elif key =='equip':
                        ui.write('You try to equipt the %s.'%action[key].name)
                        player.EquipItem(action[key])

                    elif key =='lock':
                        ui.write('You try to lock the %s.'%action[key].name)
                        action[key].Lock(action['using'])

                    elif key =='unlock':
                        ui.write('You try to unlock the %s.'%action[key].name)
                        action[key].Unlock(action['using'])

                    elif key == 'block':
                        ui.write('You try to block the %s.'%action[key].name)
                        if action['using'] is None:
                            action['using'] = jeremy
                        action[key].Block(action['using'])

                    elif key == 'unblock': # sorry this is kinda a mess. It's just to make it a little more robust
                        
                        if isinstance(action[key],roomFurnishing):
                            if action[key].blocked[0] == True:
                                ui.write('You try to unblock the %s.'%action[key].name)
                                action[key].Unblock(action['using'])
                            elif action[key].blocking[0] == True:
                                if action[key].blocking[2] == False: # If it's not obscuring what's behind it 
                                    ui.write('You try to unblock the %s.'%action[key].blocking[1][0].name)
                                else:                                
                                    ui.write('You attempt to move the %s.'%action[key].name)
                                action[key].blocking[1][0].Unblock(action['using'])
                                    
                        elif isinstance(action[key],nonPlayerCharacter):
                            if action[key].doing[1].hidden == True:
                                ui.write("You try to move"%action[key.name])
                            else:
                                ui.write("You try to stop %s from blocking the %s."%(action[key].name,action[key].doing[1].name))
                            action[key].doing[1].Unblock(action['using'])

                        else:
                            if action[key].blocked[0] == True:
                                ui.write('You try to unblock the %s.'%action[key].name)
                                action[key].Unblock(action['using'])

                    elif key == 'debug':
                        
                        
                        print('------------------------------------------------------------------------------')
                        print(action[key].name)
                        
                        pprint(vars(action[key]))
                        print('')
                        if action['using'] in ('inv','inventory'):
                            if isinstance(action[key],(nonPlayerCharacter,playerCharacter)):
                                for item in action[key].inventory:
                                    print(item.name)
                                    pprint(vars(item))
                            elif isinstance(action[key],roomFurnishing):
                                for item in action[key].containedObjects:
                                    print(item.name)
                                    pprint(vars(item))
                            if isinstance(action[key],Place):
                                for item in action[key].doors:
                                    print(item.name)
                                    pprint(vars(item))
                                print('')
                                for item in action[key].furnishings:
                                    print(item.name)
                                    pprint(vars(item))
                                print('')
                                for item in action[key].characters:
                                    print(item.name)
                                    pprint(vars(item))
                                print('')
                                for item in action[key].objects:
                                    print(item.name)
                                    pprint(vars(item))
                            print('')
                            
                    
                        
                    
                    elif key == 'using' and 'act' in action  :
                        action['on'].GeneralUse(action['using']) # This one maybe should be the other way round?
                    elif key == 'using'  :
                        pass
                    elif key == 'act'  :
                        pass
                    else:
                        print('Execute error')

            if not allow and action[key] is not None :
                ui.write('You cannot %s that.'%key)
                        
                            
    else: # if error
        ui.write('You cannot do this.')




        

##                  disallowed = {'search':False, 'move':False, 'attack':False, 'talk':False, 'open':False, 'close':False, 'using':False, 'act':False,'equip':False,'take':False}
##            if isinstance(action[key],Place):
##                disallowed['search'] = True
##            elif isinstance(action[key], Door):
##                disallowed['open'] = True
##                disallowed['close'] = True
##                disallowed['move'] = True
##            elif isinstance(action[key], roomFurnishing):
##                disallowed['open'] = True
##                disallowed['close'] = True
##                disallowed['search'] = True
##            elif isinstance(action[key], inventoryObject):
##                disallowed['search'] = True
##                disallowed['using'] = True
##            elif isinstance(action[key], nonPlayerCharacter):
##                disallowed['attack'] = True
##                disallowed['talk'] = True
            #we can change these as we see fit, but in terms of solutions this should be fine, right?
                
        
    

def MatchInput(text,player):

    #This one is a mess

    
    #need to add room and player to things
    #look: around, about, room
    #should default to player
    
    room = player.currentRoom
   
    things,inventoryThings = room.showAllObjectsAndNames() # gets all the object names and referances in a wee array
    

    # Takes form [[[Name for thing 1, Name for thing 2...],[thing 1, thing 2]], repeated for furnishings and etc]

    
##    for thingType in things:
##        for thing in thingType:
##            print(thing)

    things.append([['around','room','about'],[room,room,room]]) # these are all treated as the room
    things.append([['self','myself','me'],[player,player,player]]) # these strings are treated as player
    things.append([['inventory','bag'],['inventory','inventory']])# these as inventory
    whereLooking = 'sight'
    
    for key in text:
        if 'my ' in text[key]: # putting 'my' before nouns makes default look in inventory rather than room
            things = inventoryThings            
            text[key] = text[key].replace('my ','')
            whereLooking = 'your inventory' # used in output "there is not spoon in your inventory"
        
    similar = '' 
    

    action = {}                  

    done = False
    
 
        
    for key in text:
        action[key] = '' # there should only be one key in text, action now holds this indexing empty string
        for thingList in things: # iterates for everything that can be interacted with
            for i in range(len(thingList[0])): # there are a few layers of array
                if text[key] == thingList[0][i]: # if exact match with name
                    action[key] = thingList[1][i] # Sets value held by current verb to obj referance
                    break  #this might not work, bug (edit: i don't know why this might not work)

                elif text[key] in thingList[0][i] and similar == '': #Will catch any matching word (such as when player types only 'open door' or ' go north' both - 
                    action[key] =  thingList[1][i]                   # - resilve to the obj ref for 'north door'
                    similar = key
                elif text[key] in thingList[0][i] and similar != '':# Unless more than one object matches, in which case user will be asked to be more specific
                    action[similar] = ''


    for key in action: # only one key
        if action[key] == '': # if the key hasn't been set to an obj ref
            break # continues to next bit of code (next bit is complex so doesn't need to always run) more lenient 
        else:
            done = True # yay
            return(action[key]) # sucesfull
            
      
    if not done:
        for key in action:
            #if key not in ['using','take','give']
            thingType = [] 
            if action[key] == '':
                for thingList in things:
                    for i in range(len(thingList[0])): # same as above
                        thingList[0][i] = thingList[0][i].split() # splits multi word names into words
                        if thingList[0][i][-1] in text[key]: # if the final word of the obj is anywhere in the text
                            thingType.append([key,thingList[1][i],thingList[0][i]]) # write it in a list (hopes are this list will only have one element)
                            
                        
                            
            if len(thingType)!= 0: # we have at least one match!
                
                desc = []
                for i in range(len(thingType)):
                    desc.append('') # sets up new element as str
                    
                    for x in thingType[i][2]: # this is kinda a cluncky way to do it but i didn't know the inbuilt command at the time
                        desc[i] += x+' '
                    desc[i] = desc[i][:-1] # re-stitches the sentence of broken words back together (minus the trailing space)
                    
                if len(thingType) == 1: # only one match
                    ui.write('There is only one %s in %s: the %s.'%(thingType[0][2][-1],whereLooking,desc[0])) # This is broken , bug (edit: who knows what's wrong w this)
                    action[thingType[0][0]] = thingType[0][1]
                    return(action[key]) # sucess, returns obj
                else:
                    ui.write('There is more than one of these in %s:'%whereLooking) # there is more than one similar obj name
                    for item in desc:
                        ui.write('There is a %s'%item) # writes out what it's confused about
                    return({'error':'Ambiguous object'})
            else:
                ui.write('there is no %s in %s!'%(text[key].split()[-1],whereLooking)) # if there was no match at all in room (only now is inventory considered UNLESS USED 'my' IN INPUT)
                # Check inventory for object
                invThings = [[],[]]
                invObjects = [[],[]]
                
                for i in range(len(inventoryThings[0][0])): # yeah this is fuck but it works the samw way
                    invThings[0].append(inventoryThings[0][0][i].split()[-1])
                    invThings[1].append(inventoryThings[0][1][i])
                    if invThings[0][i] in text[key]:
                        invObjects[0].append(invThings[0][i])
                        invObjects[1].append(invThings[1][i])
                if len(invObjects[0]) == 1:
                    ui.write('There is a %s in your inventory: the %s.'%(invObjects[0][0],invObjects[0][0]))
                    action[key] = invObjects[1][0]
                
                    return(action[key])

                else:         
                    return({'error':'Object not recognised'})
        





def Interpret(text,player):

    text,verbs = Simplify(text)  # Calls simplify on the text in box
    

    objVerbs = ['take','give','equip'] # remember to add above too (this may be obsolete)
    objVerb = ''

    verbs.remove('using') # using treated differently
    using = 'using'
    
    currentVerb = ''
    verbNumber=0
    usingNumber=0
    words = text.split()
    do = {}


    for word in words: # each word in sentence
        for verb in verbs: # Finds verb in sentence
            if word == verb: 
                verbNumber+=1
                do[verb] = ''
                currentVerb = verb
                continue
                
        if word == using: # Finds 'using' in sentence
            usingNumber+=1
            do[using] = ''
            currentVerb = using
            
        if word not in verbs and word != using and currentVerb != '': # The nouns
            if do[currentVerb] == '': #nouns set as values of key being previous verb
                do[currentVerb]+=word
            else:
                do[currentVerb] += ' '+word # add space if not first word

    
    ###---Dirty fix for Use X on Y---###
    
    if usingNumber == 1 and verbNumber == 0 and words[0] == using: # must begin sentence with 'using'
        do['act'] = ''
        temp = do[using].split()
        do[using] = ''
        beforeOn = True
        for word in temp:

            if word == 'on': # pivots subject and object at word 'on' (it's not actually the subject as all sentences entered are imeratives the implied subject
                             # is the player, however i can't tell if one of the nouns is in dative case or if it's direct and indirect objects so fuckit)
                
                beforeOn = False
                
            if word != 'on' and beforeOn: # thrown into 
                if do[using] == '':
                    do[using] +=word
                else:
                    do[using] +=' '+word
            elif word != 'on' and not beforeOn:
                if do['act'] == '':
                    do['act'] +=word
                else:
                    do['act'] += ' '+word
    
        verbNumber+=1

        
    ###---Dirty fix for transfer object to/from X from/to Y---###  # not sure we need this after all
    for verb in objVerbs:
        if verb in do:
            objVerb = verb
   
    if objVerb != '' :
        do['to/from'] = ''
        temp = do[objVerb].split()
        do[objVerb] = ''
        beforeTF = True
        for word in temp:
            if word in ['to','from']:
               
                beforeTF = False
                
            if word not in ['to','from'] and beforeTF:
                if do[objVerb] == '':
                    do[objVerb] +=word
                else:
                    do[objVerb] +=' '+word
            elif word not in ['to','from'] and not beforeTF:
                if do['to/from'] == '':
                    do['to/from'] +=word
                else:
                   do['to/from'] += ' '+word
        if do['to/from'] == '':
            del do['to/from']
        
    
    for key in do: # Makes sure each verb has some nouns to go with it
        do[key] = do[key].replace('on ','') # remove garbage word 'on', used in dirty fix
        do[key] = do[key].replace('to ','')
        do[key] = do[key].replace('from ','')
        #do[key] = do[key].replace('in ','')
        if do[key] == '':
            if key == 'act':
                do[key] = 'self'
            else:
                Execute({'error':'What are you trying to %s?'%key},player)
                return()
                
   
    if verbNumber >1 or usingNumber>1: # more than one verb/using
        Execute({'error':'All that at once?'},player)
    elif verbNumber == 0: # no verbs
        Execute({'error':'What are you trying to do?'},player)
    else:
        Execute(do,player) #sucess!

                
        
def Simplify(text):

    # all the verbs
    
    toRemove = []
    fillerWords = ['','in','the','attempt','through','teh','a','try','trying','at','near','for','behind','under','while','and','by','toRemove']
    punctuation = [',','.','?','!','\'',';',':']
             
    using = ['use','using','with','activate','activating','fire','firing','turn','turning','inc','including']
    
    search = ['search','look','find','explore','inspect','observe','see']
    
    go = ['go','travel','walk','climb','enter']
    
    attack = ['attack', 'assault', 'hit','fight','kill']
    talk = ['talk','speak','talk to']
    
    take = ['take','grab','remove','carry','obtain','pick up','pick','steal']
    close = ['close','shut']
    inspect = []
    
    open_ = ['open'] #open is keyword, uses open_ instead

    unlock = ['unlock','smash'] # Add all general unlocking methods
    lock = ['lock'] 

    unblock = ['unblock','move']
    block = ['block']

    equip = ['equipt','put on','wear','hold']

    debug = ['debug'] # ToDo remove this only after beta tested

    verbs = ['debug','using','search','go','attack','talk','take','open','close','equip','lock','unlock','unblock','block']
    words = {'debug':debug,'using':using,'search':search,'go':go,'attack':attack,'talk':talk,'take':take,'open':open_,'close':close,'equip':equip,'lock':lock,'unlock':unlock,'unblock':unblock,'block':block}

    
                
    
        
    text = text.lower()
    text = text.split()
    sentence = ''
    
    for i in range(len(text)): # for each word in sentnce
        for verb in verbs:     # for each verb in verbs
            if text[i] in words[verb]: # ***The good bit***, if a word is in the array held by dictionary 'words'
                text[i] = verb  #replaces synonms of verbs with general case of verb from verbs array
            elif i < len(text) -1: # if not the last word in sentence 
                if text[i] + ' ' + text[i+1] in words[verb]: # checks two words to see - currently obsolete
                    text[i] = verb # replace first of word pair
                    text[i+1] = 'toRemove' # discard second

                    
        if i > 0: # removes repeated words (comes up like use with which resolve to the same word twice)
            if text[i] == text[i-1]:
                text[i-1] = 'toRemove'
                
    
        if text[i] in fillerWords:
            toRemove.append(text[i]) # get rid of garbage words (array as you can'd dynamically alter the length of a list you're iterating thorugh
            
        if text[i][-1] in punctuation:
            text[i] = text[i][:-1] # get rid of punctuation
            
        
              
    for word in toRemove:
        text.remove(word) #remove garbage words
        
    for word in text:
        sentence+=word+' ' #make array of words into sentence
    
    sentence = sentence[:-1] #remove trailing ' '

    if 'unlock' in text and 'open' in text: # catches phrases like "Smash Open" which resolve to unlock open - open automatically unlocks if able
        text.replace("unlock","")
    
    #Special cases
    if sentence in ('inventory','inv'): # short hand, just typing inv resolves to "open inventory"
        sentence = 'open inventory'
     
    return(sentence,verbs)









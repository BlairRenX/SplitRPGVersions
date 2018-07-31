#from __main__ import *
#from charReader import ui
import tkinter as tk
from random import randint

class GunUi():
    def __init__(self, main,player,enemy):
        self.text =''
        self.main = tk.Toplevel(main) 
        self.main.geometry("600x500")
        self.main.config(background ='#000000')
        self.main.focus_set()
        self.playerbtns = [[],[],[],[]]
        self.enemybtns = [[],[],[],[]]

        self.info = tk.Label(self.main,bg ='black',fg = '#22ee22', text = 'Arrows to move, \n space to skip moving,\n space to target, space to untarget,\n enter to attack, shift+r to reset')
        self.info.place(y = 150, x = 205)

        self.playerHits = tk.Label(self.main,bg ='black',fg = '#22ee22', text = 'Total Hits: 0\nDirect Hits: 0\nDamage Percentage: -%')
        self.playerHits.place(x = 50,y=320)
        self.enemyHits = tk.Label(self.main,bg ='black',fg = '#22ee22',text = 'Total Hits: 0\nDirect Hits: 0\nDamage Percentage: -%')
        self.enemyHits.place(x = 400,y=320)
        
        self.playerGridSize = 4
        for j in range (self.playerGridSize):
            for i in range(self.playerGridSize):
                self.topRow = tk.Button(self.main,height = 2, width = 4,bg = '#000000')
                self.topRow.place(y = 150+(40*j), x = 50+(37*i))
                self.playerbtns[j].append(self.topRow)
        self.enemyGridSize = 4
        for j in range (self.enemyGridSize):
            for i in range(self.enemyGridSize):
                self.topRow = tk.Button(self.main,height = 2, width = 4, bg = '#000000')
                self.topRow.place(y = 150+(40*j), x = 400+(37*i))
                self.enemybtns[j].append(self.topRow)


        self.enemyCharacter = [randint(0,self.enemyGridSize-1),randint(0,self.enemyGridSize-1)]
        self.numberEnemyMove = []

        
        self.moving = True
        self.attackPhase = False
        self.playerPos = [0,0]
        self.targetPos = [0,0]
        self.moves = []
        self.enemyMoves = []
        self.numberEnemyMove =  0
        self.targeted = []
        self.playerbtns[self.playerPos[0]][self.playerPos[1]].config(background = 'green')

        self.playerCanTarget = 4
        
        self.enemyMovement = 3
        self.enemyCanTarget = 4
        
        self.playerDarkGreenHits = 0
        self.playerLightGreenHits = 0

        self.enemyDarkBlueHits = 0
        self.enemyLightBlueHits = 0

        

        
##        self.me = tk.Button(self.main,height = 1, width = 2)
##        self.me.place(x = 5,y=10)
        #self.talkBTN = tk.Button(self.main, text='Talk', background = 'light blue', height = 2, command = lambda:(self.TalkEnter(self.inpt,self.inpt.get('1.0','end'),npc) ))
       # self.
        
        #self.inpt =  tk.Text(self.main, height = 1)
        #self.inpt.bind("<Return>", lambda x: self.TalkEnter(self.inpt,self.inpt.get('1.0','end-1c'),npc))
        #self.inpt.bind("<space>", lambda x:self.inpt.delete('0.0','end+2c'))
        #self.inpt.place(relx =0.36, rely = 0.65,  relwidth=0.25)


        #self.btns[0][3].config(background = 'black')

##
        self.main.bind("<Left>", lambda x:self.PlayerMove([0,-1]))
        self.main.bind("<Right>", lambda x:self.PlayerMove([0,1]))
        self.main.bind("<Up>", lambda x:self.PlayerMove([-1,0]))
        self.main.bind("<Down>", lambda x:self.PlayerMove([1,0]))
        self.main.bind("<space>",lambda x:self.PlayerTarget())
        self.main.bind("<Return>",lambda x:self.EnemyMove())
        self.main.bind("<R>",lambda x:self.Reset()) ## To Remove ToDO


    def Reset(self):
        if len( self.enemyMoves)>0: 
            self.enemyCharacter = [self.enemyMoves[-1][0],self.enemyMoves[-1][1]]
        else:
            self.enemyCharacter = [randint(0,self.enemyGridSize-1),randint(0,self.enemyGridSize-1)]
        self.numberEnemyMove = []
         
        for lst in self.enemybtns:
            for btn in lst:
                btn.config(bg='#000000')
        for lst in self.playerbtns:
            for btn in lst:
                btn.config(bg='#000000')
            
        self.moving = True
        self.attackPhase = False
        self.targetPos = [0,0]
        self.moves = []
        self.enemyMoves = []
        self.numberEnemyMove =  0
        self.targeted = []
        self.playerbtns[self.playerPos[0]][self.playerPos[1]].config(background = 'green')

       
        
        self.playerDarkGreenHits = 0
        self.playerLightGreenHits = 0

        self.enemyDarkBlueHits = 0
        self.enemyLightBlueHits = 0

        
    def PlayerMove(self,direction):
        if not self.attackPhase:
            if len(self.moves) >= 3:
                self.moving = False
            if self.moving:
                if self.playerPos[0] + direction[0] >= 0 and self.playerPos[0] + direction[0] < self.playerGridSize and self.playerPos[1] + direction[1] >= 0 and self.playerPos[1] + direction[1] < self.playerGridSize:      
                    self.playerbtns[self.playerPos[0]][self.playerPos[1]].config(background = '#62ff3f')
                    self.playerPos[0]+=direction[0]
                    self.playerPos[1]+=direction[1]
                    self.moves.append(direction)
                    self.playerbtns[self.playerPos[0]][self.playerPos[1]].config(background = 'green')
                    if len(self.moves) == 3:
                        self.enemybtns[0][0].config(bg = 'blue')
                    self.main.update()
            else:   
                if self.targetPos[0] + direction[0] >= 0 and self.targetPos[0] + direction[0] < self.playerGridSize and self.targetPos[1] + direction[1] >= 0 and self.targetPos[1] + direction[1] < self.playerGridSize:
                    if [self.targetPos[0],self.targetPos[1]] not in self.targeted:
                        self.enemybtns[self.targetPos[0]][self.targetPos[1]].config(background = '#000000')
                    self.targetPos[0]+=direction[0]
                    self.targetPos[1]+=direction[1]
                    if [self.targetPos[0],self.targetPos[1]] not in self.targeted:
                        self.enemybtns[self.targetPos[0]][self.targetPos[1]].config(background = 'blue')
                    self.main.update()
                
    def PlayerTarget(self):
        if not self.attackPhase:
            if self.moving:
                self.moving = False
                self.enemybtns[0][0].config(bg = 'blue')
            else:
                if self.targetPos not in self.targeted and len(self.targeted) <self.playerCanTarget:
                    self.enemybtns[self.targetPos[0]][self.targetPos[1]].config(background = 'red')
                    self.targeted.append(self.targetPos[:])
                elif self.targetPos in self.targeted:
                    self.enemybtns[self.targetPos[0]][self.targetPos[1]].config(background = 'blue')
                    self.targeted.remove(self.targetPos[:])
            self.main.update()


    
                        
    def PlayerAttack(self):
        if self.attackPhase:
            for item in self.targeted:
                for i in range(len(self.enemyMoves)):
                    if self.enemyMoves[i] ==item and i <len(self.enemyMoves)-1:
                        self.enemyLightBlueHits +=1
                        self.enemybtns[self.enemyMoves[i][0]][self.enemyMoves[i][1]].config(bg = 'gold')
                    elif self.enemyMoves[i] ==item and i == len(self.enemyMoves)-1:
                        self.enemyDarkBlueHits+=1
                        self.enemybtns[self.enemyMoves[i][0]][self.enemyMoves[i][1]].config(bg = 'orange')
                

                if item not in self.enemyMoves:
                    self.enemybtns[item[0]][item[1]].config(bg = 'red')
                    
                self.main.update()
                time.sleep(0.5)
        



                                    
    def EnemyAttack(self):
        if self.attackPhase:
            targets = []
            for i in range(self.enemyCanTarget):
                for i in range(self.playerGridSize**2):
                    target = [randint(0,self.playerGridSize-1),randint(0,self.playerGridSize-1)]
                    if target not in targets:
                        break
                if target not in targets:
                    targets.append(target)
                    if self.playerbtns[target[0]][target[1]]["background"] == 'green':
                        self.playerbtns[target[0]][target[1]].config(bg = 'gray')
                        self.playerDarkGreenHits+=1
                    elif self.playerbtns[target[0]][target[1]]["background"] == '#62ff3f': # light green
                        self.playerbtns[target[0]][target[1]].config(bg = 'dark gray')
                        self.playerLightGreenHits+=1
                    else:
                        self.playerbtns[target[0]][target[1]].config(bg = 'red')
                
                self.main.update()
                time.sleep(1)
            
            
    def EnemyMove(self):
        self.attackPhase = True
        for i in self.enemybtns:
            for btn in i:
                btn.config(bg='#000000')
        
        self.enemyMoves.append(self.enemyCharacter)
        
      
        self.enemybtns[self.enemyCharacter[0]][self.enemyCharacter[1]].config(bg = 'blue')
        self.main.update()
        time.sleep(1)
        
        enemyPos = self.enemyCharacter[:]
        self.numberEnemyMove = 0
        if randint(0,1): # move less than maximum
            move = randint(0,self.enemyMovement)
        else:
            move = self.enemyMovement
        for i in range(move):
            rand = randint(0,3)
            directions = [[0,1],[0,-1],[1,0],[-1,0],[0,1],[0,-1],[1,0],[-1,0]] # will randomly pick one of first 4, then cycle until valid
            direction = directions[rand][:]
            for j in range(4):
                
                if enemyPos[0] + direction[0] >= 0 and enemyPos[0] + direction[0] < self.enemyGridSize and enemyPos[1] + direction[1] >= 0 and enemyPos[1] + direction[1] < self.enemyGridSize and(enemyPos[0]+direction[0]!=self.enemyCharacter[0] or enemyPos[1]+ direction[1]!=self.enemyCharacter[1]):
                    self.numberEnemyMove+=1
                    enemyPos[0]+=direction[0]
                    enemyPos[1]+=direction[1] # enemy
                    for item in self.enemyMoves:
                        self.enemybtns[item[0]][item[1]].config(bg = '#7caeff')#light blue
                    self.enemybtns[enemyPos[0]][enemyPos[1]].config(bg = 'blue')
                    self.enemyMoves.append(enemyPos[:])
                    self.main.update()
                    time.sleep(1)
                    break
                else:
                    rand+=1
                    direction = directions[rand][:]
        for item in self.enemyMoves:
            self.enemybtns[item[0]][item[1]].config(bg = '#7caeff')
        self.enemybtns[self.enemyMoves[-1][0]][self.enemyMoves[-1][1]].config(bg = 'blue')
        self.PlayerAttack()
        self.EnemyAttack()  
        self.Damage()


    def Damage(self):

        if len(self.moves) == 0:
            self.playerDamagePercent =self.playerDarkGreenHits
        else:
            self.playerDamagePercent = (self.playerDarkGreenHits*(1-len(self.moves)/6) + self.playerLightGreenHits/6)#len(self.moves)*(1-(1-len(self.moves)/6)) # Fuckin headache right
        
##        if len(str(self.playerDamagePercent)) > 5:
##            self.playerDamagePercent = str(self.playerDamagePercent)[:6]
        
        
        newPText = 'Total Hits: %s\nDirect Hits: %s\nDamage Percentage: %.2f%s'%((self.playerLightGreenHits+self.playerDarkGreenHits),self.playerDarkGreenHits,(self.playerDamagePercent*100),'%')

        self.playerHits.config(text =newPText)

        if self.numberEnemyMove == 0:
            self.playerDamagePercent =self.playerDarkGreenHits
        else:
            self.enemyDamagePercent = (self.enemyDarkBlueHits*(1-self.numberEnemyMove/6) + self.enemyLightBlueHits/6)

##        if len(str(self.enemyDamagePercent)) > 5:
##            self.enemyDamagePercent =str(self.enemyDamagePercent)[:6]
        newEText = 'Total Hits: %s\nDirect Hits: %s\nDamage Percentage: %.2f%s'%((self.enemyDarkBlueHits+self.enemyLightBlueHits),self.enemyDarkBlueHits,(self.enemyDamagePercent*100),'%')
        self.enemyHits.config(text =newEText)


import tkinter as tk
from __main__ import *

class UI():
    #setup makes main window
    def __init__(self, main):
        self.main = main
       ##self.output = tk.Label(main, anchor = 'nw', justify = 'left')
        self.inpt =  tk.Text(main, height = 1,fg='#22ee22', background = '#003000')
        self.enterbut = tk.Button(main, text='Enter',fg='#22ee22', background = '#000100', height = 1, command = lambda:( self.enter(self.inpt,self.inpt.get('1.0','end')) ))
        self.text = ''

       # self.situation = ["You stand in an empty room. There is a door ahead of you and a door behind you", ["Try north door", "Try south door", "Other"]]
    
   
        
        self.main.geometry("850x700")
        self.main.config(background ='#000800')

        #Big output text box. Disabled so cannot be typed in.
        #rel-x,y,height,width are relative placement for window
        #self.output = tk.Label(main, anchor = 'nw', justify = 'left')
        self.output = tk.Label(main, anchor = 'nw', justify = 'left',  font = ('Courier New', 9), fg='#22ee22', bg='#000800')
        self.output.place(relx =0.2, rely = 0.02, relheight=0.6, relwidth=0.8)

        #Input box
        #calls 'enter' on key press return/enter key
        
        self.inpt.bind("<Return>", lambda x: self.enter(self.inpt,self.inpt.get('1.0','end-1c')))
        self.inpt.place(relx =0.2, rely = 0.65,  relwidth=0.5)
        #enter is called with the .get() which takes from the ext box.
        # 1.0 is line.character, so line-1.position=0
        # end is end if text box, -1c is less 1 character (can be written as -1character)
        # 'end-1c' as oppose to 'end' ommits end \n from typed enter key

       # self.fightBTN = t

        #button that calls 'enter' same as above, save for not having the -1c after 'end' as no \n is typed (hope this makes sense)
        
        self.enterbut.place(relx = 0.71, rely = 0.645, relwidth = 0.09)


    #write fucntion takes text and the textbox it's from 
    def enter(self,inpt,txt):
        txt = self.cleanInput(txt)
        self.cleanOutput()
        if isinstance(txt,str):
           
            
            txt = txt.replace('\n','')

            if txt == 't':
                self.talkWindow(playerCharacter,C1)
            if txt == 'g':
                self.gunWindow(None,None)
            
            self.write('\n')
            txt = txt+'\n'
            for i in txt:
                #Types to the end of textbox with value i
                self.text += i
                self.output.config(text = self.text)

                self.inpt.delete('end-2c','end-1c')
                #sleep for that cool typing effect
               ## time.sleep(0.03)
                #tkinter is shit
                self.main.update()
            #scrolls output to bottom (without its not possible to scroll at all, its odd)   
            #makes sure input is empt but is currently buggy not sure why, seems to automatically lead with a \n or ' ' weird ass shit
            import SPINE
            from __main__ import playerCharacter
            SPINE.Interpret(txt,playerCharacter)
            
            self.inpt.delete('0.0','end')
            #disable output so cannot be typed in
        else:
            pass
           
    def write(self,txt):
        txt = str(txt)
        txt = self.cleanInput(txt)
        self.cleanOutput() 
        txt+='\n'
        self.inpt.config(state = 'disabled')
        for i in txt:
            self.text += i
            self.output.config(text = self.text)
           ## time.sleep(0.05)
            #tkinter is shit
            self.main.update()
        self.inpt.config(state = 'normal')
        

    def cleanOutput(self):
        while self.text.count('\n')>23:
            cutof = self.text.index('\n')+1
            self.text = self.text[cutof:]

    def cleanInput(self,txt):
        if isinstance(txt,str):
            if len(txt)>0:
                if txt[0] == '\n':
                    txt = txt[1:]
                n = 0
                for i in range(len(txt)):
                    if txt[i] != '\n':
                        n+=1
                    else:
                        n = 0
                        
                    if n > 80 and txt[i] == ' ': #arbriaty number
                        n = 0
                        txt = txt[:i] + '\n' + txt[i+1:]
                    elif n > 95:
                        n = 0
                        txt = txt[:i] + '-\n' + txt[i:]
                return(txt)
            
    def talkWindow(ui,player,npc):
        import TALK_UI
        talkUi = TALK_UI.TalkUi(main,player,npc)
    def gunWindow(ui,player,enemy):
        import GUN_UI
        gunUi = GUN_UI.GunUi(main,player,enemy)

    def testFunc(self):
        return("from one....to another.")
            
if __name__ == '__main__' :
    print("aw yis")
    main = tk.Tk()
    ui = UI(main)


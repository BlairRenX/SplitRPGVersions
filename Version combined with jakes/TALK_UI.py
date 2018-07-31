from __main__ import *
import tkinter as tk
class TalkUi():
    def __init__(self, main,player,npc):
        self.text =''
        self.main = tk.Toplevel(main) 
        self.main.geometry("600x500")
        self.main.config(background ='#001100')

        self.output = tk.Label(self.main, anchor = 'nw', justify = 'left')
        self.output.place(relx =0.2, rely = 0.02, relheight=0.6, relwidth=0.6)

        self.talkBTN = tk.Button(self.main, text='Talk', background = 'light blue', height = 2, command = lambda:(self.TalkEnter(self.inpt,self.inpt.get('1.0','end'),npc) ))
       # self.
        
        self.inpt =  tk.Text(self.main, height = 1)
        self.inpt.bind("<Return>", lambda x: self.TalkEnter(self.inpt,self.inpt.get('1.0','end-1c'),npc))
        self.inpt.bind("<space>", lambda x:self.inpt.delete('0.0','end+2c'))
        self.inpt.place(relx =0.36, rely = 0.65,  relwidth=0.25)
        self.conversationBegin(npc)

        self.mood = [' angry at ',' unhapy with ',' taken aback by ',' fine with ',' happy with ',' enthusiastic with ', ' ecstatic at ']
        
        self.prevWord = 'start'

    def conversationBegin(self,npc):
        self.TalkWrite('You enter conversation with a '+npc.desc)
        self.TalkWrite(npc.name+ ':    ' + npc.talk['start'][0])
        self.inConversation = True



    def reply(self,npc,word):
        if self.inConversation:
            if word in npc.talk:
                if npc.interest + npc.talk[word][1][0] < 7:
                    npc.interest += npc.talk[word][1][0]
                else:
                    npc.interest = 6
                if npc.interest + npc.talk[word][1][0] < 0:
                    self.TalkWrite('That seems to have struck a nerve with %s, they turn away. This conversation is clearly over.'%npc.name)
                    self.inConversation  = False
                else:    
                    self.TalkWrite(npc.name+ ' seems' +self.mood[npc.interest] +'your response')
                    self.TalkWrite(npc.name+ ':    ' + npc.talk[word][0])
                    self.prevWord = word
                
            if word not in npc.talk:
                if npc.talk[self.prevWord][1][1] != 0:
                    npc.interest += npc.talk[self.prevWord][1][1]
                    if npc.interest >-1:
                        self.TalkWrite(npc.name+ ' seems' +self.mood[npc.interest] +'your response')
                    else:
                        self.TalkWrite(npc.name +' has had enough of you. This conversation is clearly over')
                        self.inConversation = False
                else:
                    self.TalkWrite(npc.name + ' didn\'t understand you, but they didn\'t seem to care. They are still' + self.mood[npc.interest] +'you.')





    def TalkEnter(self,inpt,txt,npc):
        
        txt = txt.replace('\n','')
        if txt[-1] in ('?','.',' ','\n'):
            txt = txt[:-1]
        if txt[0] == ' ':
            txt = txt[1:]
        txt = self.cleanInput(txt)
        self.cleanOutput()
        txt = txt+'\n'
        for i in txt:
            self.text += i
            self.output.config(text = self.text)
            
            self.inpt.delete('end-2c','end-1c')
            time.sleep(0.01)
            #tkinter is shit
            self.main.update()
        txt = txt.replace('\n','')
        self.reply(npc,txt)
        self.inpt.delete('0.0','end')

                    
    def TalkWrite(self,txt):
        txt = self.cleanInput(txt)
        self.cleanOutput()
        txt+='\n'
        self.inpt.config(state = 'disabled')
        for i in txt:
            self.text += i
            self.output.config(text = self.text)
            time.sleep(0.03)
            #tkinter is shit
            self.main.update()
        self.inpt.config(state = 'normal')

    def cleanOutput(self):
        if self.text.count('\n')>16:
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
                        
                    if n > 50 and txt[i] == ' ': #arbriaty number
                        n = 0
                        txt = txt[:i] + '\n' + txt[i+1:]
                    elif n >65:
                        n = 0
                        txt = txt[:i] + '-\n' + txt[i:]
                return(txt)

if __name__ == '__main__':
    print("running script directly...")
else:
    print("running from external script...")

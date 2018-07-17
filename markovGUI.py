import sys
import random
from Tkinter import *
import Tkinter, tkFileDialog, tkMessageBox
from ScrolledText import *


class Generator:
    def __init__(self):
        self.root = Tk()
        self.textLength = IntVar(value=100)
        self.fileName = "No files imported yet"
        self.statusBar = Label(self.root, bd=2, text=self.fileName, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)
        self.textBox = ScrolledText(self.root, height=18, width=47, bg="white", wrap=WORD, )
        self.textBox.pack(side=RIGHT, fill=X)
        self.root.title('Markov Chain Generator - Brian Dinh')
        self.root.minsize(width=550, height=350) # fixed height and width
        self.root.maxsize(width=550, height=350)
        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side=LEFT)
        self.entryBoxLabel = Label(self.leftFrame, text='Text Length: ', anchor=W)
        self.entryBoxLabel.pack(side=TOP)
        self.entryBox = Entry(self.leftFrame, textvariable=self.textLength, width=15, justify=CENTER)
        self.entryBox.pack(side=TOP)
        self.importButton = Button(self.leftFrame, text="Import Text", height=5, width=20, command=self.importText)
        self.importButton.pack(side=TOP, pady=7)
        self.generateButton = Button(self.leftFrame, text="Generate Text", height=5, width=20, command=self.generateText)
        self.generateButton.pack(side=TOP)
        

    def runGUI(self):
        self.root.mainloop()

    
    def importText(self):
        fname = tkFileDialog.askopenfilename()
        if len(fname) > 0: # prevent file opener from overwriting existing
            self.fileName = fname
            currentFile = "Current File: " + self.fileName
            self.updateStatus()

        
    def updateStatus(self): # update status bar to show current file path
        self.statusBar.configure(text=self.fileName)

        
    def generateText(self):
        try:
            generatedText = self.generate(self.buildChain(self.readFile()))
            self.textBox.delete(1.0, END)
            self.textBox.insert(INSERT, generatedText)
        except:
            tkMessageBox.showinfo('Error', 'Insufficient text data to generate new text')
            self.statusBar.configure(text=self.fileName)
            

    def readFile(self):
        f = open(self.fileName, 'r')
        contents = f.read().replace('\n','').replace('\t', '')
        return self.cleanContents(contents)


    # replace unneeded punctuation from the text
    def cleanContents(self, contents):
        for k in "()[]{}:;'\"\\//-_=+*&^%$#@`~<>|":
            if k in contents:
                contents = contents.replace(k, '')
        return contents


    def buildChain(self, contents, chain = {}):
        contents = contents.split(' ') # get rid of spaces
        punctuation = ['.', '!', '?']
        i = 1 # start at the second word
        for word in contents[i:]:
            # make list of words that follow the current word
            current = contents[i-1]
            if current in chain:
                chain[current].append(word)
            else:
                chain[current] = [word]
            i += 1
        return chain


    def generate(self, chain):
        word = random.choice(chain[self.getStartingWord(list(chain.keys()))])
        message = word.capitalize()
        while (len(message.split(' ')) < self.textLength.get()):
            temp = random.choice(chain[word])
            if self.containsPunct(word): # if previous word was an end word
                temp.capitalize();
            word = temp
            message += ' ' + temp
        #end the rest of the sentence after desired length has been reached
        while (not self.containsPunct(word)):
            temp = random.choice(chain[word])
            word = temp
            message += ' ' + temp
        return message


    def getStartingWord(self, words):
        # only words that follow punctuation are starter words
        starters = []
        for word in words:
            if self.containsPunct(word):
                starters.append(word)
        return random.choice(starters)


    def containsPunct(self, word):
        for p in ['.', '!', '?']:
            if p in word:
                return True
        return False



def main():
    generator = Generator()
    generator.runGUI()

    
if __name__ == "__main__":
    main()





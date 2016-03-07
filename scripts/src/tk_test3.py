from Tkinter import *

class Application(Frame):
    """ A GUI Test  """
    
    def __init__(self, master):
        """ Initialize the Frame """
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        """ Text """
        self.instruction = Label(self, text = "Enter your API key")
        self.instruction.grid(row = 0, column = 0, columnspan = 2, sticky =W)
        
        self.apikey = Entry(self)
        self.apikey.grid(row = 1, column = 1, sticky = W)
        self.submit_button = Button(self, text = "Submit", command = self.reveal)
        self.submit_button.grid(row = 2, column = 0, sticky = W)
        
        self.text = Text(self, width = 35, height = 5, wrap = WORD)
        self.text.grid(row = 3, column = 0, columnspan = 2, sticky = W)
        
    def reveal(self):
        """ display whateves """
        content = self.apikey.get()
        
        if content == "API Key":
            message = "You have access bitch"
        else:
            message = "DENIED BITCH!"
        self.text.delete(0.0, END)
        self.text.insert(0.0, message)

root = Tk()
root.title("API Key")
root.geometry("300x200")
app = Application(root)

root.mainloop()

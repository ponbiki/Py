from Tkinter import *

class Application(Frame):
    """ A GUI Test  """
    
    def __init__(self, master):
        """ Initialize the Frame """
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        """ Movie Widgets Choice """
        Label(self, text = "Choose your favorite movie type").grid(row = 0, column = 0, sticky = W)
        Label(self, text = "Select all that apply:").grid(row = 0, column = 0, sticky = W)
        self.comedy = BooleanVar()
        Checkbutton(self, text = "Comedy", variable = self.comedy, command = self.update_text).grid(row = 2, column = 0, sticky = W)
        self.drama = BooleanVar()
        Checkbutton(self, text = "Drama", variable = self.drama, command = self.update_text).grid(row = 3, column = 0, sticky = W)
        self.romance = BooleanVar()
        Checkbutton(self, text = "Romance", variable = self.romance, command = self.update_text).grid(row = 4, column = 0, sticky = W)
        
        self.result = Text(self, width = 40, height = 5, wrap = WORD)
        self.result.grid(row = 5, column = 0, columnspan = 3)
        
    def update_text(self):
        """ Update widget """
        likes = ""
        
        if self.comedy.get():
            likes += "You like comedy\n"
        if self.drama.get():
            likes += "You like drama\n"
        if self.romance.get():
            likes += "You like romance\n"
        self.result.delete(0.0, END)
        self.result.insert(0.0, likes)
root = Tk()
root.title("Movie Chooser")
app = Application(root)
root.mainloop()
from Tkinter import *

class Application(Frame):
    """ A GUI Test  """
    
    def __init__(self, master):
        """ Initialize the Frame """
        Frame.__init__(self,master)
        self.grid()
        self.button_clicks = 0
        self.create_widgets()
    
    def create_widgets(self):
        """Click counter"""

        self.button = Button(self)
        self.button['text'] = "Total Clicks = 0"
        self.button['command'] = self.update_count
        self.button.grid()
        
    def update_count(self):
        """ Increase the counter """
        self.button_clicks += 1
        self.button['text'] = "Total clicks = " + str(self.button_clicks)

root = Tk()
root.title("3 Buttons Around")
root.geometry("300x150")

app = Application(root)

root.mainloop()

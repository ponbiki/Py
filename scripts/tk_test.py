from Tkinter import *

root = Tk()

root.title("Mass Tool")
root.geometry("300x150")

app = Frame(root)
app.grid()
label = Label(app, text = "Answer Search")
label.grid()

button1 = Button(app, text = "This is a button")
button1.grid()

button2 = Button(app)
button2.grid()
button2.configure(text = "This will show text")

button3 = Button(app)
button3.grid()
button3['text'] = "This will show up too"

root.mainloop()

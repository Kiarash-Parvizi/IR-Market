import stocks.update

def onclick(key = ''):
    global e
    global d
    days = int(d.get())
    string = e.get() 
    print(string)
    # chart
    comLis = stocks.company.load_all()
    for com in comLis:
        if com.name == string:
            com.plot(days)

from tkinter import *
root = Tk()
root.geometry("250x300")
root.title('Grapher')

e = Entry(root)
e.pack()
e.focus_set()

d = Entry(root)
d.insert(END, '20')
d.pack(padx=20, pady=20)
d.focus_set()

root.bind('<Return>', onclick)

b = Button(root,text='chart',command=onclick)
b.pack(side='bottom')
root.mainloop()

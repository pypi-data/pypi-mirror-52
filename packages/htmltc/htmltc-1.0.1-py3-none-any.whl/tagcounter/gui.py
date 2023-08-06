from tkinter import *
from tkinter.messagebox import showinfo
from tagcounter.tagService import TagService


def handler(text, entry):
    try:
        counter = TagService()
        url = entry.get()
        tags = counter.count_tags(url)
        text.delete(1.0, END)
        text.insert(1.0, tags)
    except Exception as error:
        showinfo(title='Exception', message=error)


def start_gui():
    window = Tk()

    button = Button(window, text='Submit', command=lambda: handler(text, entry))
    entry = Entry(width=100)
    text = Text(height=15, wrap=WORD)

    entry.pack()
    button.pack()
    text.pack()

    window.mainloop()



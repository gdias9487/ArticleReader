import tkinter.messagebox
from tkinter import *
import tkinter.scrolledtext as scrolledtext

import pygame.mixer

import articles

global paused
paused = False


# Pause and Unpause The Current Song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


def select_article(event):
    cs = event.widget.curselection()[0]
    if cs:
        index = cs
        data = event.widget.get(index)
        article_app(cs)

    else:
        pass


def wait_file(index):
    if articles.stream(index) is not False:
        return True
    else:
        return tkinter.messagebox.showinfo('Wait', 'The file still being generated!!')


def wait_file1(index):
    if articles.play_article(index) is not False:
        return True
    else:
        return tkinter.messagebox.showinfo('Wait', 'The file still being generated!!')


def main_app():
    title_Font = ('Times New Roman', 20, 'bold')
    default_Font = ('Times New Roman', 15, 'normal')
    window = Tk()
    window.geometry('1280x1000')
    window.title('Article reader')
    window.resizable(False, False)

    frame = Frame(window, width=1280, height=720)
    frame.grid(column=0, row=1)
    frame.grid_propagate(0)
    frame.update()

    frame1 = Frame(window, width=1280, height=120)
    frame1.grid(column=0, row=0)
    text1 = Label(frame1, text='Welcome to the A.R. (Article Reader)')
    text1.place(x=425, y=10)
    text1.config(font=title_Font)

    text2 = Label(frame1, text='Choose an article above to read:')
    text2.place(x=500, y=60)
    text2.config(font=default_Font)

    scrollbar = Scrollbar(frame)

    listbox = Listbox(frame, height=50, width=190)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    scrollbar.config(command=listbox.yview)

    for i in articles.get_all_articles_title():
        listbox.insert(END, i)

    listbox.bind('<Double-1>', select_article)
    window.mainloop()


def article_app(index):
    pygame.mixer.init()
    title_Font = ('Times New Roman', 15, 'bold')
    default_Font = ('Times New Roman', 13, 'bold')
    button_Font = ('Times New Roman', 10, 'bold')
    window = Tk()
    window.geometry('1280x1000')
    window.title(articles.get_article_title_by_index(index))
    window.resizable(False, False)

    frame = Frame(window, width=1280, height=720)
    frame.place(x=100, y=120)
    frame1 = Frame(window, width=1280, height=120)
    frame1.grid(column=0, row=0)

    text1 = Label(frame1, text=articles.get_article_title_by_index(index))
    text1.place(x=100, y=10)
    text1.config(font=title_Font)

    text2 = Label(frame1, text='Wanna hear it?')
    text2.place(x=100, y=70)
    text2.config(font=default_Font)

    button1 = Button(frame1, text='Convert to mp3',
                     command=lambda: articles.hear_article(articles.get_article_text_by_index(index),
                                                           str(index)))
    button1.config(width=11, height=1, background='grey', font=button_Font)
    button1.place(x=230, y=70)


    button3 = Button(frame1, text='Play',
                     command=lambda: wait_file(index))
    button3.config(width=10, height=1, background='grey', font=button_Font)
    button3.place(x=330, y=70)

    button4 = Button(frame1, text='Stop',
                     command=lambda: pause(paused))
    button4.config(width=10, height=1, background='grey', font=button_Font)
    button4.place(x=430, y=70)

    txt = scrolledtext.ScrolledText(frame, undo=True)
    txt.insert(END,
               '\n' + articles.get_article_text_by_index(
                   index))
    txt['font'] = ('Times New Roman', '12')
    txt.pack(side=TOP, expand=True, fill='both')
    txt.config(height=40, width=120)
    window.mainloop()


main_app()

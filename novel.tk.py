'''
Novel Python Application

This program allows users to view a list of novels and add new novels by
getting data from the database. 

Miki Ando
'''
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date

import sqlite3 as sq

con = sq.connect("/Users/MikiAndo/Documents/GitHub/novel-tkinter-project-mando210/novel1.db")
c = con.cursor()

# getting data from the Author table
def get_author():
    res = c.execute("SELECT * from Author")
    # Gets the data from the table
    data = c.fetchall() 
    return data

# getting data from the Novel table
def get_novel():
    res = c.execute("SELECT NovelID, Genre, Title, AuthorName FROM Novel JOIN Author WHERE Novel.AuthorID = Author.AuthorID")
    # Gets the data from the table
    data = c.fetchall() 
    return data

# registers a new consumer for their cosumer ID
def add_novel(isbn, genre, title, authorid):
    ins_str= 'INSERT INTO Novel (ISBN, Genre, Title, AuthorID) VALUES (?,?,?,?)'
    res = c.execute(ins_str, (isbn, genre, title, authorid))
    con.commit()


# VIEW
# main menu with 3 options; View the list of Novel, Add Novel, and Exit
def render_menu():
    window = Tk()
    window.title("Novel Main Menu")
    window.geometry("400x200")

    welcome = Label(window, text = "Welcome to our Book Store", font=('helvetica', 30))
    welcome.pack()

    menuframe = Frame(window)
    menuframe.pack()
    lblmenu = Label(menuframe, text = "Choose an option:", bg = "light blue")
    lblmenu.pack(fill = X)
    
    rpt = Button(menuframe, text="View List of Novels", command = render_novel_list)
    rpt.pack(fill = X, pady=5, padx=10)
    res = Button(menuframe, text="Add a Novel", command = render_add_novel)
    res.pack(fill = X, pady=5, padx=10)
    ext = Button(menuframe, text="Exit", command = lambda:end_program(window))
    ext.pack(fill = X, pady=5, padx=10)
    
    window.mainloop()
    
#ending program
def end_program(w):
    print("\nENDED SYSTEM")
    con.close()
    w.destroy()

#formatting the data by setting borders for each field
def display_column(frame,x,y):
    for i in range(len(x)):
        field = x[i]
        tableVal = Label(frame, text = field, relief = "solid", bd = 1, width = y)
        tableVal.pack()

#creating a table for the fields for attributes
def create_frame_table(canvas):
    frame = Frame(canvas, width = "100", relief = "solid" , bd = 1)
    frame.pack(side = LEFT)
    return frame

# Shows the list of novels in a table format 
def render_novel_list():
    novel_win = Tk()
    novel_win.title("Novel List")
    novel_win.geometry("700x300")
    
    title = Label(novel_win, text = "Novel List")
    title.config(font=('helvetica', 30))
    title.pack()

    table = Canvas(novel_win)
    table.pack()

    #creates for frames for each column
    nvlframe = create_frame_table(table)
    greframe = create_frame_table(table)
    ttlframe = create_frame_table(table)
    atnframe = create_frame_table(table)
    
    novel = get_novel()
    nid = ["Novel ID"] 
    gre = ["Genre"]
    ttl = ["Title"]
    aut = ["Author Name"]

    # gets each field in the row and sorts which column they are in
    n = 1
    for row in novel:
        n = row[0]
        g = row[1]
        tt = row[2]
        an = row[3]
        
        nid.insert(n, n)
        gre.insert(n, g)
        ttl.insert(n, tt)
        aut.insert(n, an)
        n += 1

    # organizing the table by column
    novel = display_column(nvlframe, nid, "10")
    title = display_column(ttlframe,ttl, "20")
    genre = display_column(greframe,gre, "20")
    authorname = display_column(atnframe,aut, "20")
    
    novel_win.mainloop()

# Shows the list of authors 
def author_listbox(w,f,authors):
    lblauthor = Label(f, text = "Author ID, Name, Nationality").pack(side = TOP)

    Lb = Listbox(f, height = 6, width = 26,font=('helvetica', 12), exportselection = False) 
    Lb.pack(side = TOP, fill = Y)
                
    scroll = Scrollbar(w, orient = VERTICAL) # set scrollbar to list box for when entries exceed size of list box
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set)
    
    i = 0
    for author in authors:
        Lb.insert(i, author)
        i += 1
    Lb.selection_set(first = 0)

    return Lb

# checks if the entry is valid and if it is valid, it adds the novel in the database
def check_and_enter_selection(ib, g, tt, aid):
    if len(ib) == 0 or len(g) == 0 or len(tt) == 0:
        messagebox.showinfo("Error Try Again" , "ERROR: There were empty values")
    elif (not ib.isdigit()) or (g.isdigit()):
        messagebox.showinfo("Error Try Again", "ERROR: Invalid Values")
    elif (len(ib) < 13) or (len(ib) > 13):
        messagebox.showinfo("Error Try Again", "ERROR: ISBN should be 13 digits")
    else:
        add_novel(ib, g, tt, aid)
        messagebox.showinfo("Success", "SUCCESS: The novel has been added")

# Adds new novels by asking for user entry and letting users choose the author
def render_add_novel():
    add_req_win = Tk()
    add_req_win.title("Add Novel")
    add_req_win.geometry("400x400")

    entry_frame = Frame(add_req_win)
    entry_frame.pack(side = LEFT)

    ib = tk.StringVar(add_req_win)
    g = tk.StringVar(add_req_win)
    tt = tk.StringVar(add_req_win)

    option_frame = Frame(add_req_win)
    option_frame.pack(side = RIGHT)

    authors = get_author()
    authorlb = author_listbox(add_req_win, option_frame, authors)

    #isbn - user entry
    lbl = Label(entry_frame, text = "Add a new novel", font = ('helvetica', 25), bg = "light blue").pack(pady = 5)
    lblib = Label(entry_frame, text = "ISBN (13digits)").pack()
    isbn = Entry(entry_frame, textvariable = ib).pack(padx = 5)

    #genre - user entry
    lblg = Label(entry_frame, text = "Genre").pack()
    genre = Entry(entry_frame, textvariable = g).pack(padx = 5)

    #title - user entry
    lbltt = Label(entry_frame, text = "Title").pack()
    title = Entry(entry_frame, textvariable = tt).pack(padx = 5)

    # the entry button 
    rpt = Button(entry_frame, text="Add Novel",
                 command = lambda: check_and_enter_selection(ib.get(), g.get(), tt.get(),
                            authors[authorlb.curselection()[0]][0])).pack(pady=10)
 
    add_req_win.mainloop()
 
# Start here: loop the main menu until the user choses the exit option
while(render_menu()):
    print("\n\nWelcome to our Book Store")

'''
ins_str= 'DELETE FROM Novel WHERE NovelID > 4'
res = c.execute(ins_str)
con.commit()'''

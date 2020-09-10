def fdbk():
    
    import tkinter
    from tkinter import ttk

    globals()['master'] = tkinter.Tk()
    
    master.title(':)')
    frame_header = ttk.Frame(master)#header frame
    frame_header.pack()
        
    ttk.Label(frame_header).grid(row = 0, column = 1)
    ttk.Label(frame_header, text = "Thanks for trusting this system!").grid(row = 1, column = 1)
    ttk.Label(frame_header, 
              text = "If you have a moment, we'd love to hear any of your feedback!", 
              justify = 'center').grid(row = 2, column = 1)
    ttk.Label(frame_header, 
              text = "It would be beyond helpful to us in terms of our application's improvement!", 
              justify = 'center').grid(row = 3, column = 1, padx=15)
    ttk.Label(frame_header).grid(row = 4, column = 1)

    frame_content = ttk.Frame(master)
    frame_content.pack()
    
    ttk.Label(frame_content, text = 'Anonymous Comments:').grid(row = 5, column = 0, padx = 5, sticky = 'sw')
    text_comments = tkinter.Text(frame_content, width = 50, height = 10, font = ('Arial', 10))
    text_comments.grid(row = 6, column = 0, columnspan = 2, padx = 5)
    
    def submit():

        import sqlite3
        conn = sqlite3.connect("Feedback.db")
        #conn.cursor().execute("""CREATE TABLE IF NOT EXISTS feedback (id integer PRIMARY KEY, comment text);""")
        conn.cursor().execute("""INSERT INTO feedback(id, comment) VALUES(NULL, ?)""", (text_comments.get(1.0, 'end'),))
        conn.commit(); conn.close();
        
        master.quit(); master.destroy();
        from tkinter import messagebox, Tk
        Tk().withdraw(); messagebox.showinfo(title = ":)", message = "Feedback Submitted! Thanks a lot!")
    
    ttk.Button(frame_content, text = 'Submit', command = submit).grid(row = 7, column = 0, pady = 15, sticky = 'w')
    def end(): master.quit(); master.destroy()
    ttk.Button(frame_content, text = 'Cancel', command=end).grid(row = 7, column = 1, pady = 15, sticky = 'e')
    
    master.mainloop()
    
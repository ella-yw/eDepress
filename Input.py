def input_params():
    
    import tkinter

    def fetch(entries):
    
            #for entry in range(len(entries)): print('%s: "%s"' % (entries[entry][0], entries[entry][1].get()))
            
            globals()['ig_username'] = entries[0][1].get()
            globals()['tw_username'] = entries[1][1].get()
            
            root.quit(); root.destroy()
    
    def makeform(root, fields):
       
       row = tkinter.Frame(root)
       
       l = tkinter.Label(root, text='ENTER CREDENTIALS:', font=("Arial ", 25, "bold"))
       l.place(x = 20, width=120, height=25); l.pack(pady=5)
       
       tkinter.Radiobutton(root, text="Explicit subject consent recieved to access + analyze private data", padx = 20).pack(anchor=tkinter.W)
       tkinter.Radiobutton(root, text="No subject permission given", padx = 20, variable=tkinter.StringVar(root), state='disabled').pack(anchor=tkinter.W)
       
       row = tkinter.Frame(root); row.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)
       
       entries = []
       for field in fields:
          
          row = tkinter.Frame(root); row.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)
          
          tkinter.Label(row, width=18, text=field, anchor='w').pack(side=tkinter.LEFT)
          entry = tkinter.Entry(row); entry.pack(side=tkinter.RIGHT, expand=tkinter.YES, fill=tkinter.X)
          
          entries.append((field, entry))
       
       return entries
       
    def main():
        
       globals()['root'] = tkinter.Tk()
        
       fields = ['Instagram Username', 'Twitter Handle']
        
       ents = makeform(root, fields)
       
       root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
       
       b1 = tkinter.Button(root, text='Submit', width=18, fg='black', command=(lambda e=ents: fetch(e)))
       b1.pack(side=tkinter.TOP, padx=20, pady=10)
       
       root.mainloop()
    
    main()
    
    return ig_username, tw_username
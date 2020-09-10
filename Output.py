def output_params(results, demo_purposes_no_internet):

    import datetime, csv
            
    outputs = ["NO DEPRESSION RISK FOUND", 
               "MILD (SITUATIONAL) DEPRESSION RISK FOUND", 
               "MODERATE (SEASONALLY PERSISTENT) DEPRESSION RISK FOUND", 
               "MAJOR DEPRESSION RISK FOUND"]
    synopses = [
        """You have no signs of clinical depression/depressive disorder""", 
        """Situational depression is a short-term, stress-related 
        type of depression. Primarily you feel mildly depressed, 
        although you may have brief periods of normal mood. 
        The symptoms are not as strong as the symptoms of major 
        depression, but they can still last a long time. It can develop 
        after you experience a traumatic event or series of events.""", 
        """In terms of symptomatic severity, moderate depression is
        the next level up from mild cases. Moderate depression may cause
        problems with your self-esteem, and reduced productivity.""", 
        """Clinical depression is the more-severe form of depression, 
        also known as major depression or major depressive disorder.
        Patients should immediately be provided with further resources, 
        and potentially referred to psychiatry, as well as be screened for
        emergency psychiatric conditions like suicidal ideation or psychosis."""
    ]
    
    if results < 2: output = outputs[0]; synopsis = synopses[0]; 
    elif results >= 2 and results < 4: output = outputs[1]; synopsis = synopses[1]; 
    elif results >= 4 and results < 6: output = outputs[2]; synopsis = synopses[2]; 
    elif results >= 6: output = outputs[3]; synopsis = synopses[3]; 
    
    current_date = str(datetime.datetime.now()).split(".")[0]
    
    #print(output); print("Major Depression Index (MDI): " + str(results) + "%"); print("As of last scan @ " + current_date)
    
    if not demo_purposes_no_internet:
        with open("Out.csv", "a", newline="") as fp: 
            csv.writer(fp).writerow([output, str(results), current_date])
    resultss = []
    for i in list(csv.reader(open("Out.csv", "r", newline=""))): resultss.append(float(i[1]))
    avg_results = sum(resultss)/len(resultss)
    
    #wb.register('chrome', None, wb.BackgroundBrowser("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"), 1)
    #wb.get("chrome").open_new_tab("file:///"+os.path.join(os.getcwd(), "results.html")+"?output="+str(output)+"&confidence="+str(results)+"&dateTime="+current_date)    
            
    import tkinter

    globals()['window'] = tkinter.Tk()
    window.title("Derived Output")
     
    row = tkinter.Frame(window); row.pack(side=tkinter.TOP, fill=tkinter.X, pady=10, padx=20)
    lbl = tkinter.Label(row, text=output, font=("Arial Bold", 25)).pack(side=tkinter.TOP)
    
    row = tkinter.Frame(window); row.pack(side=tkinter.TOP, fill=tkinter.X, pady=10, padx=30)
    lbl = tkinter.Label(row, text=synopsis, font=("Arial", 13)).pack(side=tkinter.TOP)
    
    row = tkinter.Frame(window); row.pack(side=tkinter.TOP, fill=tkinter.X, pady=10)
    lbl2 = tkinter.Label(row, text="Major Depression Index (MDI):", font=("Arial", 13)).pack(side=tkinter.TOP)
    lbl2 = tkinter.Label(row, text=str(results), font=("Arial Bold", 18), anchor='w').pack(side=tkinter.TOP)
    
    row = tkinter.Frame(window); row.pack(side=tkinter.TOP, fill=tkinter.X, pady=10)
    lbl2 = tkinter.Label(row, text="Long-Term Averaged MDI:", font=("Arial", 13)).pack(side=tkinter.TOP)
    lbl2 = tkinter.Label(row, text=str(avg_results), font=("Arial Bold", 18), anchor='w').pack(side=tkinter.TOP)
    
    row = tkinter.Frame(window); row.pack(side=tkinter.TOP, fill=tkinter.X, pady=10)
    lbl3 = tkinter.Label(row, text="As of last scan @ " + current_date, font=("Arial italic", 9)).pack(side=tkinter.TOP)
    
    row = tkinter.Frame(window); row.pack(side=tkinter.TOP, fill=tkinter.X, pady=10)
    def end(): window.quit(); window.destroy()
    b1 = tkinter.Button(row, text='Okay great!', font=("Arial Bold", 13), width=18, bg='black', fg='white', command=end).pack(side=tkinter.TOP)
    
    window.mainloop()
        
    return
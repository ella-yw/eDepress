from PIL import Image, ImageTk; import tkinter
root = tkinter.Tk(); root.title("eDepress")
img = Image.open("Logo.png"); img = img.resize((500, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img); panel = tkinter.Label(root, image=img)
panel.image = img; panel.pack();
root.after(5000, lambda: root.destroy()); root.mainloop()

demo_purposes_no_internet = True

from Input import input_params
ig_username, tw_username = input_params() #JohnDoe41741061 (for IG & FB)
from tkinter import messagebox, Tk
Tk().withdraw(); messagebox.showinfo(":)", "The system will now begin extracting and parsing the data!")

if demo_purposes_no_internet:
    import time; time.sleep(7)
else:    
    from Retriever import retrieve
    retrieve(ig_username, tw_username)

from tkinter import messagebox, Tk
Tk().withdraw(); messagebox.showinfo(":)", "The system has finished mining the data! It will now begin applying pre-trained AI models to analyze this data!")

from Analyzer import analyze
results = analyze()

if results != "nothing_new":
    from Output import output_params
    from tkinter import messagebox, Tk
    Tk().withdraw(); messagebox.showinfo(":)", "The system has finished analyzing the data! It will now compute the user's results!")
    output_params(results, demo_purposes_no_internet)
    from Feedback import fdbk; fdbk(); 
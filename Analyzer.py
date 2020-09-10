def analyze():
    
    from keras.models import load_model
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    import glob, datetime, numpy as np, csv, keras, cv2
    from skimage import transform
    
    #print("Loading All Data...", end='')
    
    text = []; blurb = []; picture = []; video = [];
    
    sheets = ["ig/ig_data.csv", "tw/tw_data.csv", "fb/fb_data.csv"]
    
    picture_extensions = {".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".gif"}
    video_extensions = {".mp4", ".mp3", ".avi", ".mov", ".3gp", ".flv", ".wmv", ".webm", ".ogg", ".m4a", ".3gp2"}
    
    dates = []
    for row in csv.reader(open("Out.csv", "r")):
        dates.append(datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'))
    prev_last_date = dates[-1]
    
    for sheet in sheets:
        try:
            for record in list(csv.reader(open(sheet, "r", encoding="utf-8"))):
                if datetime.datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S') > prev_last_date: 
                    entity = sheet.split("/")[0]
                    if entity == "ig" or entity == "tw" or entity == "fb": 
                        text.append(record[2])
                        if record[-1] == 'True':
                            file = glob.glob(entity + '/' + record[0] + '*', recursive=True)[0]
                            if any(file.endswith(ext) for ext in picture_extensions): picture.append(file)
                            elif any(file.endswith(ext) for ext in video_extensions): video.append(file)
                            elif file.endswith(".txt"): blurb.append(file)
        except FileNotFoundError: pass
    
    #print("DONE\n")
    
    #print("Analyzing All Data...", end='')
    
    keras.backend.clear_session()
    text_model = load_model("AI/text_model.hdf5")
    
    results = []
    
    for sentence in text:
        if sentence != "":
            
            sentence = [sentence]            
            
            t = Tokenizer(); t.fit_on_texts(sentence)
            sentence = pad_sequences(sequences=t.texts_to_sequences(sentence), maxlen=500)
               
            outputs = text_model.predict(sentence)
            results.append(np.argmax(np.array(outputs).flatten()))
    
    keras.backend.clear_session()
    image_model = load_model("AI/image_model.hdf5")
    
    img_size = 64
    
    for pic in picture:
        if pic != "":
            
            image = transform.resize(cv2.imread(pic), (img_size, img_size), mode='constant')
            image = image.reshape(1, image.shape[0], image.shape[1], 3)
                
            image = np.array(image).astype(np.float)
               
            outputs = image_model.predict(image)
            results.append(np.argmax(np.array(outputs).flatten()))
    
    #print("DONE\n")
    
    try:
        #CLASSES: DEPRESSION = 0; NORMAL = 1;
        prob_of_depression = 100-(sum(results)/len(results)*100)
        return prob_of_depression
    except ZeroDivisionError:
        from tkinter import messagebox, Tk
        Tk().withdraw(); messagebox.showwarning("¯\_(ツ)_/¯", "The system has nothing new/recent to analyze!")
        return "nothing_new"
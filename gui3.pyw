import os
import sys
import threading
import youtube_dl
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory


r,w = os.pipe()
sys.stdout = os.fdopen(w, 'w')

downloading = False

def download():
    def func():
        global downloading
        if not downloading:
            with youtube_dl.YoutubeDL({'format': formt.get()}) as ydl:
                link = re.findall('^https://www.youtube.com/watch[?]v=[^&]+', inp.get())
                if link:
                    text.delete(1.0, END)
                    downloading = True
                    ydl.download(link)
                    downloading = False
                print('***DOWNLOAD DONE***')
        else:
            print('******DO NOT INTURRUPT CURRENT DOWNLOAD*******')
    threading.Thread(target=func).start()  

            
def file_save():
    os.chdir((askdirectory()))
    directory.set('Save to: ' + os.getcwd())
 

def printer(r, bytes):
    string = ''
    while True:
        string = os.read(r, bytes).decode()
        text.insert(INSERT, string)


def flusher():
    while True:
        sys.stdout.flush()




root = Tk()
root.title('Youtube Downloader')
# root.iconbitmap('black-tube.ico')
frame = Frame(root)
frame.pack(expand=YES, fill=BOTH)
frame.config(bg='#8b0000')

frame_1 = Frame(root)
frame_2 = Frame(root)
frame_1.pack(expand=YES, fill=BOTH)
frame_1.config(bg='#8b0000')
frame_2.config(bg='#8b0000')
frame_2.pack(expand=YES, fill=BOTH)



inp = StringVar()
inp.set('')
directory = StringVar()
directory.set('Save to: ' + os.getcwd())
formt = StringVar()
formt.set('best')


font = ('robot', 12, 'bold')

Label(frame, text="Youtube Downloader", font=font).pack(side=TOP, pady=10)
ttk.Label(frame, text='Enter a Link', font=font).pack(side=LEFT, pady=10)
entry = Entry(frame, textvariable=inp, width=50, font=font, bg='black', fg='green')
entry.pack(side=LEFT, pady=10)
Label(frame_1, text='quality', font=font).pack(side=LEFT)
ttk.Combobox(frame_1, values=['best', 'worst', 'bestaudio',  'worstaudio'], state='readonly', font=font, textvariable=formt).pack(side=LEFT)


ttk.Label(frame_2, textvariable=directory, font=font).pack(expand=YES, fill=X, pady=10)
text = Text(frame_2, width=50, bg='black', fg='green')
text.pack()
ttk.Button(frame_2, text='Download', command=download).pack(side=LEFT, expand=YES, fill=BOTH)
ttk.Button(frame_2, text='Browse', command=file_save).pack(side=LEFT, expand=YES, fill=BOTH)


t2 = threading.Thread(target=printer, args=(r, 5))
t2.daemon = True
t2.start()
t3 = threading.Thread(target=flusher)
t3.daemon = True
t3.start()

mainloop()
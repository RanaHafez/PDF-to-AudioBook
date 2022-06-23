from gtts import gTTS
import PyPDF2
import tkinter as tk
from tkinter import filedialog as fd
import pygame
from tkinter.messagebox import showinfo

HEADING_FONT = ("Comic Sans MS", 15, "bold")
BUTTONS_FONT = ("Comic Sans MS", 9, "bold")
BACKGROUND_COLOR = '#DAEAF1'
BUTTONS_BACKGROUND = "#F2D1D1"
BUTTONS_FOREGROUND = "#748DA6"

def open_file():
    file_name = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[("PDF File" ,".pdf")],
    )
    return file_name


def get_file():
    file_name = open_file()
    convert_to_mp3(file_name)


def convert_to_mp3(file_name):
    try:
        global saved_mp3
        # loading_indicator.grid(row=2, column=0)
        path = open(file_name, 'rb')
        pdfreader = PyPDF2.PdfFileReader(path)
        new_name = file_name[:-4]

        cleaned_text = ""
        for page_num in range(pdfreader.numPages):
            text = pdfreader.getPage(page_num).extractText()
            cleaned_text += text.strip().replace('\n', ' ')


        saved_mp3 = f"{new_name}.mp3"
        obj = gTTS(text=cleaned_text)
        obj.save(saved_mp3)
        # loading_indicator.config(text="Done Loading")
        play_audio.grid(row=2, column=1)
    except FileNotFoundError:
        showinfo(
            title="File Not Found",
            message=f"{file_name} is not found. Try Again Later."
        )


def play():
    print(saved_mp3)
    pygame.init()
    pygame.mixer.music.load(saved_mp3)
    pygame.mixer.music.play()
    pause_audio.grid(row=2, column=2)
    stop_audio.grid(row=2, column=3)
    unpause_audio.grid(row=2, column=4)


def pause():
    pygame.mixer.music.pause()


def stop():
    pygame.mixer.music.stop()


def unpause():
    pygame.mixer.music.unpause()


window = tk.Tk()
window.title("PDF to MP3")
window.geometry("800x400")
window.config(bg='#DAEAF1', padx=50, pady=50)


canvas = tk.Canvas(width=250, height=250)
photo = tk.PhotoImage(file='waves.png')
canvas.create_image(110, 110, image=photo)
canvas.config(bg= BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=2, column=0, columnspan=2)

label = tk.Label(
    text="Convert your PDF to MP3", bg=BACKGROUND_COLOR, fg="#748DA6", font=HEADING_FONT)

label.grid(row=1, column=0)

file_button = tk.Button(
    text="Open PDF",
    bg=BUTTONS_BACKGROUND,
    fg=BUTTONS_FOREGROUND,
    command=get_file,
    font=BUTTONS_FONT
)

file_button.grid(row=3, column=0)

play_audio = tk.Button(
    text="▶️Play",
    bg=BUTTONS_BACKGROUND,
    fg=BUTTONS_FOREGROUND,
    font=BUTTONS_FONT,
    command=play, padx=20)

pause_audio = tk.Button(
    text="⏸️Pause",
    bg=BUTTONS_BACKGROUND,
    fg=BUTTONS_FOREGROUND,
    font=BUTTONS_FONT,
    command=pause,
    padx=20
)

stop_audio = tk.Button(text="⏹️Stop", bg=BUTTONS_BACKGROUND, fg=BUTTONS_FOREGROUND,
                       font=BUTTONS_FONT, command=stop, padx=20)

unpause_audio = tk.Button(text="⏯️Continue", bg=BUTTONS_BACKGROUND, fg=BUTTONS_FOREGROUND,
                          font=BUTTONS_FONT, command=unpause, padx=20)

window.mainloop()

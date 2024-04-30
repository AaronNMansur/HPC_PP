from tkinter import *
import pygame
from tkinter import filedialog
import os
import time
from mutagen.mp3 import MP3

root = Tk()
root.title('Mp3 Player')
root.iconbitmap('')
root.geometry('500x400')


def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000

    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    current_song = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song = f'C:/Users/JeepK/PyCharmProjects/HPC_PP/songs/{song}.mp3'

    status_bar.config(text=f'Time Elapsed: {converted_current_time}')

    status_bar.after(1000, play_time)


bg_color = 'white'  # Dark background color
fg_color = 'white'  # Light text color
highlight_color = '#1E90FF'  # Light blue for selection

root.config(bg=bg_color)

pygame.mixer.init()


def add_song():
    song_path = filedialog.askopenfilename(initialdir='audio/', title='Choose A Song',
                                           filetypes=(('mp3 Files', '*.mp3'),))
    if song_path:
        song_name = os.path.basename(song_path).replace('.mp3', '')
        song_box.insert(END, song_name)


def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose A Song', filetypes=(('mp3 Files', '*.mp3'),))
    for song in songs:
        song_name = os.path.basename(song).replace('.mp3', '')
        song_box.insert(END, song_name)


def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/JeepK/PyCharmProjects/HPC_PP/songs/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()


def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)


def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song = f'C:/Users/JeepK/PyCharmProjects/HPC_PP/songs/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


def previous_song():
    back_one = song_box.curselection()
    back_one = back_one[0] - 1
    song = song_box.get(back_one)
    song = f'C:/Users/JeepK/PyCharmProjects/HPC_PP/songs/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(back_one)
    song_box.selection_set(back_one, last=None)


def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()


global paused
paused = False


def pause():
    global paused
    paused = not paused

    if paused:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

master_frame = Frame(root)
master_frame.pack(pady=20)

song_box = Listbox(master_frame, bg='black', fg='green', width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

back_btn = PhotoImage(file='images/BackPP.png')
forward_btn = PhotoImage(file='images/ForwardPP.png')
play_btn = PhotoImage(file='images/PlayPP.png')
pause_btn = PhotoImage(file='images/PausePP.png')
stop_btn = PhotoImage(file='images/StopPP.png')

controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0)

volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=20)

back_button = Button(controls_frame, image=back_btn, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn, borderwidth=0, command=pause)
stop_button = Button(controls_frame, image=stop_btn, borderwidth=0, command=stop)

back_button.grid(row=0, column=3)
forward_button.grid(row=0, column=4)
play_button.grid(row=0, column=0)
pause_button.grid(row=0, column=1)
stop_button.grid(row=0, column=2)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add One Song To Playlist', command=add_song)

add_song_menu.add_command(label='Add Many Songs To Playlist', command=add_many_song)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Remove One Song From Playlist')
remove_song_menu.add_command(label='Remove Many Songs From Playlist')

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

volume_slider = Scale(volume_frame, from_=0, to=1, orient=VERTICAL, command=volume, length=125, resolution=0.01)
volume_slider.pack(pady=10)



root.mainloop()

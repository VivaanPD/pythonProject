import os.path
from customtkinter import *
from pytube import YouTube
from tkinter.messagebox import showerror
from pathlib import Path
import threading
import subprocess
import http.client as httplib

set_appearance_mode('dark')
set_default_color_theme('blue')

win = CTk()
win.title('YouTube to MP4')
win.geometry('500x400')
win.resizable(False, False)


tabview = CTkTabview(win, width=500, height=400)
tabview.pack(padx=0, pady=0)

tabview.add('Download')
tabview.add('Merge')
tabview.set('Download')

top_frame = CTkFrame(tabview.tab('Download'), corner_radius=5, fg_color='#434854')
top_frame.pack(pady=10)

link_entry = CTkEntry(top_frame, placeholder_text='Enter YouTube Link Here', width=350)
link_entry.grid(row=0, column=1, padx=10, pady=10)

bottom_frame = CTkFrame(tabview.tab('Download'), corner_radius=5, width=400)
bottom_frame.pack(pady=10)


def have_internet():
    conn = httplib.HTTPSConnection('8.8.8.8', timeout=5)
    try:
        conn.request('HEAD', '/')
        return True
    except Exception:
        return False
    finally:
        conn.close()


def download_template_for_all(resolution):
    global link_entry
    internet_connection = have_internet()
    if internet_connection is True:
        youtube = YouTube(str(link_entry.get().replace(" ", "")))
        title = youtube.title
        output_file = os.path.join(str(Path.home() / "Downloads"), f'{resolution}__{title.replace(" ", "_")}.mp4')
        if os.path.exists(output_file):
            dialog = CTkInputDialog(title='Already Exists', text='This File Already Exists. Do You Want To'
                                                                 ' Override? ONLY ANSWER WITH YES IF YOU WANT TO'
                                                                 ' PRESS CANCEL IF YOU DO NOT')
            if dialog.get_input().replace(" ", "").lower() == 'yes':
                try:
                    required_audio_stream = youtube.streams.filter(only_audio=True).order_by('abr').desc().first()
                    downloading_label.configure(text='Downloading... please wait')
                    downloading_label.pack()
                    required_video_stream = youtube.streams.filter(resolution=resolution,
                                                                   file_extension='mp4',
                                                                   progressive=False).order_by('resolution').desc().first()
                    try:
                        location_video = required_video_stream.download(max_retries=100, filename_prefix=f'{resolution}_',
                                                                        output_path=str(Path.home() / 'Downloads'),
                                                                        filename=f'{title.replace(" ", "_")}.mp4')

                        location_audio = required_audio_stream.download(max_retries=100, filename_prefix='audio_',
                                                                        output_path=str(Path.home() / "Downloads"),
                                                                        filename=f'{title.replace(" ", "_")}.webm')
                        os.remove(output_file)
                        codec = 'copy'
                        subprocess.run(f'ffmpeg -i {location_video} -i {location_audio} -c {codec} {output_file}')
                        os.remove(location_video)
                        os.remove(location_audio)
                        downloading_label.configure(text='Download Complete')
                        location_textbox.configure(state='normal')
                        location_textbox.insert(END, f'The Location of Your Video File is: {output_file}\n\n')
                        location_textbox.pack(pady=10)
                        location_textbox.configure(state='disabled')
                        three_sixty_p.configure(state='normal')
                        four_eighty_p.configure(state='normal')
                        seven_twenty_p.configure(state='normal')
                        ten_eighty_p.configure(state='normal')
                    except:
                        three_sixty_p.configure(state='normal')
                        four_eighty_p.configure(state='normal')
                        seven_twenty_p.configure(state='normal')
                        ten_eighty_p.configure(state='normal')
                        showerror(title='Invalid', message='No Streams For This Resolution Found')
                except:
                    three_sixty_p.configure(state='normal')
                    four_eighty_p.configure(state='normal')
                    seven_twenty_p.configure(state='normal')
                    ten_eighty_p.configure(state='normal')
                    showerror(title='UNAVAILABLE VIDEO', message='THE VIDEO YOU ARE TRYING TO DOWNLOAD IS UNAVAILABLE')
            else:
                three_sixty_p.configure(state='normal')
                four_eighty_p.configure(state='normal')
                seven_twenty_p.configure(state='normal')
                ten_eighty_p.configure(state='normal')
                dialog.destroy()
        else:
            try:
                required_audio_stream = youtube.streams.filter(only_audio=True).order_by('abr').desc().first()
                downloading_label.configure(text='Downloading... please wait')
                downloading_label.pack()
                required_video_stream = youtube.streams.filter(resolution=resolution,
                                                               file_extension='mp4',
                                                               progressive=False).order_by('resolution').desc().first()
                try:
                    location_video = required_video_stream.download(max_retries=100, filename_prefix=f'{resolution}_',
                                                                    output_path=str(Path.home() / 'Downloads'),
                                                                    filename=f'{title.replace(" ", "_")}.mp4')

                    location_audio = required_audio_stream.download(max_retries=100, filename_prefix='audio_',
                                                                    output_path=str(Path.home() / "Downloads"),
                                                                    filename=f'{title.replace(" ", "_")}.webm')
                    codec = 'copy'
                    subprocess.run(f'ffmpeg -i {location_video} -i {location_audio} -c {codec} {output_file}')
                    os.remove(location_video)
                    os.remove(location_audio)
                    downloading_label.configure(text='Download Complete')
                    location_textbox.configure(state='normal')
                    location_textbox.insert(END, f'The Location of Your Video File is: {output_file}\n\n')
                    location_textbox.pack(pady=10)
                    location_textbox.configure(state='disabled')
                    three_sixty_p.configure(state='normal')
                    four_eighty_p.configure(state='normal')
                    seven_twenty_p.configure(state='normal')
                    ten_eighty_p.configure(state='normal')
                except:
                    three_sixty_p.configure(state='normal')
                    four_eighty_p.configure(state='normal')
                    seven_twenty_p.configure(state='normal')
                    ten_eighty_p.configure(state='normal')
                    showerror(title='Invalid', message='No Streams For This Resolution Found')
            except:
                three_sixty_p.configure(state='normal')
                four_eighty_p.configure(state='normal')
                seven_twenty_p.configure(state='normal')
                ten_eighty_p.configure(state='normal')
                showerror(title='UNAVAILABLE VIDEO', message='THE VIDEO YOU ARE TRYING TO DOWNLOAD IS UNAVAILABLE')
    else:
        three_sixty_p.configure(state='normal')
        four_eighty_p.configure(state='normal')
        seven_twenty_p.configure(state='normal')
        ten_eighty_p.configure(state='normal')
        showerror(title='NO INTERNET', message='CONNECT TO INTERNET BEFORE ATTEMPTING DOWNLOAD')


def three_sixty():
    three_sixty_p.configure(state='disabled')
    four_eighty_p.configure(state='disabled')
    seven_twenty_p.configure(state='disabled')
    ten_eighty_p.configure(state='disabled')
    download_template_for_all(resolution='360p')


def three_sixty_thread():
    threading.Thread(target=three_sixty).start()


def four_eighty():
    three_sixty_p.configure(state='disabled')
    four_eighty_p.configure(state='disabled')
    seven_twenty_p.configure(state='disabled')
    ten_eighty_p.configure(state='disabled')
    download_template_for_all(resolution='480p')


def four_eighty_thread():
    threading.Thread(target=four_eighty).start()


def seven_twenty():
    three_sixty_p.configure(state='disabled')
    four_eighty_p.configure(state='disabled')
    seven_twenty_p.configure(state='disabled')
    ten_eighty_p.configure(state='disabled')
    download_template_for_all(resolution='720p')


def seven_twenty_thread():
    threading.Thread(target=seven_twenty).start()


def ten_eighty():
    three_sixty_p.configure(state='disabled')
    four_eighty_p.configure(state='disabled')
    seven_twenty_p.configure(state='disabled')
    ten_eighty_p.configure(state='disabled')
    download_template_for_all(resolution='1080p')


def ten_eighty_thread():
    threading.Thread(target=ten_eighty).start()


three_sixty_p = CTkButton(bottom_frame, text='360p', width=100, command=three_sixty_thread)
three_sixty_p.grid(row=0, column=0, padx=10, pady=10)

four_eighty_p = CTkButton(bottom_frame, text='480p', width=100, command=four_eighty_thread)
four_eighty_p.grid(row=0, column=1, padx=10, pady=10)

seven_twenty_p = CTkButton(bottom_frame, text='720p', width=100, command=seven_twenty_thread)
seven_twenty_p.grid(row=0, column=2, padx=10, pady=10)

ten_eighty_p = CTkButton(bottom_frame, text='1080p', width=100, command=ten_eighty_thread)
ten_eighty_p.grid(row=0, column=3, padx=10, pady=10)

location_textbox = CTkTextbox(tabview.tab('Download'), width=450, height=180, wrap=WORD)
location_textbox.configure(font=('helvetica', 13))
location_textbox.configure(state='disabled')

downloading_label = CTkLabel(tabview.tab('Download'))

win.mainloop()



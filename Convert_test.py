from customtkinter import *
import os
from tkinter import filedialog
from pathlib import Path
import convertapi
from tkinter import messagebox
import threading

convertapi.api_secret = 'i66kt1TsvpWM3R13'

set_default_color_theme('dark-blue')
set_appearance_mode('default')

root = CTk()
root.geometry('600x600')
root.title('PDF and Word converter')

home_path = str(Path.home())

frame_for_input_buttons = CTkFrame(master=root, corner_radius=10, fg_color='#434854')
frame_for_input_buttons.pack(pady=30)

frame_for_conversion = CTkFrame(master=root, corner_radius=10, fg_color='#434854')

frame_for_the_rest = CTkFrame(master=root, corner_radius=10, fg_color='#434854')

combobox = CTkOptionMenu(master=frame_for_input_buttons, values=["Word (*.docx)", "PDF (*.pdf)", "JPG (*.jpg)"])
combobox.pack(padx=20, pady=10)
combobox.set("Which type of file do you want to convert? Default is all types (*.*)")  # set initial value

frame_for_textbox = CTkFrame(master=root, corner_radius=10, fg_color='#434854')

textbox = CTkTextbox(master=frame_for_textbox, height=50, width=400)

sv = StringVar(value='Select your filetype')


def callback(choice):
    if choice != "":
        btn_for_conversion.pack(padx=20, pady=10)


combobox2 = CTkOptionMenu(master=frame_for_conversion, values=["Word (*.docx)", "PDF (*.pdf)"], variable=sv,
                          command=callback)

rootfile = ""


def choose_file():
    global rootfile
    if str(combobox.get()) == "PDF (*.pdf)":
        rootfile = filedialog.askopenfilename(initialdir=f'{home_path}\Desktop',
                                              filetypes=(("PDF Files", "*.pdf"), ("all files", "*.*")))
    elif str(combobox.get()) == "Word (*.docx)":
        rootfile = filedialog.askopenfilename(initialdir=f'{home_path}\Desktop',
                                              filetypes=(("Word Files", "*.docx"), ("all files", "*.*")))
    elif str(combobox.get()) == "JPG (*.jpg)":
        rootfile = filedialog.askopenfilename(initialdir=f'{home_path}\Desktop',
                                              filetypes=(("JPG files", "*.jpg"), ("all files", "*.*")))
    else:
        rootfile = filedialog.askopenfilename(initialdir=f'{home_path}\Desktop')
    getting_filename = os.path.basename(rootfile)
    if getting_filename != "":
        frame_for_textbox.pack(pady=20)
        frame_for_conversion.pack(pady=20)
        textbox.pack(padx=10, pady=15)
        combobox2.pack(padx=20, pady=10)
        textbox.insert("5.0", f"The file you have chosen to convert is {getting_filename}")


def conversion():
    a = filename()
    basename = os.path.basename(a)
    b, c = os.path.splitext(basename)

    if combobox2.get() == "Word (*.docx)":
        if os.path.exists(f"{home_path}" + "\Desktop" + fr"\{b}.docx") or combobox.get() == "JPG (*.jpg)":
            messagebox.showerror('Invalid conversion', 'The converted file already exists in your Desktop')
        else:
            converting_label.configure(text='Converting.... please wait')
            converting_label.pack(pady=10, padx=10)
            result = convertapi.convert('docx', {'File': f"{a}"})
            result.file.save(f"{home_path}" + "\Desktop" + fr"\{b}.docx")
            textbox_for_converted.pack(padx=10, pady=10)
            converting_label.configure(text='Conversion Complete')
            textbox_for_converted.insert("5.0", f"The file {b}.docx has been saved to your Desktop")

    if combobox2.get() == "PDF (*.pdf)":
        if os.path.exists(f"{home_path}" + "\Desktop" + fr"\{b}.pdf"):
            messagebox.showerror('Invalid conversion', 'The converted file already exists in your Desktop')
        else:
            converting_label.configure(text='Converting.... please wait')
            converting_label.pack(padx=10, pady=10)
            result = convertapi.convert('pdf', {'File': f"{a}"})
            result.file.save(f"{home_path}" + "\Desktop" + fr"\{b}.pdf")
            textbox_for_converted.pack(padx=10, pady=10)
            converting_label.configure(text='Conversion Complete')
            textbox_for_converted.insert("5.0", f"The file {b}.pdf has been saved to Desktop")


def threading_for_conversion():
    threading.Thread(target=conversion).start()


textbox_for_converted = CTkTextbox(master=root, height=50, width=400)


def filename():
    global rootfile
    return rootfile


my_button = CTkButton(master=frame_for_input_buttons, command=choose_file, text='Choose Your File')
my_button.pack(pady=10)

btn_for_conversion = CTkButton(master=frame_for_conversion, command=threading_for_conversion, text="Convert now")

converting_label = CTkLabel(master=root)

root.mainloop()

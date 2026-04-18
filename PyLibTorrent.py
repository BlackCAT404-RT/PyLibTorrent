from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import tkinter as tk
import time
import shutil
import random
import string
import webbrowser
import os

ico = os.path.join("data/PLT_ico.ico")
file_ico = os.path.join("data/PLT_file_ico.ico")
plt_tmp = os.path.join("plt_torrent_tmp")

prog_name = "PyLibTorrent"
not_reclam_ver = False

def donate():
    if not_reclam_ver:
        webbrowser.open("https://www.google.com", new=2)
    else:
        messagebox.showerror("Ошибка", "Извините, но в этой версии данная функция недоступна!")

def site():
    if not_reclam_ver:
        webbrowser.open("https://www.google.com", new=2)
    else:
        messagebox.showerror("Ошибка", "Извините, но в этой версии данная функция недоступна!")

def copy_tor():
    copy_tor_win = tk.Tk()
    copy_tor_win.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Выберите Torrent файлы",
        filetypes=[("Torrent files", "*.torrent"), ("All files", "*.*")]
    )

    if file_paths:
        if not os.path.exists(plt_tmp):
            os.makedirs(plt_tmp)

        for file_path in file_paths:
            _, ext = os.path.splitext(file_path)
            if ext.lower() == '.torrent':
                if os.path.isfile(file_path):
                    random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
                    new_name = f'torrent_{random_code}.torrent'
                    
                    copied_path = os.path.join(plt_tmp, os.path.basename(file_path))
                    shutil.copy2(file_path, copied_path)
                    
                    renamed_path = os.path.join(plt_tmp, new_name)
                    os.rename(copied_path, renamed_path)
                else:
                    messagebox.showerror("Ошибка", f"Файл не найден: {file_path}")
            else:
                messagebox.showerror("Ошибка", f"Файл не является Torrent файлом: {file_path}")
    else:
        messagebox.showerror("Ошибка", "Файлы не выбраны!")

def about():
    about_win = tk.Tk()
    about_win.title('О программе "{}"'.format(prog_name))
    about_win.iconbitmap(ico)
    about_win.resizable(False, False)
    
    w, h = 500, 200
    x = (about_win.winfo_screenwidth() // 2) - (w // 2)
    y = (about_win.winfo_screenheight() // 2) - (h // 2)

    about_win.geometry(f"{w}x{h}+{x}+{y}")

    about_win.mainloop()

main_win = tk.Tk()
main_win.title(prog_name)
main_win.iconbitmap(ico)
main_win.state('zoomed')

menubar = tk.Menu(main_win)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Открыть файл", command=copy_tor)
filemenu.add_command(label="Сохранить")
filemenu.add_separator()
filemenu.add_command(label="Выход", command=main_win.destroy)

referencemenu = tk.Menu(menubar, tearoff=0)
referencemenu.add_command(label="Сайт", command=site)
referencemenu.add_command(label="Донат", command=donate)
referencemenu.add_separator()
referencemenu.add_command(label="О программе", command=about)

menubar.add_cascade(label="Файл", menu=filemenu)
menubar.add_cascade(label="Справка", menu=referencemenu)
main_win.config(menu=menubar)

main_win.mainloop()
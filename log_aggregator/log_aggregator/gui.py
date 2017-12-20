from cStringIO import StringIO
import Tkinter
import opt_parser
import os
import sys
import thread
import time
import colors

def disable_colors():
    colors.bcolors.HEADER = ''
    colors.bcolors.OKBLUE = ''
    colors.bcolors.OKGREEN = ''
    colors.bcolors.WARNING = ''
    colors.bcolors.FAIL = ''
    colors.bcolors.ENDC = ''
    colors.bcolors.BOLD = ''
    colors.bcolors.UNDERLINE = ''


def callback(text_zone, btn_name):
    description_file = get_text(text_zone)
    if (btn_name == "local"):
        thread.start_new_thread(opt_parser.manage_local,(None, True, description_file))
    if (btn_name == "server"):
        thread.start_new_thread(opt_parser.manage_send,(None, True, description_file))


def make_gui():
    disable_colors()
    sys.stdout = std_out_buffer = StringIO()
    main_window = Tkinter.Tk()
    to_pack_list = []

    text_box = generate_text_zone(main_window)
    text_box.pack()

    console = generate_console(main_window)
    console.pack()

    to_pack_list.append(generate_btn(main_window, "Save locally", callback, text_box, "local"))
    to_pack_list.append(generate_btn(main_window, "Send to server", callback, text_box, "server"))

    for element in to_pack_list :
        element.pack()

    while main_window:
        main_window.update_idletasks()
        main_window.update()
        update_console(std_out_buffer, console)
        time.sleep(0.1)


def generate_console(main_window):
    console = Tkinter.Text(main_window, height=10, width=60, background="black", fg="white", font=("Helvetica", 14))
    return console

def update_console(console_stream, console):
    str = console_stream.getvalue()
    console_stream.truncate(0)
    if str:
        console.insert(Tkinter.END, str)
        console.yview_pickplace("end")


def generate_text_zone(main_window):
    text_zone = Tkinter.Text(main_window, height=5, width=60, font=("Helvetica", 16))
    text_zone.pack()
    text_zone.insert(Tkinter.END, "Describe your problem")
    return text_zone

def generate_btn(main_window, btn_text, callback_func, callback_arg1, callback_arg2):
    btn = Tkinter.Button(main_window, text=btn_text, command=lambda: callback_func(callback_arg1, callback_arg2 ))
    return btn

def get_text(text_box):
    input = text_box.get("1.0", Tkinter.END)
    if(input != "Describe your problem\n"):#here we should save in file
        description_file_name = "bug describer"
        fp = open(description_file_name, "w")
        fp.write(input)
        fp.close()
        cwd = os.getcwd()
        file_path = cwd + "/" + description_file_name
        return file_path
    return None

make_gui()

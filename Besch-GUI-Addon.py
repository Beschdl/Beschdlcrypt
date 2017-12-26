from tkinter import filedialog
from tkinter import *
import sys
import os


try:
    import Beschdlcrypt_dev
except ImportError:
    print("Main script not found. Aborting!")
    sys.exit()
import Beschdlcrypt_dev as parent

######### API stuff
class APIListener:
    isActive = False
    def onPrint(self, *args):
        print(*args)#Need to change to output to GUI

    def activate(self):
        isActive = True

isFileOpen = False

parent.addListener(APIListener())
master = Tk()

_type = StringVar(master)
_type.set("Choose A Method")

_ende = StringVar(master)
_ende.set("Encrypt")

current_file = ""

def chosefile(c):
    global current_file
    current_file = openfile().replace("/", "\\")
    filetext = current_file.split("\\")[-1]
    if len(filetext) > 20:
        filetext = filetext[0:15] + "...." + filetext.split(".")[-1]
    c[0].config(text = filetext)

def run():
    parent.args.algorithm = _type.get()
    if _ende.get() == "Encrypt":
        ende = ":e"
    else:
        ende = ":d"
    if len(string_input[0].get("1.0","end")[0:-1]) == 0 or _type.get() in parent.file_input_only_algos or _type.get() + ende in parent.file_input_only_algos:
        parent.args.type = parent.file_input
        parent.args.input = current_file
    else:
        parent.args.input = string_input[0].get("1.0","end")[0:-1]
        parent.args.type = parent.raw_input
    parent.args.output = output_input[0].get("1.0","end")[0:-1]
    parent.args.key = key_input[0].get("1.0","end")
    parent.args.encrypt = _ende.get() == "Encrypt"
    parent.args.decrypt = _ende.get() == "Decrypt"
    parent.main()

mainscreen = OptionMenu(master, _type, *parent.algos), 0.4, 0.1, 0.2, 0.1
en_de_select = OptionMenu(master, _ende, "Encrypt", "Decrypt"), 0.7, 0.4, 0.1, 0.05
string_input = Text(master), 0.2, 0.4, 0.4, 0.2
file_button = Button(master, text="Choose File", command = lambda: chosefile(file_text)), 0.2, 0.4, 0.1, 0.05
file_text = Label(master, text = "No file Chosen", bg = "#f49e42", anchor = W), 0.3, 0.4, 0.2, 0.05
text_file_button = Button(master, text="Choose File", command = lambda: chosefile(text_file_text)), 0.2, 0.7, 0.1, 0.05
text_file_text = Label(master, text = "No file Chosen", bg = "#f49e42", anchor = W), 0.3, 0.7, 0.2, 0.05
key_input_text = Label(master, text = "key:", bg = "#f49e42", anchor = W), 0.67, 0.5, 0.1, 0.05
key_input = Text(master), 0.7, 0.5, 0.2, 0.1
finalize_button = Button(master, text = "Encrypt", command = run), 0.4, 0.8, 0.2, 0.1
output_input = Text(master), 0.7, 0.6, 0.2, 0.1
output_input_text = Label(master, text = "output file:", bg = "#f49e42", anchor = W), 0.62, 0.6, 0.07, 0.05

def update():
    if _type.get() in parent.aliases:
        _type.set(parent.aliases[_type.get()])
    master.after(50, update)
    if _ende.get() == "Encrypt":
        finalize_button[0].config(text = "Encrypt")
    elif _ende.get() == "Decrypt":
        finalize_button[0].config(text = "Decrypt")
    if _ende.get() == "Encrypt":
        ende = ":e"
    else:
        ende = ":d"

    if _type.get() not in parent.non_cript_algos and _type.get() + ende not in parent.non_cript_algos:
        build(en_de_select)
    else:
        finalize_button[0].config(text = "Go")
        remove(en_de_select)

    if _type.get() not in parent.file_input_only_algos and _type.get() + ende not in parent.file_input_only_algos:
        build(string_input)
        build(text_file_button)
        build(text_file_text)
        remove(file_button)
        remove(file_text)
    else:
        remove(string_input)
        remove(text_file_button)
        remove(text_file_text)
        build(file_button)
        build(file_text)

    if _type.get() in parent.require_keys_algos or _type.get() + ende in parent.require_keys_algos:
        build(key_input)
        build(key_input_text)
    else:
        remove(key_input)
        remove(key_input_text)

    if _type.get() in parent.require_output_algos or _type.get() + ende in parent.require_output_algos:
        build(output_input)
        build(output_input_text)
    else:
        remove(output_input)
        remove(output_input_text)







built_componants = []
packed_componatns = []

def build(c):
    if c in built_componants: return
    built_componants.append(c)
    if c not in packed_componatns:
        c[0].pack()
        packed_componatns.append(c)
    c[0].place(relx = c[1], rely = c[2], relwidth = c[3], relheight = c[4])


def remove(c):
    if c not in built_componants: return;
    built_componants.remove(c)
    c[0].place(relx = 5, rely = 5)

def openfile():
    return filedialog.askopenfilename(title = "Select file")

build(mainscreen)
build(finalize_button)
master.wm_title("Beschdlcrypt")
master.after(50, update)
master.config(width=1000, height=500, bg = "#f49e42")
master.mainloop()
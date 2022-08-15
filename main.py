from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk
from tktooltip import ToolTip
import win32api
import pygame



root = Tk()
root.title("Havryho textový editor")
root.iconbitmap("./crow.ico")
root.attributes('-fullscreen',True)
pygame.mixer.init()


# set variable for open file name
global open_status_name
open_status_name = False
global selected_text
selected_text = False
current_font_family= "Arial"
global current_font_size
current_font_size = 16


# skryje title bar
# root.overrideredirect(True)

# create new file function
# Vymaze okno od prvniho radku az po knec
def new_file():
	'''Funkce vymaže text box a nastaví titulek programu tak, že k němu připíše new file ve spodním boxu nastaví
	také New file, Nastaví také globální proměnou open_status_name na False, protože bez ní se nový soubor ukládal
	do naposled použitého souboru tímto se tento bug odstranil'''
	my_text_widget.delete(1.0, END)
	root.title("Havryho textový editor - New file")
	bottom_status_bar.config(text=f"New file          ")
	global open_status_name
	open_status_name = False


# function open file
def open_file():
	""""Funkce open_file nejprve vymaže text box a ten bude úplně prázdný, následně nastaví vyskakovací okno,
	kde se soubory budou otvírat z přednastavené složky,zkontroluje jestli už existuje jméno souboru a
	uloží ho do globální proměnné pro pozdější použití , nastaví titulek okna open file a nastaví tipy souborů
	zatím ponechám text, html a python a ještě všechny tipy souborů. Potom nastaví spodní label a vypíše
	 cestu souboru plus název souboru poté upraví titulek okna a přidá k názvu titulku i název souboru.
	 Poté funkce otevře soubor pro čtení a přidá všechno ze souboru do textboxu a zavře soubor."""
	my_text_widget.delete(1.0, END)
	# Grab file
	file_name = filedialog.askopenfilename(initialdir="C:/Users/jozin/OneDrive/Dokumenty/Havryho editor", title="Open file", filetypes=(("Text files" , "*.txt"), ("HTML files", "*.html"), ("Python files", "*.py"), ("All files", "*.*")))
	# check if is there filename
	if file_name:
		# we do from file name global variable for use it later
		global open_status_name
		open_status_name = file_name
	# update bottom status bar and title of window
	name = file_name
	bottom_status_bar.config(text=f"{name}          ")
	name = name.replace("C:/Program Files/Havryho editor", "")
	root.title(f"Havryho textový editor - {name}")
	# open file
	file_name = open(file_name, 'r')
	stuff = file_name.read()
	# add file to text box
	my_text_widget.insert(END, stuff)
	# close the open file
	file_name.close()


# save us file
def save_us():
	'''Nastaví vzyskakovací okno, kde se soubory budou ukládat do přednastavené složky, nastaví titulek okna na Save file
	a nastaví tipy souborů. Poté funkce upraví ve spodním boxu text a upozorní uživatele, že soubor je uložen
	a následně změní jméno souboru a nebo ponechá to staré záleží na tom, co zadá uživatel a upraví opět název
	titulku okna na jméno souboru. Funkce pak uloží soubor tak že ho otevře pro zapsaní to zančí w a uloží vše
	od prvního řádku až po konec souboru. Pak funkce soubor zavře a můžeme dál pracovat v programu'''
	file_name = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Users/jozin/OneDrive/Dokumenty/Havryho editor", title="Save file", filetypes=(("Text files", "*.txt"), ("HTML files", "*.html"), ("Python files", "*.py"), ("All files", "*.*")))
	if file_name:
		# update status bars
		name = file_name
		bottom_status_bar.config(text=f"Saved: {name}          ")
		name = name.replace("C:/Users/jozin/OneDrive/Dokumenty/Havryho editor", "")
		root.title(f"Havryho textový editor - {name}")

		# save the file
		file_name = open(file_name, 'w')
		file_name.write(my_text_widget.get(1.0, END))
		# close file
		file_name.close()


# save file
def save_file():
	'''Pokud je open status name pravda(existuje) otevře soubor pro zapsání a přepíše vše od prvního řádku až po konec
	 souboru a soubor zase uzavře, potom přepíše text ve spodním boxu aby upozornil uživatele, že soubor je uložen.
	Pokud open status name neexistuje zavolá funkci save us '''
	global open_status_name
	if open_status_name:
		# save the file
		file_name = open(open_status_name, 'w')
		file_name.write(my_text_widget.get(1.0, END))
		# close file
		file_name.close()
		bottom_status_bar.config(text=f"Saved: {open_status_name}          ")
	else:
		save_us()


# cut text
def cut_text(e):
	'''Funkce zkontroluje zda je použitá klávesová zkratka parametr e je použit jako parametr lambda funkce, která je
	nastavená na False, pokud je použitá nastaví se True a vybraní text se uloží do dočasného úložiště a vybraný text
	pak bude použitelný všude v aplikaci,pokud není použitá klavesova zkratka označený text v textovém okně vytvoří a
	 proměnou selected_text, a uloží do ní označený text selected text je globální proměná, protože budu m´potřebovat
	  s ní pracovat venku z funkce, poté z text boxu označený text vymaže a vyčistí dočasné úložiště clipboard'''
	global selected_text
	# check to see if keyboard shortcut used
	if e:
		selected_text = root.clipboard_get()
	else:
		if my_text_widget.selection_get():
			# grab selected text from text box
			selected_text = my_text_widget.selection_get()
			# delete selected text from text box
			my_text_widget.delete("sel.first", "sel.last")
			# clear the clipboard
			root.clipboard_clear()
			root.clipboard_append(selected_text)


# copy text
def copy_text(e):
	'''Pokud je použita klávesová zkratka text se uloží do dočasného úložiště pokud použiju talčítko, vybraný text
	se uloží do proměné selected text a vymaže se dočasné úložiště a poté se do něj kopírovaný text přidá '''
	global selected_text
	# check to see f we use keyboards shortcut
	if e:
		selected_text = root.clipboard_get()
	if my_text_widget.selection_get():
		# Grab selected text from text box
		selected_text = my_text_widget.selection_get()
		# clear the clipboard
		root.clipboard_clear()
		root.clipboard_append(selected_text)


# paste text
def paste_text(e):
	'''Pokud je text vybraný to znamená je něco uložené v proměné selected text, funkce vloží vybraný text na pozici
	kurzoru, proměná selected text jsou koordináty kurzoru, kde se nachází kurzor a selected text je proměná, ve které
	je uložen text '''
	global selected_text
	# check if keyboard shortcut is used
	if e:
		selected_text = root.clipboard_get()
	else:
		if selected_text:
			position = my_text_widget.index(INSERT)
			my_text_widget.insert(position, selected_text)


def bold_text():
	'''Tato funkce vztvoří bold font. Potom ho nastaví pro text v my_text_widget a poté zkontroluje, zda už tento tag
	není použitý a pokud ano odstraní tento font z textu pokud použitý není nastaví opět font bold na vybraný text'''
	# create bold font
	bold_font = font.Font(my_text_widget, my_text_widget.cget("font"))
	bold_font.configure(weight="bold")
	# configure tag
	my_text_widget.tag_configure("bold", font=bold_font)
	# deffine current tag
	current_tags = my_text_widget.tag_names("sel.first")
	# if statement to see if tag is been set
	if "bold" in current_tags:
		my_text_widget.tag_remove("bold", "sel.first", "sel.last")
	else:
		my_text_widget.tag_add("bold", "sel.first", "sel.last")


def italics_text():
	'''Tato funkce vztvoří italic font. Potom ho nastaví pro text v my_text_widget a poté zkontroluje, zda už tento tag
	není použitý a pokud ano odstraní tento font z textu pokud použitý není nastaví opět font bold na vybraný text'''
	# create bold font
	italics_font = font.Font(my_text_widget, my_text_widget.cget("font"))
	italics_font.configure(slant="italic")
	# configure tag
	my_text_widget.tag_configure("italic", font=italics_font)
	# deffine current tag
	current_tags = my_text_widget.tag_names("sel.first")
	# if statement to see if tag is been set
	if "italic" in current_tags:
		my_text_widget.tag_remove("italic", "sel.first", "sel.last")
	else:
		my_text_widget.tag_add("italic", "sel.first", "sel.last")


def underline_text():
	'''Tato funkce vztvoří font s podtrženým textem. Potom ho nastaví pro text v my_text_widget a poté zkontroluje,
	 zda už tento tag není použitý a pokud ano odstraní tento font z textu pokud použitý není nastaví opět font
	  underline na vybraný text'''
	# create underline font
	underline_font = font.Font(my_text_widget, my_text_widget.cget("font"))
	underline_font.configure(underline=True)
	# configure tag
	my_text_widget.tag_configure("underline", font=underline_font)
	# deffine current tag
	current_tags = my_text_widget.tag_names("sel.first")
	# if statement to see if tag is been set
	if "underline" in current_tags:
		my_text_widget.tag_remove("underline", "sel.first", "sel.last")
		my_text_widget.tag_remove("overstrike", "sel.first", "sel.last")
	else:
		my_text_widget.tag_add("underline", "sel.first", "sel.last")


def overstrike_text():
	'''Tato funkce vztvoří font s podtrženým textem. Potom ho nastaví pro text v my_text_widget a poté zkontroluje,
	 zda už tento tag není použitý a pokud ano odstraní tento font z textu pokud použitý není nastaví opět font
	  underline na vybraný text'''
	# create underline font
	overstrike_font = font.Font(my_text_widget, my_text_widget.cget("font"))
	overstrike_font.configure(overstrike=True)
	# configure tag
	my_text_widget.tag_configure("overstrike", font=overstrike_font)
	# deffine current tag
	current_tags = my_text_widget.tag_names("sel.first")
	# if statement to see if tag is been set
	if "overstrike" in current_tags:
		my_text_widget.tag_remove("overstrike", "sel.first", "sel.last")
		my_text_widget.tag_remove("underline", "sel.first", "sel.last")
	else:
		my_text_widget.tag_add("overstrike", "sel.first", "sel.last")


# change selected text color
def text_color():
	'''Tato funkce nechá uživatele vybrat barvu z palety barev a uloží ji do proměnné my_color, potom upraví
	text v dolním baru a vypíše kód použité barvy poté vytvoří font s touto barvou a jako v ostatních funkcích
	zkontroluje zda už tag není použitý a pokud ano tak ho zruší a pokud ne tak změní barvu textu'''
	# pick a color
	my_color = colorchooser.askcolor()[1]
	if my_color:
		bottom_status_bar.config(text=my_color)
		# create color font
		color_font = font.Font(my_text_widget, my_text_widget.cget("font"))
		# configure tag
		my_text_widget.tag_configure("color_text", font=color_font, foreground=my_color)
		# deffine current tag
		current_tags = my_text_widget.tag_names("sel.first")
		# if statement to see if tag is been set
		if "color_text" in current_tags:
			my_text_widget.tag_remove("color_text", "sel.first", "sel.last")
		else:
			my_text_widget.tag_add("color_text", "sel.first", "sel.last")


def background_color():
	'''Tato funkce nechá vybrat uživatele barvu a nastaví ji jako pozadí'''
	my_color = colorchooser.askcolor()[1]
	if my_color:
		my_text_widget.config(bg=my_color)


def all_text_color():
	'''Tato funkce necá vybrat uživatele barvu a změní veškerý text na vybranou barvu'''
	my_color = colorchooser.askcolor()[1]
	if my_color:
		my_text_widget.config(fg=my_color)


# Print file function
def print_file():
	'''Pokud file to print existuje '''
	# Grab file
	file_to_print = filedialog.askopenfilename(initialdir="C:/Users/jozin/OneDrive/Dokumenty/Havryho editor",
	                                           title="Open file",
	                                           filetypes=(("Text files" , "*.txt"), ("HTML files", "*.html"), ("Python files", "*.py"), ("All files", "*.*")))
	if file_to_print:
		win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)


# Select all text
def select_all_text(e):
	'''Tato funkce označí veškerý text od prvního řádku až do konce dokumentu'''
	# Add sel tag to all text
	my_text_widget.tag_add("sel", 1.0, END)


# Clear all text
def clear_all():
	'''Tato funkce vymaže veškerý text z dokumentu'''
	my_text_widget.delete(1.0, END)


def day_mode():
	main_color = "SystemButtonFace"
	second_color = "SystemButtonFace"
	text_color = "black"
	root.config(bg=main_color)
	bottom_status_bar.config(bg=main_color, fg=text_color)
	my_text_widget.config(bg=second_color, fg=text_color)
	up_toolbar_frame.config(bg=main_color)
	# Toolbar buttons
	bold_button.config(bg=second_color)
	italics_button.config(bg=second_color)
	underline_button.config(bg=second_color)
	overstrike_button.config(bg=second_color)
	undo_button.config(bg=second_color)
	redo_button.config(bg=second_color)
	color_button.config(bg=second_color)
	print_file_button.config(bg=second_color)
	new_file_button.config(bg=second_color)
	save_file_button.config(bg=second_color)
	align_right_button.config(bg=second_color)
	align_left_button.config(bg=second_color)
	align_center_button.config(bg=second_color)
	night_mode_button.config(bg=second_color)
	day_mode_button.config(bg=second_color)
	play_button.config(bg=second_color)
	stop_button.config(bg=second_color)
	# file menu colors
	file_menu.config(bg=main_color, fg=text_color)
	edit_menu.config(bg=main_color, fg=text_color)
	options_menu.config(bg=main_color, fg=text_color)
	color_menu.config(bg=main_color, fg=text_color)


def night_mode():
	main_color = "#373737"
	second_color = "grey45"
	text_color = "light green"
	root.config(bg=main_color)
	bottom_status_bar.config(bg=main_color, fg=text_color)
	my_text_widget.config(bg=second_color, fg=text_color)
	up_toolbar_frame.config(bg=main_color)
	# Toolbar buttons
	bold_button.config(bg=second_color)
	italics_button.config(bg=second_color)
	underline_button.config(bg=second_color)
	overstrike_button.config(bg=second_color)
	undo_button.config(bg=second_color)
	redo_button.config(bg=second_color)
	color_button.config(bg=second_color)
	print_file_button.config(bg=second_color)
	new_file_button.config(bg=second_color)
	save_file_button.config(bg=second_color)
	align_right_button.config(bg=second_color)
	align_left_button.config(bg=second_color)
	align_center_button.config(bg=second_color)
	night_mode_button.config(bg=second_color)
	day_mode_button.config(bg=second_color)
	play_button.config(bg=second_color)
	stop_button.config(bg=second_color)
	# file menu colors
	file_menu.config(bg=main_color, fg=text_color)
	edit_menu.config(bg=main_color, fg=text_color)
	options_menu.config(bg=main_color, fg=text_color)
	color_menu.config(bg=main_color, fg=text_color)


def crazy_color_mode():
	pass


def my_popup_menu(e):
	try:
		pop_up_menu.tk_popup(e.x_root, e.y_root,0)
	finally:
		# Release the grab
		pop_up_menu.grab_release()


def font_size_chooser(e):
	global current_font_size
	current_font_size = size_var.get()
	my_text_widget.tag_configure("size_text", font=(current_font_family, current_font_size))
	# deffine current tag
	my_text_widget.tag_add("size_text", "sel.first", "sel.last")


def change_font(e):
	global current_font_family
	current_font_family = font_family.get()
	my_text_widget.tag_configure("font_family", font=(current_font_family, current_font_size))
	# deffine current tag
	my_text_widget.tag_add("font_family", "sel.first", "sel.last")


# Align Left
def align_left():
	text_align = my_text_widget.get(1.0, "end")
	my_text_widget.tag_config("left", justify=LEFT)
	my_text_widget.delete(1.0, END)
	my_text_widget.insert(INSERT, text_align, "left")


# Align Center
def align_center():
	text_align = my_text_widget.get(1.0, "end")
	my_text_widget.tag_config("center", justify=CENTER)
	my_text_widget.delete(1.0, END)
	my_text_widget.insert(INSERT, text_align, "center")


# Align Right
def align_right():
	text_align = my_text_widget.get(1.0, "end")
	my_text_widget.tag_config("right", justify=RIGHT)
	my_text_widget.delete(1.0, END)
	my_text_widget.insert(INSERT, text_align, "right")

def play_song():
	'''Funkce načte soubor s muzikou a nastaví přehrávání do nekonečna'''
	pygame.mixer.music.load("music.mp3")
	pygame.mixer.music.play(loops=-1)

def stop_song():
	'''Funkce zastaví muziku'''
	pygame.mixer.music.stop()

# create toolbar frame
up_toolbar_frame = Frame(root)
up_toolbar_frame.pack(fill=X)

# create main frame
my_frame = Frame(root, bg='black', relief='raised', bd=1)
my_frame.pack(pady=5)

# create scroll bar for text box - vertical
my_text_scroll = Scrollbar(my_frame)
my_text_scroll.pack(side=RIGHT, fill=Y)

# horizontal scroll bar
my_text_scroll_horizontal = Scrollbar(my_frame, orient="horizontal")
my_text_scroll_horizontal.pack(side=BOTTOM, fill=X)

# create text widget

# selectbackground je barva pozadi za oznacenym textem
# selectforeground je barva oynaceneho textu
# undo true mohu pouzit ctrl z k vraceni akce
my_text_widget = Text(my_frame, width=101,
                      height=25,
                      font=(current_font_family, current_font_size),
                      selectbackground="grey", selectforeground="red",
                      undo=True,
                      yscrollcommand=my_text_scroll.set,
                      wrap="none",
                      xscrollcommand=my_text_scroll_horizontal.set)
my_text_widget.pack()

# configure our scroll bar
my_text_scroll.config(command=my_text_widget.yview)

# configure my horizontal scroll bar
my_text_scroll_horizontal.config(command=my_text_widget.xview)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add file menu
# tearoff= False menu nejde vyjmout a presouvat
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New file", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save as", command=save_us)
file_menu.add_separator()
file_menu.add_command(label="Print file", command=print_file)
# add separator vytvori linku v menu
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


# add edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Cut                      ", command=lambda: cut_text(False), accelerator="ctrl + x")
edit_menu.add_command(label="Copy                     ", command=lambda: copy_text(False), accelerator="ctrl + c")
edit_menu.add_command(label="Paste                    ", command=lambda: paste_text(False), accelerator="ctrl + v")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text_widget.edit_undo, accelerator="ctrl + z")
edit_menu.add_command(label="Redo", command=my_text_widget.edit_redo, accelerator="ctrl + y")
edit_menu.add_separator()
edit_menu.add_command(label="Select all", command=lambda: select_all_text(True), accelerator="ctrl + a")
edit_menu.add_command(label="Clear all", command=clear_all)
# add color menu
# tearoff= False menu nejde vyjmout a presouvat
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="colors", menu=color_menu)

color_menu.add_command(label="Text color", command=text_color)
color_menu.add_command(label="All text color", command=all_text_color)
color_menu.add_command(label="Background color", command=background_color)

# Options menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)

options_menu.add_command(label="Day mode", command=day_mode)
options_menu.add_command(label="Night mode", command=night_mode)
options_menu.add_command(label="Crazy color mode", command=crazy_color_mode)

# popup menu
pop_up_menu = Menu(root, tearoff=0)
pop_up_menu.add_command(label="cut", command=lambda: cut_text(False))
pop_up_menu.add_command(label="copy", command=lambda: copy_text(False))
pop_up_menu.add_command(label="paste", command=lambda: paste_text(False))
pop_up_menu.add_separator()
pop_up_menu.add_command(label="Undo", command=my_text_widget.edit_undo, accelerator="ctrl + z")
pop_up_menu.add_command(label="Redo", command=my_text_widget.edit_redo, accelerator="ctrl + y")
pop_up_menu.add_separator()
pop_up_menu.add_command(label="Select all", command=lambda: select_all_text(True), accelerator="ctrl + a")


# add status bar of bottom
bottom_status_bar = Label(root, text="Ready            ", anchor=E, font=12)
bottom_status_bar.pack(side=BOTTOM, fill=X, pady=5)


# Edit binding keys
# pro bindování použít atribut bind a jako parametry zadat klávesu a potom funkci
root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)
root.bind("<Control-Key-a>", select_all_text)
# nastavi bind na prave kliknuti
root.bind("<Button-3>", my_popup_menu)


# image of buttons
undo_image = PhotoImage(file='undo1.png')
redo_image = PhotoImage(file='redo1.png')
night_image = PhotoImage(file='moon.png')
day_image = PhotoImage(file='sun.png')
new_file_image = PhotoImage(file="add-document.png")
save_file_image = PhotoImage(file="disk.png")
print_file_image = PhotoImage(file="print.png")
italic_image = PhotoImage(file="italic.png")
bold_image = PhotoImage(file="bold.png")
underline_image = PhotoImage(file="underline.png")
overline_image = PhotoImage(file="overline.png")
color_image = PhotoImage(file="font_color.png")
align_left_image = PhotoImage(file="align_left.png")
align_center_image = PhotoImage(file="align_center.png")
align_right_image = PhotoImage(file="align_right.png")
play_image = PhotoImage(file="play.png")
stop_image = PhotoImage(file="stop.png")

# create buttons
# pro buttony mohu pouzit grid protoze to je v novem frame
new_file_button = Button(up_toolbar_frame, image=new_file_image, command=new_file)
new_file_button.grid(column=0, row=0, padx=(20, 0))

print_file_button = Button(up_toolbar_frame, image=print_file_image, command=print_file)
print_file_button.grid(column=1, row=0, padx=5)

save_file_button = Button(up_toolbar_frame, image=save_file_image, command=save_file)
save_file_button.grid(column=2, row=0, padx=(0, 25))

# size list box
size_var = IntVar()
font_size_box = ttk.Combobox(up_toolbar_frame, width=14, textvariable=size_var, state="readonly")
font_size_box["values"] = tuple(range(8, 80, 2))
# set font 16 how i want
font_size_box.current(4)
font_size_box.grid(column=3, row=0, padx=15)
font_size_box.bind("<<ComboboxSelected>>", font_size_chooser)

# font list box
font_tuple = font.families()
font_family = StringVar()
font_box = ttk.Combobox(up_toolbar_frame, width=30, textvariable=font_family, state="readonly")
font_box["values"] = font_tuple
font_box.current(font_tuple.index("Arial"))
font_box.grid(column=4, row=0, padx=5)
font_box.bind("<<ComboboxSelected>>", change_font)

# bold button
bold_button = Button(up_toolbar_frame, text="Bold text", image=bold_image, command=bold_text)
bold_button.grid(column=5, row=0, padx=(20, 0))

# italic  button
italics_button = Button(up_toolbar_frame, image=italic_image, text="Italics text", command=italics_text)
italics_button.grid(column=6, row=0, padx=5)

# underline button
underline_button = Button(up_toolbar_frame, text="Underline text", image=underline_image, command=underline_text)
underline_button.grid(column=7, row=0, padx=(0, 5))

# overstrike button
overstrike_button = Button(up_toolbar_frame, text="Overstrike text", image=overline_image, command=overstrike_text)
overstrike_button.grid(column=8, row=0)

# color text button
color_button = Button(up_toolbar_frame, text="Colors", image=color_image, command=text_color)
color_button.grid(column=9, row=0, padx=25)

align_left_button = Button(up_toolbar_frame, image=align_left_image, command=align_left)
align_left_button.grid(column=10, row=0, padx=5)

align_center_button = Button(up_toolbar_frame, image=align_center_image, command=align_center)
align_center_button.grid(column=11, row=0, padx=(0, 5))

align_right_button = Button(up_toolbar_frame, image=align_right_image, command=align_right)
align_right_button.grid(column=12, row=0, padx=0)

# undo button
undo_button = Button(up_toolbar_frame, text="Undo", image=undo_image, command=my_text_widget.edit_undo)
undo_button.grid(column=13, row=0, padx=(100, 0))

# redo button
redo_button = Button(up_toolbar_frame, text="Redo", image=redo_image, command=my_text_widget.edit_redo)
redo_button.grid(column=14, row=0, padx=(5, 50))


day_mode_button = Button(up_toolbar_frame, image=day_image, command=day_mode)
day_mode_button.grid(column=15, row=0, padx=5)

night_mode_button = Button(up_toolbar_frame, image=night_image, command=night_mode)
night_mode_button.grid(column=16, row=0, padx=(0, 50))

play_button = Button(up_toolbar_frame, image=play_image, command=play_song)
play_button.grid(column=17, row=0, padx=5)

stop_button = Button(up_toolbar_frame, image=stop_image, command=stop_song)
stop_button.grid(column=18, row=0)



# Tooltips
ToolTip(stop_button, msg="Stop work music button", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(play_button, msg="Start work music button", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(night_mode_button, msg="Night mode", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(day_mode_button, msg="Day mode", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(redo_button, msg="Redo", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(undo_button, msg="Undo", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(align_right_button, msg="Align text to right", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(align_center_button, msg="Align text to center", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(align_left_button, msg="Align text to left", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(color_button, msg="Choose color of text", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(overstrike_button, msg="Overstrike text", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(underline_button, msg="Underline text", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(italics_button, msg="Italics text", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")
ToolTip(bold_button, msg="Bold text", follow=True, parent_kwargs={"bg": "black", "padx": 2, "pady": 2}, bg="lemon chiffon")

root.mainloop()

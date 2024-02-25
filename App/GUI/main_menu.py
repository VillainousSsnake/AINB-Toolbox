# Contains main menu function

# Importing dependencies
from tkinterdnd2 import DND_FILES
import App.GUI.customtkinter as ctk
from tkinter import filedialog
from functools import partial


# _func class
class _Func:
    @staticmethod
    def drop_file(tabview, open_file, event=None):
        open_file = event.data[1:len(event.data)-1]
        tabview.set("AINB Editor")


# Button func
class ButtonFunc:
    @staticmethod
    def drag_and_drop_button_command(tabview, open_file, event=None):

        supportedFileFormats = (
            (
                'All Editable Files', [
                    '*.ainb'
                ]
            ),
            ('AI Node Binary', '*.ainb')
        )

        open_file = filedialog.askopenfile(title="Select a file", filetypes=supportedFileFormats)

        tabview.set("AINB Editor")


# main_menu function
def main_menu(app):

    # Creating variables
    open_file = None
    file_specs = None

    # Creating root window
    root = ctk.CTk()
    root.title("AINB-Toolbox - VillainousSsnake - Alpha V0.1")
    root.geometry("850x525+200+200")

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Creating tabview
    tabview = ctk.CTkTabview(root, height=1000)
    tabview.add("Home")
    tabview.add("AINB Editor")
    tabview.add("Settings")
    tabview.set("Home")
    tabview.pack(fill=ctk.BOTH)

    dragAndDropTarget = ctk.CTkLabel(tabview.tab("Home"), font=("Ariel", 20),
                                     text="➕ \nDrag & Drop Here",
                                     corner_radius=10, fg_color="gray", wraplength=300)
    dragAndDropTarget.pack(expand=True, fill=ctk.BOTH, padx=40, pady=40)

    drop_partial = partial(_Func.drop_file, tabview, open_file)
    dragAndDropTarget.drop_target_register(DND_FILES)
    dragAndDropTarget.dnd_bind("<<Drop>>", drop_partial)
    drag_and_drop_button_command = partial(ButtonFunc.drag_and_drop_button_command, open_file, tabview)
    dragAndDropTarget.bind("<1>", drag_and_drop_button_command)

    # Root mainloop
    root.mainloop()

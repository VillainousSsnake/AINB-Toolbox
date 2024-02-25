# Contains main menu function

# Importing dependencies
from tkinterdnd2 import DND_FILES
import App.GUI.customtkinter as ctk
from tkinter import filedialog


# _func class
class _Func:
    @staticmethod
    def drop_file(event):
        filepath = event.data[1:len(event.data)-1]


# Button func
class ButtonFunc:
    @staticmethod
    def drag_and_drop_button_command(event=None):

        supportedFileFormats = (
            (
                'All Editable Files', [
                    '*.ainb'
                ]
            ),
            ('AI Node Binary', '*.ainb')
        )

        filepath = filedialog.askopenfile(title="Select a file", filetypes=supportedFileFormats)


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
    tabview = ctk.CTkTabview(root)
    tabview.add("Home")
    tabview.add("AINB Editor")
    tabview.add("Settings")
    tabview.set("Home")
    tabview.pack(fill=ctk.BOTH)

    dragAndDropTarget = ctk.CTkLabel(tabview.tab("Home"),
                                     text="➕ \nDrag & Drop Here",
                                     corner_radius=10, fg_color="gray", wraplength=300)
    dragAndDropTarget.pack(expand=True, fill=ctk.BOTH, padx=40, pady=40)

    dragAndDropTarget.drop_target_register(DND_FILES)
    dragAndDropTarget.dnd_bind("<<Drop>>", _Func.drop_file)
    dragAndDropTarget.bind("<1>", ButtonFunc.drag_and_drop_button_command)

    # Root mainloop
    root.mainloop()

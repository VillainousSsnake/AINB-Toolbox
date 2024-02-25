# Contains main menu function

# Importing dependencies
from tkinterdnd2 import DND_FILES
import App.GUI.customtkinter as ctk


# _func class
class _Func:
    @staticmethod
    def drop_file(event):
        print(event.data[1:len(event.data)-1])


# Button func
class ButtonFunc:
    @staticmethod
    def app_section_header_button_command(value: str = None):
        pass  # TODO: Stub


# main_menu function
def main_menu(app):

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

    # Creating app_sections_header button
    app_sections_header = ctk.CTkSegmentedButton(root,
                                                 values=["Home", "AINB Editor", "Settings"],
                                                 command=ButtonFunc.app_section_header_button_command)
    app_sections_header.set("Home")
    app_sections_header.pack()

    dragAndDropTarget = ctk.CTkLabel(root, text="➕ \nDrag & Drop Here", corner_radius=10, fg_color="gray", wraplength=300)
    dragAndDropTarget.pack(expand=True, fill="both", padx=40, pady=40)

    dragAndDropTarget.drop_target_register(DND_FILES)
    dragAndDropTarget.dnd_bind("<<Drop>>", _Func.drop_file)

    # Root mainloop
    root.mainloop()

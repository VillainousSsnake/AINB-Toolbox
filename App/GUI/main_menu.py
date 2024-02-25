# Contains main menu function

# Importing dependencies
import customtkinter as ctk
from tkinterdnd2 import DND_FILES


# _func class
class _Func:
    @staticmethod
    def drop_file(event: str = None):
        pass  # TODO: Stub


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

    label = ctk.CTkLabel(root, text="➕ \nDrag & Drop Here", corner_radius=10, fg_color="blue", wraplength=300)
    label.pack(expand=True, fill="both", padx=40, pady=40)

    # Add this 2 lines to make it a dnd widget
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', drop)

    # Root mainloop
    root.mainloop()

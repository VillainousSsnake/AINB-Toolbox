# Contains main menu function

# Importing dependencies
import customtkinter as ctk


# Button func
class ButtonFunc:
    @staticmethod
    def file_button_command():
        pass  # TODO: Stub

    @staticmethod
    def settings_button_command():
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

    # TODO: Other code here

    # Root mainloop
    root.mainloop()

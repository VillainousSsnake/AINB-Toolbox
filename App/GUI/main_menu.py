# Contains main menu function

# Importing dependencies
from tkinterdnd2 import DND_FILES
import App.GUI.customtkinter as ctk
from tkinter import filedialog
from functools import partial
from App.AppLib.config import Config


# _func class
class _Func:
    @staticmethod
    def update_theme_option_menu(theme_option_menu):
        match Config.get_setting("current_theme"):
            case "dark":
                theme_option_menu.set("Dark")
            case "light":
                theme_option_menu.set("Light")
            case "system":
                theme_option_menu.set("System")

    @staticmethod
    def drop_file(tabview, open_file, event=None):
        open_file = event.data[1:len(event.data)-1]
        tabview.set("AINB Editor")


# Button func
class ButtonFunc:
    @staticmethod
    def export_all_ainb_button_command(app):
        pass  # TODO: Stub

    @staticmethod
    def theme_option_menu_button_command(app, appearance):
        ctk.set_appearance_mode(appearance.lower())
        app.settings["current_theme"] = appearance.lower()
        Config.overwrite_setting("current_theme", appearance.lower())

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

        fp = filedialog.askopenfile(title="Select a file", filetypes=supportedFileFormats)

        if fp is None:
            return 1

        open_file = fp

        tabview.set("AINB Editor")


# main_menu function
def main_menu(app):

    # Detecting if the romfs_path is None
    if app.settings["romfs_path"] is None:
        pass  # TODO: Stub

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

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

    #
    #
    #
    #
    #                      ########################
    #                      #    "Home" SECTION    #
    #                      ########################


    dragAndDropTarget = ctk.CTkLabel(tabview.tab("Home"), font=("Ariel", 20),
                                     text="➕ \nDrag & Drop Here",
                                     corner_radius=10, wraplength=300)
    dragAndDropTarget.pack(expand=True, fill=ctk.BOTH, padx=40, pady=40)

    drop_partial = partial(_Func.drop_file, tabview, open_file)
    dragAndDropTarget.drop_target_register(DND_FILES)
    dragAndDropTarget.dnd_bind("<<Drop>>", drop_partial)
    drag_and_drop_button_command = partial(ButtonFunc.drag_and_drop_button_command, tabview, open_file)
    dragAndDropTarget.bind("<1>", drag_and_drop_button_command)

    export_all_ainb_button_partial = partial(ButtonFunc.export_all_ainb_button_command, app)
    export_all_ainb_button = ctk.CTkButton(master=tabview.tab("Home"),
                                           text="Extract all AINB from RomFS Dump",
                                           command=export_all_ainb_button_partial)
    export_all_ainb_button.pack()

    #
    #
    #
    #
    #                      ############################
    #                      #    "Settings" SECTION    #
    #                      ############################

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    romfs_path_label = ctk.CTkLabel(
        master=tabview.tab("Settings"),
        text="Game Dump Location",
        corner_radius=5, fg_color="#3B8ED0"
    )
    romfs_path_label.grid(row=0, column=0, padx=20, pady=10)

    romfs_path_entry = ctk.CTkEntry(master=tabview.tab("Settings"),
                                    placeholder_text="Eg. (D:\\Tears of the Kingdom\\romfs)")
    romfs_path_entry.grid(row=0, column=1)

    theme_label = ctk.CTkLabel(
        master=tabview.tab("Settings"),
        text="Current Theme            ",
        corner_radius=5, fg_color="#3B8ED0"
    )
    theme_label.grid(row=1, column=0)

    theme_option_menu_command = partial(ButtonFunc.theme_option_menu_button_command, app)
    theme_option_menu = ctk.CTkOptionMenu(
        master=tabview.tab("Settings"),
        values=["Dark", "Light", "System"],
        command=theme_option_menu_command
    )
    _Func.update_theme_option_menu(theme_option_menu)
    theme_option_menu.grid(row=1, column=1)

    # Root mainloop
    root.mainloop()

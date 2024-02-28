# Contains main menu function

# Importing dependencies
from App.FFLib.custom_sarc import Sarc
from App.AppLib.config import Config
import customtkinter as ctk
from App.FFLib.AINB import AINB
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import pygments.lexers.data
from tkinter import ttk
import chlorophyll
import zstandard
import os.path
import pathlib
import oead

# Supported file formats variable
supportedFileFormats = (
    (
        'All Editable Files', [
            '*.ainb'
        ]
    ),
    ('AI Node Binary', '*.ainb')
)


# _func class
class _Func:
    @staticmethod
    def update_ainb_editor(variables):

        if variables["open_file"] is None:
            variables["CodeBox"].delete(0.0, "end")
            return 0

        CodeBox = variables["CodeBox"]
        CodeBox.delete(0.0, "end")
        file = AINB(variables["open_file"], 'fp')
        CodeBox.insert(0.0, file.json)

    @staticmethod
    def focus_in_romfs_entry(romfs_path_label, event=None):
        romfs_path_label.configure(
            text="Game Dump Location*                                                                      "
        )

    @staticmethod
    def update_romfs_entry(app, romfs_path_entry, romfs_path_label, event=None):
        romfs_path = romfs_path_entry.get()
        app.settings["romfs_path"] = romfs_path
        Config.overwrite_setting("romfs_path", romfs_path)
        romfs_path_label.configure(
            text="Game Dump Location                                                                        "
        )

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
    def drop_file(tabview, variables, event=None):
        variables["open_file"] = str(event.data[1:len(event.data)-1])

        if variables["open_file"] is not None:
            continueQuitPopup = messagebox.askokcancel(
                title="AINB-Toolbox Popup",
                message="Opening this file will get rid of the last file you were editing.\nDo you want to continue?"
            )

            if continueQuitPopup is False:
                return 0

        _Func.update_ainb_editor(variables)
        tabview.set("AINB Editor")


# Button func
class ButtonFunc:
    @staticmethod
    def open_ainb_button_command():
        pass  # TODO: Stub

    @staticmethod
    def save_ainb_button_command(variables, code_view):

        # Asking out filepath if there is no file
        if variables["open_file"] is None:
            messagebox.showinfo("AINB-Toolbox Pop-up", "Please select file path to save as.")
            variables["open_file"] = filedialog.asksaveasfile(
                title="Save as...",
                filetypes=(
                    ("AI Node Binary", "*ainb"),
                    ("All Files", "*")
                )
            ).name

        # Getting the code_contents
        code_contents = code_view.get("1.0", "end-1c")

        # Converting the file
        ainb_data = AINB.json_to_ainb(code_contents)

        # Message pop-up
        continuePopup = messagebox.askokcancel(
            "AINB-Toolbox Pop-up",
            "Saving will overwrite the file, do you want to continue?"
        )

        # Quiting or continuing based on the pop-up outcome
        if continuePopup is False:
            return 0

        # Writing file
        with open(variables["open_file"], "wb") as f_out:
            f_out.write(ainb_data)

        # Output Pop-up
        messagebox.showinfo("AINB-Toolbox Pop-up", "Export successful!\nFile Exported to: " + variables["open_file"])

    @staticmethod
    def export_ainb_button_command(code_view):

        # Asking out filepath
        messagebox.showinfo("AINB-Toolbox Pop-up", "Please select file path to save as.")
        path_out = filedialog.asksaveasfile(
            title="Save as...",
            filetypes=(
                ("AI Node Binary", "*ainb"),
                ("All Files", "*")
            )
        ).name

        # Getting the code_contents
        code_contents = code_view.get("1.0", "end-1c")

        # Converting the file
        ainb_data = AINB.json_to_ainb(code_contents)

        # Writing file
        with open(path_out, "wb") as f_out:
            f_out.write(ainb_data)

        # Output Pop-up
        messagebox.showinfo("AINB-Toolbox Pop-up", "Export successful!\nFile Exported to: " + path_out)

    @staticmethod
    def tabview_command(variables):
        _Func.update_ainb_editor(variables)

    @staticmethod
    def romfs_path_browse_button_command(app, romfs_path_entry):
        romfs_path = filedialog.askdirectory(title="Select Tears of the Kingdom RomFS Folder")
        if romfs_path == "":
            return 0
        else:
            app.settings["romfs_path"] = romfs_path
            Config.overwrite_setting("romfs_path", romfs_path)
            romfs_path_entry.delete(0, "end")
            romfs_path_entry.insert(0, romfs_path)

    @staticmethod
    def export_all_ainb_button_command(romfs_path):

        counter = 0

        messagebox.showinfo("AINB-Extract-Tool Version 1.0", "Please select your output path")
        output_folder = filedialog.askdirectory(title="Output export directory")

        if output_folder == "":
            return 0

        toplevel = ctk.CTkToplevel()

        progressbar = ttk.Progressbar(master=toplevel, orient='horizontal', mode='determinate', length=200)
        progressbar.pack(side="top")
        progressbar.start()
        progressLabel = ctk.CTkLabel(master=toplevel, text="0%")
        progressLabel.pack(side="top")

        if not os.path.exists(output_folder + "/AI"):
            os.mkdir(output_folder + "\\AI")

        for file in os.listdir(romfs_path + "\\Pack\\Actor"):

            decom = zstandard.ZstdDecompressor(
                dict_data=zstandard.ZstdCompressionDict(Sarc.get_zsdic_data(".pack", romfs_path)))

            archive = oead.Sarc(
                decom.decompress(
                    pathlib.Path(
                        os.path.join(
                            romfs_path + "\\Pack\\Actor", file
                        )
                    ).read_bytes()
                )
            )

            for _file in archive.get_files():

                if _file.name.endswith(".ainb"):

                    with open(os.path.join(output_folder, _file.name), "wb") as outfile:
                        outfile.write(bytes(_file.data))

                    counter += 1
                    progressbar.step(1)
                    progressLabel.configure(text=str(counter / 131.42)[:4] + "%")
                    toplevel.update()

            messagebox.showinfo("AINB-Toolbox Pop-up",
                                "Extraction complete!\nExtracted to: " + output_folder)
            toplevel.destroy()

    @staticmethod
    def theme_option_menu_button_command(app, drag_and_drop_target, code_box, appearance):
        ctk.set_appearance_mode(appearance.lower())
        app.settings["current_theme"] = appearance.lower()
        Config.overwrite_setting("current_theme", appearance.lower())

        # Drag and drop label appearance
        if ctk.get_appearance_mode() == "Dark":
            drag_and_drop_target.configure(fg_color="#242424")
        else:
            drag_and_drop_target.configure(fg_color="#EBEBEB")

        # Code editor appearance
        if ctk.get_appearance_mode() == "Dark":
            code_box.configure(color_scheme="monokai")
        else:
            code_box.configure(color_scheme="ayu-light")

    @staticmethod
    def drag_and_drop_button_command(tabview, variables, event=None):

        fp = filedialog.askopenfile(title="Select a file", filetypes=supportedFileFormats)

        if fp is None:
            return 1

        if variables["open_file"] is not None:
            continueQuitPopup = messagebox.askokcancel(
                title="AINB-Toolbox Popup",
                message="Opening this file will get rid of the last file you were editing.\nDo you want to continue?"
            )
            if continueQuitPopup is False:
                return 0

        variables["open_file"] = fp.name

        _Func.update_ainb_editor(variables)
        tabview.set("AINB Editor")


# main_menu function
def main_menu(app):

    # Detecting if the romfs_path is None
    if app.settings["romfs_path"] is None:

        # Asking user to provide romfs path
        continue_prompt = False
        while continue_prompt is False:
            messagebox.showinfo("AINB-Toolbox Pop-up", "Please select your romfs folder.")
            romfs_folder = filedialog.askdirectory(title="Select RomFS Folder Path")
            if romfs_folder == "":
                message = """Do you want to continue without a romfs dump?
This will most likely cause a lot of errors in the future."""
                continue_prompt = messagebox.askyesno(
                    "AINB-Toolbox Pop-up", message)
            else:
                app.settings["romfs_path"] = romfs_folder
                Config.overwrite_setting("romfs_path", romfs_folder)
                continue_prompt = True

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating variables
    variables = {
        "open_file": None
    }

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
    tabview_command = partial(ButtonFunc.tabview_command, variables)
    tabview.configure(command=tabview_command)
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
                                     text="Click here to open file",
                                     corner_radius=10, wraplength=300)
    if ctk.get_appearance_mode() == "Dark":
        dragAndDropTarget.configure(fg_color="#242424")
    else:
        dragAndDropTarget.configure(fg_color="#EBEBEB")
    dragAndDropTarget.pack(expand=True, fill=ctk.BOTH, padx=40, pady=40)

    drag_and_drop_button_command = partial(ButtonFunc.drag_and_drop_button_command, tabview, variables)
    dragAndDropTarget.bind("<1>", drag_and_drop_button_command)

    export_all_ainb_button_partial = partial(ButtonFunc.export_all_ainb_button_command, app.settings["romfs_path"])
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

    root.columnconfigure(0)
    root.columnconfigure(1)

    romfs_path_label = ctk.CTkLabel(
        master=tabview.tab("Settings"),
        text="Game Dump Location                                                                        ",
        corner_radius=5, fg_color="#3B8ED0"
    )
    romfs_path_label.grid(row=0, column=0, padx=20, pady=10)

    romfs_path_entry = ctk.CTkEntry(master=tabview.tab("Settings"))
    if app.settings["romfs_path"] is None:
        romfs_path_entry.configure(placeholder_text="Eg. (D:\\Tears of the Kingdom\\romfs)")
    else:
        romfs_path_entry.insert(0, app.settings["romfs_path"])
    romfs_path_entry.grid(row=0, column=1, padx=20, pady=10)
    romfs_path_entry_command_partial = partial(_Func.update_romfs_entry, app, romfs_path_entry, romfs_path_label)
    romfs_path_entry_focus_partial = partial(_Func.focus_in_romfs_entry, romfs_path_label)
    romfs_path_entry.bind("<Return>", romfs_path_entry_command_partial)
    romfs_path_entry.bind("<Key>", romfs_path_entry_focus_partial)

    romfs_browse_command = partial(ButtonFunc.romfs_path_browse_button_command, app, romfs_path_entry)
    romfs_path_browse = ctk.CTkButton(
        tabview.tab("Settings"),
        text="Browse...", fg_color="grey",
        command=romfs_browse_command,
    )
    romfs_path_browse.grid(row=0, column=3)

    theme_label = ctk.CTkLabel(
        master=tabview.tab("Settings"),
        text="Current Theme                                                                                    ",
        corner_radius=5, fg_color="#3B8ED0"
    )
    theme_label.grid(row=1, column=0, padx=20, pady=10)

    # Moved command assignment to line
    theme_option_menu = ctk.CTkOptionMenu(
        master=tabview.tab("Settings"),
        values=["Dark", "Light", "System"],
    )
    _Func.update_theme_option_menu(theme_option_menu)
    theme_option_menu.grid(row=1, column=1, padx=20, pady=10)

    #
    #
    #
    #
    #                      ###############################
    #                      #    "AINB Editor" SECTION    #
    #                      ###############################

    # Creating and configuring the CodeView
    CodeBox = chlorophyll.CodeView(
        master=tabview.tab("AINB Editor"), lexer=pygments.lexers.data.JsonLexer, height=1000,
    )
    if ctk.get_appearance_mode().lower() == "dark":
        CodeBox.configure(color_scheme="monokai")
    else:
        CodeBox.configure(color_scheme="ayu-light")
    CodeBox.pack(fill="both", pady=50)
    variables["CodeBox"] = CodeBox

    # Creating open button
    open_ainb_button_command = partial(ButtonFunc.open_ainb_button_command)
    open_ainb_button = ctk.CTkButton(master=tabview.tab("AINB Editor"), text="Open",
                                     command=open_ainb_button_command)
    open_ainb_button.place(x=0, y=0)

    # Creating save button
    save_ainb_button_command = partial(ButtonFunc.save_ainb_button_command, variables, CodeBox)
    save_ainb_button = ctk.CTkButton(master=tabview.tab("AINB Editor"), text="Save",
                                     command=save_ainb_button_command)
    save_ainb_button.place(x=150, y=0)

    # Creating export button
    export_ainb_button_command = partial(ButtonFunc.export_ainb_button_command, CodeBox)
    export_ainb_button = ctk.CTkButton(master=tabview.tab("AINB Editor"), text="Export",
                                       command=export_ainb_button_command)
    export_ainb_button.place(x=300, y=0)

    # Updating to ainb_editor
    _Func.update_ainb_editor(variables)

    # SETTINGS MENU STUFF
    # Assigning theme_option_menu_command
    theme_option_menu_command = partial(ButtonFunc.theme_option_menu_button_command, app, dragAndDropTarget, CodeBox)
    theme_option_menu.configure(command=theme_option_menu_command)

    # Root mainloop
    root.mainloop()

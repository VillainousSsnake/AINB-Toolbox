# App/AINB-Toolbox.py
# Holds main program code

# Importing modules
from App.AppLib.app import App
from App.AppLib.index import Index

# Creating App
app = App()

# Main loop
while app.returnStatement != "exit":

    match app.returnStatement:
        case "main":
            Index.main_menu(app)

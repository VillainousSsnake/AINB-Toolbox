# App/AppLib/index.py
# Contains GUI index

# Importing GUI
from App.GUI.main_menu import main_menu as _main_menu


# Index class (Holds menu functions)
class Index:
    @staticmethod
    def main_menu(self):
        _main_menu(self)

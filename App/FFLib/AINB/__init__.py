# AINB library
from App.FFLib.AINB import converter as conv


# AINB class
class AINB:
    def __init__(self, input_, mode='d'):
        match mode:
            case 'd':
                self.data = input_
                self.json = conv.ainb_to_json(input, mode)

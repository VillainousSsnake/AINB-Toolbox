# AINB library
from App.FFLib.AINB import converter as conv


# AINB class
class AINB:
    def __init__(self, input_, mode='d'):

        match mode:

            case 'd':

                self.data = input_
                self.json = conv.ainb_to_json(input_, 'd')

            case 'fp':

                with open(input_, "rb") as f_in:
                    self.data = f_in.read()

                self.json = conv.ainb_to_json(self.data, 'd')

    def json_to_ainb(self, input_, mode='d'):

        match mode:

            case 'd':

                pass  # TODO: Stub

            case 'fp':

                pass  # TODO: Stub

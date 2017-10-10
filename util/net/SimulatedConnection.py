import util.miscellaneous as misc

from util.net.Connection import Connection
from control.agent.Agent import Agent


class SimulatedConnection(Connection):

    def __init__(self):
        Connection.__init__(self)

        # The simulated input stream received from others agents
        # self.SIMULATED_INPUT = []

    def send(self, message, address):
        address.cnn.BUFFER.append(message)

    '''
    def receive(self):
        for m in self.SIMULATED_INPUT:
            self.BUFFER.append(m)
        del self.SIMULATED_INPUT[:]
    '''

    def to_string(self, indent_1: int, indent_2 : int):
        indent_str_1 = misc.indent(indent_1)
        indent_str_2 = misc.indent(indent_2)

        super(self).to_string(indent_1, indent_2)
        print(indent_str_1 + "SimulatedConnection:\n",
              indent_str_2 + "Number of SIMULATED_INPUT elements:", "\n")


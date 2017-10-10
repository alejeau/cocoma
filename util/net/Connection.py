import util.miscellaneous as misc

from abc import ABC, abstractmethod

class Connection(ABC):

    def __init__(self):
        # The buffer where the connection writes the received messages.
        self.BUFFER = []

    def get_buffer_and_flush(self) -> list:
        answer = self.BUFFER[:]
        del self.BUFFER[:]

        return answer

    @abstractmethod
    def send(self, message, address):
        pass

    '''
    @abstractmethod
    def receive(self):
        pass
    '''

    def to_string(self, indent_1: int, indent_2 : int):
        indent_str_1 = misc.indent(indent_1)
        indent_str_2 = misc.indent(indent_2)
        print(indent_str_1 + "Connection:\n",
              indent_str_2 + "Number of BUFFER elements:", len(self.BUFFER),
              "\n")


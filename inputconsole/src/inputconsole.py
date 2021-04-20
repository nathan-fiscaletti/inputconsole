import time
from threading import Thread
import sys
import readchar

class InputConsole():
    """
    A console will present output like a normal terminal would, but it
    will maintain an input line that is always present at the bottom
    of the output.
    """
    def __init__(self):
        self.__old_stdout=sys.stdout
        self.__input_string = ''
        self.__prompt = '> '
        self.__unknown_command_handler = None
        self.commands = {}

    def write(self, text):
        """
        Writes a message to the console output.
        """
        output = '\r\033[K' + text.rstrip('\n') + '\n'
        output = output + '\r' + self.__prompt
        output = self.__parse_input_string(output)

        self.__old_stdout.write(output)
        self.__old_stdout.flush()

    def listen_for_input(self, prompt='> '):
        """
        Listens for input with the specified prompt.
        """
        Thread(target=self.__input_thread, args=[prompt]).start()

    def register_command(self, name, action):
        """
        Registers a command.
        """
        self.commands[name] = action

    def set_unknown_command_handler(self, handler):
        """
        Sets the handler for unknown commands. Handler should return
        a boolean and take one parameter containing the full input
        text of the command. The boolean response value indicates
        whether or not the command was processed. True means it was
        processed, False mean sit was not.
        """
        self.__unknown_command_handler = handler

    def __parse_input_string(self, prefix):
        printable_input_string = self.__input_string
        input_string_components = self.__input_string.split()

        if len(input_string_components) > 0:
            space_char = ''
            if len(input_string_components) > 1:
                space_char = ' '

            if input_string_components[0] in self.commands:
                printable_input_string = (
                    '\033[92m' + input_string_components[0] +
                    '\033[0m' + space_char +
                    ' '.join(input_string_components[1:])
                )
            else:
                printable_input_string = (
                    '\033[91m' + input_string_components[0] +
                    '\033[0m' + space_char +
                    ' '.join(input_string_components[1:])
                )

            if self.__input_string.endswith(' '):
                printable_input_string = printable_input_string + ' '

        return prefix + printable_input_string

    def __input_thread(self, prompt):
        self.__prompt = prompt
        self.__old_stdout.write(prompt)
        self.__old_stdout.flush()
        while True:
            key = ''
            # Stop processing input characters once either Control+C
            # is pressed or Enter is pressed.
            while (key != readchar.key.ENTER and 
                   key != readchar.key.CTRL_C):
                key = readchar.readkey()

                # Handle backspace
                if key == readchar.key.BACKSPACE:
                    if self.__input_string != '':
                        self.__input_string = self.__input_string[:-1]
                        self.__old_stdout.write('\b\033[K')

                # Cancel out arrow keys
                elif (key == readchar.key.UP or 
                     key == readchar.key.DOWN or
                     key == readchar.key.LEFT or
                     key == readchar.key.RIGHT):
                    self.__old_stdout.write('\033[C')

                # Handle general characters
                else:
                    self.__input_string = self.__input_string + key

                self.__old_stdout.write(
                    self.__parse_input_string('\r' + self.__prompt)
                )
                self.__old_stdout.flush()

            # If Control+C was pressed, quit.
            if key == readchar.key.CTRL_C:
                quit()

            # Assume enter was pressed and process the command
            if key == readchar.key.ENTER:
                ret = self.__input_string
                ch = ''
                self.__input_string = ''
                self.__handle_command(ret.rstrip('\n\r'))

    def __handle_command(self, command):
        command_components = command.split()
        command_name = command_components[0]

        if command_name in self.commands:
            try:
                self.commands[command_name](command_components[1:])
            except Exception as e:
                self.write(
                    "Failed to run command '{0}': {1}".format(
                        command_name, e
                    )
                )
        else:
            if self.__unknown_command_handler is not None:
                if self.__unknown_command_handler(command):
                   return
            self.write("Unknown command: {0}\n".format(command)) 

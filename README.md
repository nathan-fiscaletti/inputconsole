# InputConsole
> **InputConsole** is a console for Python that will keep all output above the input line without interrupting the input line.

```shell
$ pip3 install inputconsole
```

[![PyPI version](https://badge.fury.io/py/inputconsole.svg)](https://badge.fury.io/py/inputconsole)
[![Downloads](https://pepy.tech/badge/inputconsole)](https://pepy.tech/project/inputconsole)
[![GitHub issues](https://img.shields.io/github/issues/nathan-fiscaletti/inputconsole.svg)](https://github.com/nathan-fiscaletti/inputconsole/issues)
[![GitHub license](https://img.shields.io/github/license/nathan-fiscaletti/inputconsole.svg)](https://github.com/nathan-fiscaletti/inputconsole/blob/master/LICENSE)

![Demo](./demo.gif)

## Example

```py
from inputconsole import InputConsole

# Create the console
console = InputConsole()

# Register a command
def help(args):
    console.write("I don't want to help you {0}.\n".format(args[0]))
console.register_command('help', help)

# Set unknown command handler, Return 'True' for command handled or
# 'False' for command not handled.
def unknown_command_handler(command):
    console.write("Unknown command: " + command)
    return True
console.set_unknown_command_handler(unknown_command_handler)

# Start listening for input on a new thread
# Input line will always stay at the bottom
console.listen_for_input()

# Generate random output to keep the output thread active.
def steady_flow():
    num = 0
    while True:
        console.write("this is an output message: {0}\n".format(num))
        time.sleep(2)
        num += 1
t = Thread(target=steady_flow)
t.start()
t.join()
```
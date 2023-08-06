__author__ = "Henning Schmitz"

import sys

def command_line_input():
    """
    Python script can be run from the command line with a given input.
    :return: The given input is returned.
    """
    if len(sys.argv) >= 2:
        input = sys.argv[1]
    else:
        print('No input value is given.')

    return input
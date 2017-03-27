#! /usr/bin/env python

import sys, csv

def main(argv):
    # Verify correct input file given
    fname = validate_input(argv)

    # Open file, read lines into a list
    with open(fname) as f:
        input_file = f.read()


def validate_input(argv):
    if len(argv) == 2 and argv[1][-4:] == '.asc':
        return argv[1]
    else:
        sys.exit('ERROR: Please provide one valid argument file')


if __name__ == '__main__':
    main(sys.argv)


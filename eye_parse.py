#! /usr/bin/env python

from __future__ import print_function
import sys, csv

def main(argv):
    # Verify correct input file given
    fname = validate_input(argv)

    # Open file, read lines into a list
    with open(fname) as f:
        input_file = f.read()

    # Put each trial in a dict
    trials = get_trials(input_file)


def validate_input(argv):
    ''' Ensure input argument is only argument provided and has .asc extension
    '''
    if len(argv) == 2 and argv[1][-4:] == '.asc':
        return argv[1]
    else:
        sys.exit('ERROR: Please provide one valid argument file')


def get_trials(ip_file):
    trials = []
    # Get list of trials, each trial is long string
    trials_raw = ip_file.split('START\t')[1:]

    # Split each trial_raw trial from one string into lines
    for i, trial in enumerate(trials_raw):
        trials_raw[i] = trial.splitlines()

    # Split each trial line into a list of words
    for trial in trials_raw:
        for i, line in enumerate(trial):
            trial[i] = line.split()

        END_line = get_END_line(trial)

        # Use Constant offsets from END_line number to extract TRIAL_VAR data

        # and add it to a dictionary

        # If RESPONSE is CORRECT, look for DRAW_LIST

        # Get timestamp of DRAW_LIST line

    return trials


def get_END_line(trial):
    ''' Finds the first line where the first word is 'END'.


    Args:
        trial: Nested list, each line split into list of words.

    Returns:
        Returns the line number of first 'END' encountered.
    '''
    END_line = -1
    # Find 'END' and get line number
    for line_num, line in enumerate(trial):
        if 'END' in line[0]:
            END_line = line_num 
            break
    return END_line


if __name__ == '__main__':
    main(sys.argv)


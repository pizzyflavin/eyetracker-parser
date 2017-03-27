#! /usr/bin/env python

from __future__ import print_function
import sys, csv

# Constant Offset Values
TRIAL_OFFSET =      2
TYPE_OFFSET =       3
PRACTICE_OFFSET =   4
IMAGE_OFFSET =      5
LETTER_OFFSET =     6
LOCATIONID_OFFSET = 7
LOCATION_OFFSET =   8
EXPECTED_OFFSET =   9
INDEX_OFFSET =      10
KEYPRESS_OFFSET =   11
RESPONSE_OFFSET =   12
RT_OFFSET =         13
DISPTIME_OFFSET =   14
KEYRESP_OFFSET =    15
SOA_OFFSET =        16
SACCADE_OFFSET =    17

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
        try:
            trial_dict = {
                    'trial':        trial[END_line + TRIAL_OFFSET][5],
                    'trial_type':   trial[END_line + TYPE_OFFSET][5],
                    'practice':     trial[END_line + PRACTICE_OFFSET][0],
                    'image':        trial[END_line + IMAGE_OFFSET][5],
                    'letter':       trial[END_line + LETTER_OFFSET][5],
                    'locationid':   trial[END_line + LOCATIONID_OFFSET][5],
                    'location':     trial[END_line + LOCATION_OFFSET][5:],
                    'expected':     trial[END_line + EXPECTED_OFFSET][5],
                    'TRIAL_INDEX':  trial[END_line + INDEX_OFFSET][5],
                    'KEYPRESS':     trial[END_line + KEYPRESS_OFFSET][5],
                    'RESPONSE':     trial[END_line + RESPONSE_OFFSET][5],
                    'RT':           trial[END_line + RT_OFFSET][5],
                    'DISP_ON_TIME': trial[END_line + DISPTIME_OFFSET][5],
                    'KEY_RESP_TIME':trial[END_line + KEYRESP_OFFSET][5],
                    'soa':          trial[END_line + SOA_OFFSET][5],
                    'SACCADE_RT':   trial[END_line + SACCADE_OFFSET][5]
                    }
            # Add newly created dict to trials list
            trials.append(trial_dict)

        except NameError:
            print('Error adding dict entries. Make sure END_line has value.')
        except IndexError:
            print('Check that "trial" has been split appropriately')
            print('(i.e. "trial" is a list of lines, each of which has been'
                    'split into a list of words.)')

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


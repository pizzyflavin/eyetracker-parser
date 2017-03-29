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
    input_file = validate_input(argv)

    # Get desired data from each trial
    trials = get_trials(input_file)

    # Load data into a csv file
    keys = ['trial',
            'trial_type',
            'practice',
            'image',
            'IMG_DISP_TIME',
            'letter',
            'locationid',
            'location',
            'expected',
            'TRIAL_INDEX',
            'KEYPRESS',
            'RESPONSE',
            'RT',
            'DISP_ON_TIME',
            'KEY_RESP_TIME',
            'soa',
            'SACCADE_RT']

    with open(input_file[:-4] + '_data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(keys)
        for trial_dict in trials:
            data = []
            for key in keys:
                data.append(trial_dict[key])
            writer.writerow(data)

def validate_input(argv):
    ''' Ensure input argument is only argument provided and has .asc extension
    '''
    if len(argv) == 2 and argv[1][-4:] == '.asc':
        return argv[1]
    else:
        sys.exit('ERROR: Please provide one valid argument file')


def get_trials(fname):
    ''' Extract trial information from raw text input file


    Args:
        ip_file: string representation of a .asc output file from an
            eyetracker machine.

    Returns:
        Returns a list of trial dictionaries
    '''
    # Open file, read lines into a list
    with open(fname) as f:
        input_file = f.read()

    trials_list = []
    # Get list of trials, each trial is long string
    trials_raw = input_file.split('START\t')[1:]

    # Split each trial_raw trial from one string into lines
    for i, trial in enumerate(trials_raw):
        trials_raw[i] = trial.splitlines()

    # Split each trial line into a list of words
    for i, trial in enumerate(trials_raw):
        for j, line in enumerate(trial):
            trial[j] = line.split()

        # Add trial to dict
        current_dict = trial_to_dict(trial, trials_list)

        # Look for DRAW_LIST. If there, get timestamp
        DRAW_line = get_line('DRAW_LIST', trial)
        if DRAW_line:
            timestamp = trial[DRAW_line][1]
            # Add timestamp to trial dict
            current_dict['IMG_DISP_TIME'] = timestamp
        else:
            current_dict['IMG_DISP_TIME'] = None
    return trials_list


def trial_to_dict(trial, trial_list):
    ''' Put trial into dictionary, and add dictionary to list argument.


    Args:
        trial:      Trial to put in dictionary, expects list of lines, each
            line is a list of words from that line.
        trial_list: List to which trial will be appended
    Returns:
        trial_dict: newly created dictionary
    '''
    END_line = get_line('END', trial)
    # Use Constant offsets from END_line number to extract TRIAL_VAR data
    # and add it to a dictionary
    try:
        trial_dict = {
                'trial':        trial[END_line + TRIAL_OFFSET][5],
                'trial_type':   trial[END_line + TYPE_OFFSET][5],
                'practice':     trial[END_line + PRACTICE_OFFSET][5],
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
        trial_list.append(trial_dict)
        return trial_dict
    except NameError:
        print('Error adding dict entries. Make sure END_line has value.')
    except IndexError:
        print('Check that "trial" has been split appropriately')
        print('(i.e. "trial" is a list of lines, each of which has been'
                'split into a list of words.)')


def get_line(pattern, trial):
    ''' Finds the first line containing <pattern>.


    Args:
        trial: Nested list, each line split into list of words.
        pattern: String to look for
    Returns:
        pattern_line_num: first line containing <pattern>
            or False if not found
    '''
    # Find pattern and get line number
    pattern_line_num = False
    for line_num, line in enumerate(trial):
        if pattern in line:
            pattern_line_num = line_num
            break;
    return pattern_line_num



if __name__ == '__main__':
    main(sys.argv)


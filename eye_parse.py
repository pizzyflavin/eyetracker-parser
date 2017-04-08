#! /usr/bin/env python

from __future__ import print_function
import sys, csv

# Constant Definitions
MISSING_VAL = None

# Constant Offset Values
offsets = {
        'trial':            2,
        'trial_type':       3,
        'practice':         4,
        'image':            5,
        'IMG_DISP_TIME':    0,
        'letter':           6,
        'locationid':       7,
        'location':         8,
        'expected':         9,
        'TRIAL_INDEX':      10,
        'KEYPRESS':         11,
        'RESPONSE':         12,
        'RT':               13,
        'DISPLAY_ON_TIME':  14,
        'KEY_RESPONSE_TIME':15,
        'soa':              16,
        'SACCADE_RT':       17,
        'TRIAL_RESULT':     18
}

# Column headers
columns = [
        'trial',
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
        'DISPLAY_ON_TIME',
        'KEY_RESPONSE_TIME',
        'soa',
        'SACCADE_RT',
        'TRIAL_RESULT',
        'AVG_PUPILDIAM_DIFF'
]


def main(argv):
    # Verify correct input file given
    input_file = validate_input(argv)

    # Get desired data from each trial
    trials = get_trials(input_file)

    # Load data into a csv file
    with open(input_file[:-4] + '_data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(columns)
        for trial_dict in trials:
            data = []
            for column in columns:
                data.append(trial_dict[column])
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
            current_dict['IMG_DISP_TIME'] = MISSING_VAL
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
    # Build list of keys for trial dict
    keys = columns
    missing_keys = []
    # Check for errors in trial
    error = error_check(trial)
    if error:
        err_num = error
        keys = columns[:-err_num]
        missing_keys = columns[-err_num:]

    trial_dict = {}
    # Pair keys and values
    for key in keys:
        line = trial[END_line + offsets[key]]
        if key in line:
            # Special case, data in different format
            if key == 'TRIAL_RESULT':
                value = line[3]
            # Normal data format
            else:
                value = line_to_val(line)
            trial_dict[key] = value
    if missing_keys:
        # If missing keys, pair with none and add to trial_dict
        for key in missing_keys:
            trial_dict[key] = MISSING_VAL

    # Add newly created dict to trials list
    trial_list.append(trial_dict)
    return trial_dict


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
        line_str = ' '.join(line)
        if line_str.find(pattern) >= 0:
            pattern_line_num = line_num
            break;
    return pattern_line_num


def error_check(trial):
    ''' Determines if an error occured during data collection in a trial, and
    if so returns the number of lost messages.

    Args:
        trial: Nested list of lines, each line split into list of words.
    Returns:
        error: The number of messages lost if error found, otherwise False
    '''
    error = False
    err_line = get_line('ERROR MESSAGES LOST', trial)
    if err_line:
        error = int(trial[err_line][5])
    return error


def line_to_val(line):
    size = len(line)
    # If standard format, just return last string in line
    val = line[5]
    # If non-standard, add extra data
    if size > 6:
        for i in range(6, size):
            val = val + line[i]
    return val


if __name__ == '__main__':
    main(sys.argv)


#! /usr/bin/env python

import sys, csv

def main(fname):
    # Open file, read lines into a list
    with open(fname) as f:
        file_lines = f.read().splitlines()

    image_access = [[], []]

    # Search for keywords
    for line in file_lines:
        word_list = line.split()
        if 'DRAW_LIST' in word_list:
            image_access[0].append(word_list[1])
        if 'image' in word_list:
            image_access[1].append(word_list[5])

    # Write timestamp and image_name lists to csv file
    with open((fname[:-4] + '_data.csv'), 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(image_access)

if __name__ == '__main__':
    main(sys.argv[1])


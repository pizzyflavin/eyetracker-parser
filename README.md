# Eyetracker Parser

This project is for analyzing data from an eye-tracking machine that a friend
was using for a grad school assignment.

An experiment was performed on several subjects in order to determine the
effect of startling images on pupil diameter (I'm sure for some good reason).

### WHAT IT DOES
The eye_parse.py script takes an .asc file as an input and parses it for
relevant sample data. This data is then put into a .csv file for your further
analysis (My friend just wanted .csv files instead of these .asc files).

### HOW TO USE IT
In order to use this software, you first need to generate the .asc files output
by the proprietary eye-tracking machine. Then run the following in your
terminal while in the project:  
`./eye_parse.py <file>.asc`  
You should now have a csv file that presents the sample data to you in
a non-proprietary format.

Test data is located in `external/test_data/`

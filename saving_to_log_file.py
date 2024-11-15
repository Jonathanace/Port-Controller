import os
from datetime import datetime
import pytz

# Saves a string of text to a logfile in the following format: Month Day Year Time Text

def save_to_logfile(event: str):

    pst_timezone = pytz.timezone("America/Los_Angeles")
    date = datetime.now(pst_timezone)
    current_date_pst = date.date() #get current date

    curr_year = current_date_pst.year #get current year 

    filename = "logfile" + str(curr_year) + ".txt" #name of the logfile

    print(filename)

    with open(filename, 'a+', encoding='ascii') as file: # Open file and create if not already existing

        curr_time = date.strftime('%B %d %Y: %H:%M ') # get current date, time in year, month, day hour, minutes
        file.write(curr_time + event + '\n') # Write timestamp + event onto logfile 

        file.close() #  close file

    
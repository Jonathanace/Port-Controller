import os
from datetime import datetime
import pytz

def save_to_logfile(comment: str):

    pst_timezone = pytz.timezone("America/Los_Angeles")
    current_date_pst = datetime.now(pst_timezone).date() #get current date

    curr_year = current_date_pst.year #get current year 

    filename = "logfile" + str(curr_year) + ".txt" #name of the logfile

    print(filename)

    with open(filename, 'a+') as file:
        file.write("Testing")

        file.close()

    

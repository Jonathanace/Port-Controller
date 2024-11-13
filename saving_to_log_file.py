import os
import datetime
import pyzt

def save_to_logfile(comment: str):

    pst_timezone = pyzt.timezone("America/Los Angeles")
    current_date_pst = datetime.now(pst_timezone).date() #get current date

    curr_year = current_date_pst.year #get current year 

    filename = "logfile" + str(curr_year) + ".txt" #name of the logfile

    with open(filename, 'a') as file:
        file.write("Testing")

    

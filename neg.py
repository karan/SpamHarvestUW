################# Imports ###########################
import csv
import matplotlib.pylab as plt
from datetime import datetime
import os
################# Imports ###########################

################# Main ###########################
if __name__ == '__main__':
    
    print 'Loading csv dump file..'
    # full_dump.csv
    # Rows: Email, Posted, Received, From, Subject, Clickable, Anchored, Obfuscation, Platform, Notes
    data = csv.reader(open('full_dump.csv', 'r')) # load the dump
    next(data, None) # skip the headers
    
    print 'Starting to build the dict...'
    for num, row in enumerate(data): # iterate over the data
        posted = row[1] # get posted date
        received = row[2][:-12] # get received date, slice to ignore the UTC offset
        posted_fmt = '%m/%d/%Y %H:%M' # format of the timestamp
        rec_fmt = '%a, %d %b %Y %H:%M:%S' # format of the timestamp
        
        # parse the timestamps as datetime objects
        posted_date = datetime.strptime(posted, posted_fmt) 
        rec_date = datetime.strptime(received, rec_fmt)
        
        tdelta = rec_date - posted_date # gets the time difference in seconds
        hours = tdelta.total_seconds() / 60 / 60 # convert to hours

        if hours < 0:
            print '%d --> %s' % (hours, row[0])
################# Main ###########################

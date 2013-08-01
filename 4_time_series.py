################# Imports ###########################
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.dates as mdates
import os
################# Imports ###########################


################# Methods ###########################
def plot_series(x, y):
    fig, ax = plt.subplots()
    ax.plot_date(x, y, fmt='g--')
    
    fig.autofmt_xdate()
    plt.title("Email spam time series")
    plt.ylabel("Number of emails")
    plt.grid(True)
    plt.tight_layout()
    create_folder("time_series")
    fig = plt.gcf() # return reference to current figure
    fig.set_size_inches(20,14)
    plt.savefig('time_series/weekly.png', format='png', dpi=100)
    plt.show()

def create_folder(name):
    """
    Creates a new directory with the passed name if it
    doesn't exist.
    """
    if not os.path.exists(name):
        os.makedirs(name)
################# Methods ###########################


################# Main ###########################
if __name__ == '__main__':
    print 'Loading csv dump file..'
    data = csv.reader(open('full_dump.csv', 'r')) # load the dump
    next(data, None) # skip the headers
    
    date_to_emails = defaultdict(int) # maps a date to num of emails received on the date
    
    for num, row in enumerate(data): # iterate over the data
        received = row[2][5:-21] # get received date only
        rec_fmt = '%d %b %Y' # format of the timestamp
        rec_date = mdates.date2num(datetime.strptime(received, rec_fmt)) # parse the timestamps as datetime objects
        date_to_emails[rec_date] += 1
    
    
    x = list(date_to_emails.keys()) # the dates
    y = list(date_to_emails.values()) # num of emails
    
    plot_series(x, y)
    
################# Main ###########################
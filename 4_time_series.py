################# Imports ###########################
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.dates as mdates
from matplotlib.dates import WeekdayLocator
from matplotlib.dates import DateFormatter
import os
################# Imports ###########################


################# Methods ###########################
def plot_series(x, y):
    """
    Buils a time series where:
    x = list of dates
    y = list on number of emails
    Interval is 2 weeks
    """
    fig, ax = plt.subplots()
    ax.plot_date(x, y, fmt='g-')
    
    # For tickmarks and ticklabels every week
    ax.xaxis.set_major_locator(WeekdayLocator(byweekday=1, interval=2))
    
    # For tickmarks (no ticklabel) every week
    ax.xaxis.set_minor_locator(WeekdayLocator(byweekday=1))
    
    # for some reason this is needed to get the month displayed too
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

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
    
def plot_hist(weeks_list):
    """
    Builds a histogram for weeks after which spam email was received.
    """
    plt.title('Number of emails after x weeks of posting')
    plt.xlabel('Weeks after posting')
    plt.ylabel('Number of emails')
    plt.hist(weeks_list, bins=60, alpha=0.5, histtype='bar')
    create_folder("time_series")
    fig = plt.gcf()
    fig.set_size_inches(20,14)
    plt.savefig('time_series/weekly_hist.png', format='png', dpi=100)
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
    weeks_list = [] # stores weeks after posting that email was received
    
    for num, row in enumerate(data): # iterate over the data
        posted = row[1]
        received = row[2][5:-21] # get received date only
        posted_fmt = '%m/%d/%Y %H:%M' # format of the timestamp
        rec_fmt = '%d %b %Y' # format of the timestamp
        posted_date = datetime.strptime(posted, posted_fmt) # parse the timestamps as datetime objects
        rec_date = datetime.strptime(received, rec_fmt) # parse the timestamps as datetime objects
        
        delta = rec_date - posted_date
        weeks = delta.total_seconds() / 60 / 60 / 24 / 7 # change seconds to weeks
        
        date_to_emails[mdates.date2num(rec_date)] += 1 # add received date to dict
        weeks_list.append(weeks)
    
    x = list(date_to_emails.keys()) # the dates
    y = list(date_to_emails.values()) # num of emails
    
    plot_series(x, y)
    
    plot_hist(weeks_list)
    
################# Main ###########################
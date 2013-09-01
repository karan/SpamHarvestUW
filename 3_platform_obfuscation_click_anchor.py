################# Imports ###########################
import csv
import matplotlib.pylab as plt
from datetime import datetime
import os
################# Imports ###########################


################# Methods ###########################
def plot_hist(plot_data, top_key):
    """
    Plots the passed plot_data[top_key] dict on a step histogram.
    """
    plot_data = plot_data[top_key]
    plt.title('Number of emails per week by ' + top_key)
    plt.xlabel('Spam emails per week')
    plt.ylabel('Frequency')
    for key in plot_data:
        plt.hist(plot_data[key], bins=20, alpha=0.5, histtype='step', label=key)
    plt.legend()
    create_folder(top_key)
    fig = plt.gcf()
    fig.set_size_inches(20,14)
    plt.savefig(top_key + '/hist.png', format='png', dpi=100)

def plot_box(plot_data, top_key):
    """
    Plots the passed plot_data[top_key] dict on a side by side
    box plot.
    """
    plot_data = plot_data[top_key]
    data = [list_of_weeks for list_of_weeks in plot_data.values()]
    plt.title('Spam emails per week by ' + top_key, fontsize=20)
    plt.boxplot(data)
    plt.xticks([(i + 1) for i in range(len(plot_data.values()))], \
                 ['%s' % i for i in plot_data.keys()], rotation=80)
    plt.tight_layout()
    create_folder(top_key)
    fig = plt.gcf() # return reference to current figure
    fig.set_size_inches(20,14)
    plt.savefig(top_key + '/box_plot.png', format='png', dpi=100)
    
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
    # full_dump.csv
    # Rows: Email, Posted, Received, From, Subject, Clickable, Anchored, Obfuscation, Platform, Notes
    data = csv.reader(open('full_dump.csv', 'r')) # load the dump
    next(data, None) # skip the headers
    
    # stores all the data
    plot_data = {
        'platform': {},
        'obfuscation': {}, 
        'clickable': {'yes': [], 'no': [], 'invalid': []},
        'anchored': {'yes': [], 'no': [], 'invalid': []}
    }
    
    print 'Starting to build the dict...'
    for num, row in enumerate(data): # iterate over the data
        platform = row[8].lower() # get platform for the email
        obfuscations = row[7].split(' | ') # get all obfuscations used as list
        clickable = row[5].lower() # get the clickable status
        anchored = row[6].lower() # get the anchored status
        
        posted = row[1] # get posted date
        received = row[2][:-12] # get received date, slice to ignore the UTC offset
        posted_fmt = '%m/%d/%Y %H:%M' # format of the timestamp
        rec_fmt = '%a, %d %b %Y %H:%M:%S' # format of the timestamp
        
        # parse the timestamps as datetime objects
        posted_date = datetime.strptime(posted, posted_fmt) 
        rec_date = datetime.strptime(received, rec_fmt)
        
        tdelta = rec_date - posted_date # gets the time difference in seconds
        weeks = tdelta.total_seconds() / 60 / 60 / 24 / 7 # convert to weeks
        
        
        # map the clickable status
        plot_data['clickable'][clickable].append(weeks)
        
        # map the clickable status
        plot_data['anchored'][anchored].append(weeks)

        # each platform is the key of dict, with values being list of weeks
        if platform in plot_data['platform']:
            plot_data['platform'][platform].append(weeks)
        else:
            plot_data['platform'][platform] = [weeks]
            
        # add all obfuscations to the list as well
        for obfuscation in obfuscations:
            if obfuscation in plot_data['obfuscation']:
                plot_data['obfuscation'][obfuscation].append(weeks)
            else:
                plot_data['obfuscation'][obfuscation] = [weeks]
        
        if num % 1000 == 0:
            print '\t%d rows parsed..' % num
    
    print 'All rows parsed and data loaded as a dict...'
    
    print 'Start making graphs..'
    for key in ['platform', 'obfuscation', 'clickable', 'anchored']:
        plt.figure()
        plot_hist(plot_data, key) # plot the histogram
        plt.figure()
        plot_box(plot_data, key) # plot the boxplot
        
    print 'All done!'
################# Main ###########################

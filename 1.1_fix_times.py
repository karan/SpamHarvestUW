################# Imports ###########################
import csv
from datetime import datetime
################# Imports ###########################

################# Main ###########################
if __name__ == '__main__':
    
    data = csv.reader(open('emails.csv', 'r')) # load the dump
    header = next(data, None) # skip the header

    posted_fmt = '%m/%d/%Y %H:%M' # format of the timestamp

    row1 = next(data, None)

    while True:
        row2 = next(data, None)
        if not row2: # EOF
            break
        posted1_date = datetime.strptime(row1[6], posted_fmt)
        posted2_date = datetime.strptime(row2[6], posted_fmt)
        if (posted2_date - posted1_date).total_seconds() == 90000:
                print '%d: %s and %s' % (data.line_num, row1[0], row2[0])

        row1 = row2
################# Main ###########################

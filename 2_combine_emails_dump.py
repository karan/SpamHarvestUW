"""
This script will combine the dump.csv and email.csv
files into a new full_dump.csv file which will have email
properties.

About 0.5% emails in the dump are not classified.
"""

import csv

# dump.csv
# Rows: Email, Timestamp, Timestamp, From, Subject
dump = csv.reader(open('dump.csv', 'r'))
next(dump, None)

output = csv.writer(open('full_dump.csv', 'wb'))
output.writerow(['Email', 'Posted', 'Received', 'From', 'Subject', \
                 'Clickable', 'Anchored', 'Obfuscation', \
                 'Platform', 'Notes'])

row_count = 0 # total number of rows
write_count = 0 # total number of rows written

for row in dump: # start iterating through the dump
    row_count += 1
    email = row[0] # the email address
    received = row[1] # timestamp the email was received
    From = row[3] # the 'sender'
    subject = row[4] # subject of the email
    
    emails = csv.reader(open('emails.csv', 'r'))
    next(emails, None)
    
    for e in emails: # iterate over the emails.csv file
        if e[0] == email: # if the emails match
            clickable = e[1] # was the email posted clickable
            anchored = e[2] # was it anchored
            obfuscation = e[3] # how was it obfuscated
            platform = e[4] # what platform was it posted on
            notes = e[5] # any notes
            posted = e[6] # timestamp of posting
    
    if email != '' and posted != '' and received != '' and \
       From != '' and clickable != '' and anchored != '' and \
       obfuscation != '' and platform != '':
        # write to the file only if we have all required data
        output.writerow([email, posted, received, From, \
                    subject, clickable, anchored, \
                    obfuscation, platform, notes])
        write_count += 1
        
    if write_count % 1000 == 0:
        print '%d done' % write_count
        
print '%d of %d have been written with a success rate of %.02f%%' % \
(write_count, row_count, (float(write_count) * 100 / float(row_count)))

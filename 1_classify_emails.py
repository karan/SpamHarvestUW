import csv
import pprint
import matplotlib.pyplot as plt

def plot(key, stats):
    """
    Plots the dict corresponding to the passed key name.
    """
    D = stats[key]
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), D.keys(), fontsize=10)
    plt.setp(plt.xticks()[1], rotation=90)
    plt.title('Percentage of emails for: ' + key)
    plt.xlabel('Made ' + key)
    plt.ylabel('Percentage of emails posted')
    plt.savefig('classify_graphs/%s.png' % key, bbox_inches='tight')
    
if __name__ == '__main__':
    data = csv.reader(open('emails.csv', 'r')) # Load the CSV
    next(data, None) # skip the header

    stats = {
        'clickable':{'yes':0, 'no':0, 'invalid':0},
        'anchored':{'yes':0, 'no':0, 'invalid':0},
        'obfuscation':{},
        'platform':{}
    }

    row_count = 0 # will be used to calculate percentages

    for row in data: # traverse over the rows
        row_count += 1
        ## Clickable ##
        stats['clickable'][row[1].lower()] += 1

        ## Anchor ##
        stats['anchored'][row[2].lower()] += 1

        ## Obfuscation ##
        obfuscations = row[3].split(' | ') # get a list of all obfuscations
        for obfuscation in obfuscations:
            if obfuscation in stats['obfuscation']:
                stats['obfuscation'][obfuscation] += 1
            else:
                stats['obfuscation'][obfuscation] = 1

        ## Platform ##
        if row[4] in stats['platform']:
            stats['platform'][row[4]] += 1
        else:
            stats['platform'][row[4]] = 1

    p = pprint.PrettyPrinter(indent=4)
    p.pprint(stats) # prints just the numbers

    for query in stats:
        for param in stats[query]:
            # change to percentages over total emails posted
            stats[query][param] = (stats[query][param] * 100) / row_count

    # p.pprint(stats) # print the percentages

    plot('clickable', stats)
    plot('anchored', stats)
    plot('obfuscation', stats)
    plot('platform', stats)

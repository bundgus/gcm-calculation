import csv

with open('EC Air Service Location Pairs With Distance Filtered.csv', 'w', newline='') as csvfileout:
    csvwriter = csv.writer(csvfileout, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerow(['Origin', 'Destination', 'Distance_Miles'])

    with open('EC Air Service Location Pairs With Distance.csv', newline='') as csvfilein:
        reader = csv.reader(csvfilein, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            print(row[0], row[1], float(row[6]))
            csvwriter.writerow([row[0], row[1], float(row[6])])
            quit()

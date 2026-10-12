# Monthly response time (incident creation to closing)  average per zipcode
# For all 2020 data, record response time (if incident closed) and number of complaints in a list, then add up and divide by list length
# Total up average for all 2020 data

import csv
from datetime import datetime, date
date_format = "%m/%d/%Y %I:%M:%S %p"
with open('data/311_Service_Requests_from_2010_to_Present_20250928.csv', 'r') as fi:
    reader = csv.reader(fi)
    header = next(reader)
    records = {} # have the zipcodes as keys, nested lists of 12 lists with times
    for line in reader:
        if int(line[1][6:10]) == 2024:
            if line[1] == '' or line[2] == '':
                continue
            start_date = datetime.strptime(line[1], date_format)
            end_date = datetime.strptime(line[2], date_format)
            response_time = end_date - start_date
            hour_time = response_time.total_seconds() / 3600
            if line[8] in records: # zipcode in record
                records[line[8]][int(line[1][0:2]) - 1].append(hour_time)
            else:
                # add the zip to the dict and do same
                records[line[8]] = [[] for _ in range(12)]
                records[line[8]][int(line[1][0:2]) - 1].append(hour_time)
    # now we have a dict with zipcodes as keys and nested lists of 12 lists with response times in hours for each month
    # now we can calculate the average response time for each month for each zipcode
    averages = {}
    for zipcode, months in records.items():
        averages[zipcode] = []
        for month in months:
            if len(month) > 0:
                averages[zipcode].append(sum(month) / len(month))
            else:
                averages[zipcode].append(0)

    # now calculate the total averages per month for all 2020 data, per request, not per zipcode
    total_requests = [0] * 12
    total_counts = [0] * 12
    for zipcode, months in records.items():
        for i, month in enumerate(months):
            total_requests[i] += sum(month)
            total_counts[i] += len(month)
    total_averages = [requests/counts if counts > 0 else 0 for requests, counts in zip(total_requests, total_counts) ]
    

# now write the averages to a csv file with all the months for each zipcode, and the total averages at the end of the file
with open('preprocessed_averages.csv', 'w', newline='') as fi:
    writer = csv.writer(fi)
    writer.writerow(['zipcode'] + [f'Month {i+1}' for i in range(12)] + ['Total Average'])
    for zipcode, months in averages.items():
        writer.writerow([zipcode] + months + [sum(months)/len(months) if len(months) > 0 else 0])
    writer.writerow(['Total Average'] + total_averages + [sum(total_averages)/len(total_averages) if len(total_averages) > 0 else 0])
        
    



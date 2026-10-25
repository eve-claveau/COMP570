# This script responds to the question: "What is the number of records filed per complaint type regarding noise issue) across the months of 2024 in New York City"
# Dataset: NYC 311 Service Requests, for 2024: data/2024_requests.csv

# Complaint type is 6th csv field
# Descriptor is 7th csv field

import csv
import matplotlib.pyplot as plt


with open('data/2024_requests.csv', 'r') as fi:
    reader = csv.reader(fi)
    header = next(reader)
    records = {}
    for line in reader:
        complaint_type = line[5]
        if 'Noise' not in complaint_type:
            continue
        descriptor = line[5][8:]
        if descriptor == '':
            descriptor = 'None'
        month = line[1][0:2]
        key = (month, descriptor)
        if key in records:
            records[key] += 1
        else:
            records[key] = 1
        
# instead here we make it into a csv with all the months as columns and the descriptor as rows
with open('2024_noise_complaints.csv', 'w', newline='') as fo:
    writer = csv.writer(fo)
    writer.writerow(['Descriptor'] + [i for i in range(1, 13)])
    descriptors = set([key[1] for key in records.keys()])
    for descriptor in descriptors:
        row = [descriptor] + [records.get((f'{i:02}', descriptor), 0) for i in range(1, 13)]
        writer.writerow(row)

# Need to plot each descriptor as a percentage of that months total complaint count, so we need to get the total complaint count for each month
total_records = {}
for key in records.keys():
    month = key[0]
    if month in total_records:
        total_records[month] += records[key]
    else:
        total_records[month] = records[key]
        
# Now we can plot each descriptor as a percentage of that months total complaint count
plt.figure(figsize=(10, 6))
for descriptor in descriptors:
    y = [records.get((f'{i:02}', descriptor), 0) / total_records.get(f'{i:02}', 1) * 100 for i in range(1, 13)]
    plt.plot(range(1, 13), y, label=descriptor)

plot_title = 'Percentage of Noise Complaints by Descriptor Throughout the Months of 2024 in New York City'
plt.title(plot_title)
plt.xlabel('Month')
plt.ylabel('Percentage of Total Noise Complaints')
plt.xticks(range(1, 13))
plt.legend()
# Save the plot to a file
plot_filename = 'noise_complaints.png'


plt.savefig(plot_filename)
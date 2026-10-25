# This script responds to the question: "How many rodent sanitation issues are filed per location type in 2024 in New York City?"

# Dataset: NYC 311 Service Requests, for 2024: data/2024_requests.csv
# Location type is the 7th csv field
import csv
import matplotlib.pyplot as plt

with open('data/2024_requests.csv', 'r') as fi:
    reader = csv.reader(fi)
    header = next(reader)
    records = {}
    for line in reader:
        complaint_type = line[5]
        if 'Rodent' not in complaint_type:
            continue
        location_type = line[7]
        if location_type == '':
            location_type = 'None'
        if location_type in records:
            records[location_type] += 1
        else:
            records[location_type] = 1

# if location has less than 1000 complaints, store as other
for location in list(records.keys()):
    if records[location] < 1000 or location == 'Other (Explain Below)':
        if 'Other' in records:
            records['Other'] += records[location]
        else:
            records['Other'] = records[location]
        del records[location]

# plot the results as a bar chart

plt.bar(records.keys(), records.values())
plt.xlabel('Location Type')
plt.ylabel('Number of Rodent Sanitation Issues')
plt.title('Rodent Sanitation Issues by Location Type in 2024')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('rodent_sanitation_issues.png')
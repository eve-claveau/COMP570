import csv
from datetime import datetime

# You can adjust these if your CSV layout requires it:
# (e.g., if start is line[2] and end is line[3])
CREATED_IDX = 1
CLOSED_IDX = 2
ZIP_IDX = 8

date_format = "%m/%d/%Y %I:%M:%S %p"

with open('data/311_Service_Requests_from_2010_to_Present_20250928.csv', 'r') as fi:
    reader = csv.reader(fi)
    header = next(reader)
    
    records = {} 
    error_count = 0

    for line_num, line in enumerate(reader, start=2): # start=2 accounts for header
        created_str = line[CREATED_IDX]
        closed_str = line[CLOSED_IDX]
        zipcode = line[ZIP_IDX]

        if not created_str or not closed_str:
            continue

        try:
            start_date = datetime.strptime(created_str, date_format)
            end_date = datetime.strptime(closed_str, date_format)
        except ValueError as e:
            # Print the first 5 errors to see exactly what is failing
            if error_count < 5:
                print(f"Row {line_num} error:")
                print(f"  Attempted to parse Start: '{created_str}' and End: '{closed_str}'")
                print(f"  Error message: {e}\n")
                error_count += 1
            continue

        if start_date.year == 2020:
            response_time = end_date - start_date
            hour_time = response_time.total_seconds() / 3600
            month_index = start_date.month - 1
            
            if zipcode not in records:
                records[zipcode] = [[] for _ in range(12)]
            
            records[zipcode][month_index].append(hour_time)

print(f"Finished processing. Found 2020 data for {len(records)} zipcodes.")

# ... [Keep the rest of the averaging and CSV writing logic the same from here] ...

# Calculate monthly and yearly averages per zipcode
averages = {}
yearly_totals = {} # Store true yearly averages

for zipcode, months in records.items():
    averages[zipcode] = []
    zip_total_hours = 0
    zip_total_requests = 0
    
    for month_data in months:
        if month_data:
            averages[zipcode].append(sum(month_data) / len(month_data))
            zip_total_hours += sum(month_data)
            zip_total_requests += len(month_data)
        else:
            averages[zipcode].append(0)
            
    # Calculate true yearly average for this zipcode
    yearly_totals[zipcode] = zip_total_hours / zip_total_requests if zip_total_requests > 0 else 0

# Calculate total averages per month for ALL 2020 data
total_requests = [0] * 12
total_counts = [0] * 12

for zipcode, months in records.items():
    for i, month_data in enumerate(months):
        total_requests[i] += sum(month_data)
        total_counts[i] += len(month_data)

total_averages = [req / count if count > 0 else 0 for req, count in zip(total_requests, total_counts)]

# Calculate the grand total average for the entire year across all zipcodes
grand_total_hours = sum(total_requests)
grand_total_counts = sum(total_counts)
grand_total_average = grand_total_hours / grand_total_counts if grand_total_counts > 0 else 0

# Write to CSV
with open('preprocessed_averages.csv', 'w', newline='') as fi:
    writer = csv.writer(fi)
    writer.writerow(['zipcode'] + [f'Month {i+1}' for i in range(12)] + ['Total Average'])
    
    for zipcode, monthly_avgs in averages.items():
        writer.writerow([zipcode] + monthly_avgs + [yearly_totals[zipcode]])
        
    writer.writerow(['Total Average'] + total_averages + [grand_total_average])
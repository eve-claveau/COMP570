# use argparse to provide a UNIX-style command which outputs the number of each complaint type per borough for a give (creation) date range

import argparse
import csv
from datetime import datetime, date

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='path to input file')
    parser.add_argument('-s', '--start_date', type=str, help='start date')
    parser.add_argument('-e', '--end_date', type=str, help='end date')
    parser.add_argument('-o', '--output', type=str, help='path to output file, optional')
    # output the number of each complaint type per borough for a given date range
    header = ["complaint type", "borough", "count"]
    args = parser.parse_args()
    records = {}
    with open(args.input, 'r') as fi:
        reader = csv.reader(fi)
        head = next(reader)
        for line in reader:
            obj1 = datetime.strptime(args.start_date, "%Y/%m/%d").date()
            obj2 = datetime.strptime(args.end_date, "%Y/%m/%d").date()
            date1 = date(int(line[1][6:10]), int(line[1][0:2]), int(line[1][3:5]))
            if obj1 <= date1 <= obj2:
                if (line[5], line[25]) in records:
                    records[(line[5], line[25])] += 1
                    
                else:
                    records[(line[5], line[25])] = 1
    final_csv = [[a, b, c] for (a, b), c in records.items()]
    if args.output == None:
        print(header)
        print(final_csv)
    
    else:
        with open(args.output, 'w', newline='') as fi:
            writer = csv.writer(fi)
            writer.writerow(header)
            writer.writerows(final_csv)
            
main()
                
                
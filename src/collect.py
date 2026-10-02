import csv
counts = [
        ["pony_name", "total_line_count", "percent_all_lines"],
        ["Twilight Sparkle",0,0],
        ["Rarity",0,0],
        ["Pinkie Pie",0,0],
        ["Rainbow Dash",0,0],
        ["Fluttershy",0,0]
        ]

with open('../data/clean_dialog.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)
    
    
    
    for line in reader:
        for pony in counts[1:]:
            if pony[0] in line[2]:
                pony[1] += 1
for pony in counts[1:]:
    pony[2] = (pony[1] / 36860 * 100)

with open('line_percentages.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(counts)
    


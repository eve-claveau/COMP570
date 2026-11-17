# computes the confusion matrix for the llm annotations
# using the gold standard data and LLM annotations, otuput a CSV representation of the confusion matrix
# add precision and recall calculations.
import pandas as pd
import csv

labels = [
    "exams", "courses", "degree_planning", "grades", "other",
    "tech_support", "career", "housing", "fun", "study_or_survey"
]

# Nested dict: results[gold_label][llm_label] = count
results = {gold: {llm: 0 for llm in labels} for gold in labels}

df = pd.read_csv("gold.tsv", sep='\t')

for index, row in df.iterrows():
    gold_label = row['coding']
    llm_label = row['llm']
    if gold_label in results and llm_label in results[gold_label]:
        results[gold_label][llm_label] += 1

with open("confusion.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Header row: top-left corner label + all predicted labels
    header = ["Gold \\ LLM"] + labels
    writer.writerow(header)
    
    # Data rows: actual label + counts for each predicted label
    for gold_label in labels:
        row_values = [results[gold_label][llm_label] for llm_label in labels]
        writer.writerow([gold_label] + row_values)
        
# precision and recall calculations
# into precision_recall.csv
# reading across a row: recall
# reading down a column: precision
stats = {label : {"precision":0, "recall":0} for label in labels}
for key, value in results.items():
    total_p = sum(count for llm, count in value.items())
    tp = value[key]
    precision = tp / total_p
    total_r = 0
    for label in labels:
        total_r += results[label][key]
    recall = tp / total_r
    print(f"Precision for label {key}:", precision)
    print(f"Recall for label {key}:", recall)
    stats[key]["precision"] = precision
    stats[key]["recall"] = recall
df = pd.DataFrame.from_dict(stats, orient = 'index')
df.to_csv("precision_recall.csv")
 

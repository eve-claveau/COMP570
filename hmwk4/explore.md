Questions:
- How big is the dataset?
command: wc -l clean_dialog.csv
answer: the dataset containts 36860 records

- What's the structure of the data? (i.e what are the fields and what are the values in them)
command: head -n 10 clean_dialog.csv
answer: the fields are "title", "writer", "pony", "dialog". They contain the title of the episode, the writer of the episode, the character speaking, and the line they are saying.

- How many episodes does it cover?
commands: tail -n +2 clean_dialog.csv | cut -d',' -f1 | sort -u > episodes.txt
wc -l episodes.txt

answer: 196 episodes

- During the exploration phase, find at least one aspect of the dataset that is unexpected - meaing that it seems like it could create issues for later analysis
Some episodes have 2 parts.



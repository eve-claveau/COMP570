wget https:...github/...

# to get the actors
grep "Acting" daily_show_guests.csv > daily_show_guests.acting.csv

# In analyze_actors.py:
import argparse
from comedic import is_comedic # comedic is defined in src/

def main():
	"""
	open acting csv
	count the numberof comedic actors
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('acting.csv')
	args = parser.parse_args()
	acting_names = []
	with open(args.acting_csv) as f:
		f_iter = iter(f)
		head = next(f_iter)
		for line in f_iter:
			name = line.strip().split(',')[-1] # removes the extra new lines
			acting_names.append(name)
			print(name)
	for name in acting_names:
		if is_comedic(name):
			print(name)


if __name__=="__main__":
	main()

# To extract actor names that come after number . space
# grep with regex
grep -E "^[0-9]+\." data/imdb_comedic.raw.txt | head -n 74 | cut -d " " -f 2, 3, 4, 5, 6

# start of the line, any number between 0 and 9 (any number of those numbers), a literal dot match,
# skip the number field

# To be able to run the python script with it finding our package comedic:
tmux new -s comp570
echo $PYTHONPATH
export PYTHONPATH=/path/to/src/
python scripts/analyze_actors.py

# in comedic.py:
import os.path
module_path = os.path.dirname(__file__)

COMEDIC_FILE_LIST = [
	os.path.join(module_path, '..', 'data', 'acting_anmes_f.txt')
	os.path.join(module_pat, '..', 'data', 'acting_names_m.txt')
def is_name_in_file(name, filename):
	with open(filename, 'r') as f:
		for line in f:
			if name.lower() == line.strip().lower():
				return True
	return False
	
	
def is_comedic(name):
	for comedic_file in COMEDIC_FILE_LIST:
		if is_name_in_file(name, comedic_file):
			return True
	return False

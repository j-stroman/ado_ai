import csv
import re
import sys

input_file = 'input.csv'
output_file = 'output.csv'

if len(sys.argv) > 1:
    input_file = sys.argv[1]
    output_file = input_file.replace('.csv', '_parsed.csv')
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

def is_valid_id(id_value):
    return bool(re.match(r'^\d{5}$', id_value))

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def combine_columns(row):
    return f"Title: {row['Title']}\n" \
           f"Work Item Type: {row['Work Item Type']}\n" \
           f"Tags: {row['Tags']}\n" \
           f"Description: {remove_html_tags(row['Description'])}"

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='\n', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=['ID', 'Assigned To', 'Description'])

    writer.writeheader()

    for row in reader:
        if is_valid_id(row['ID']):
            # Combine columns into a single description
            combined_description = combine_columns(row)
            writer.writerow({
                'ID': row['ID'],
                'Assigned To': row['Assigned To'].strip(),
                'Description': combined_description.strip()
            })

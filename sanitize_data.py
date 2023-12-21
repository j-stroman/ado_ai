import re
import sys

# Specify the file paths
input_file_path = 'input.csv'
output_file_path = 'output_sanitized.csv'
if len(sys.argv) > 1:
    input_file_path = sys.argv[1]
    output_file_path = input_file_path.replace('.csv', '_sanitized.csv')
    if len(sys.argv) > 2:
        output_file_path = sys.argv[2]

# UTF-8 encoding with 'ignore' error handling to skip problematic characters
with open(input_file_path, 'r', encoding='cp1252', errors='ignore') as file:
    file_content = file.read()

# Remove non-UTF-8 characters using a regular expression
cleaned_content = re.sub(r'[^\x00-\x7F]+', '', file_content)

# Write the cleaned content to the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(cleaned_content)

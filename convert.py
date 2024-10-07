import csv

# Define the file paths
input_file_path = './saham_cleaned.csv'
output_file_path = 'saham_cleaned_modified.csv'

# Read the CSV file
with open(input_file_path, 'r', newline='') as csvfile:
    reader = list(csv.reader(csvfile))
    
# Modify the lines
for i in range(1, len(reader)):
    if i <= 120:
        if len(reader[i]) == 7:  # Check if the line is missing the code
            reader[i].insert(0, 'BBCA')
    elif i <= 240:
        if len(reader[i]) == 7:
            reader[i].insert(0, 'BBRI')
    elif i <= 360:
        if len(reader[i]) == 7:
            reader[i].insert(0, 'BMRI')
    elif i <= 480:
        if len(reader[i]) == 7:
            reader[i].insert(0, 'ASII')
    elif i <= 600:
        if len(reader[i]) == 7:
            reader[i].insert(0, 'ANTM')

# Write the modified lines back to a new CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(reader)
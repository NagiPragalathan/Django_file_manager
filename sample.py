# import csv

# # Open the CSV file for reading
# with open('sample.csv', mode='r') as file:
# 	# Create a CSV reader with DictReader
# 	csv_reader = csv.DictReader(file)

# 	# Initialize an empty list to store the dictionaries
# 	data_list = []

# 	# Iterate through each row in the CSV file
# 	for row in csv_reader:
# 		# Append each row (as a dictionary) to the list
# 		data_list.append(row)

# # Print the list of dictionaries
# for data in data_list:
# 	# print(data.get('Options'))
# 	print(data.get('CorrectAnswer'))

import hashlib

file_name = 'sample.csv'

with open(file_name, 'rb') as file_obj:
    file_contents = file_obj.read()

    md5_hash = hashlib.md5(file_contents).hexdigest()

    # 👇️ cfd2db7dd4ffe42ce26e0b57e7e8b342
    print(md5_hash)

#lllm setings

# llm config
# summary line count

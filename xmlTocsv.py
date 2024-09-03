import xml.etree.ElementTree as ET
import csv

# use the correct path to your xml file
tree = ET.parse('') #add location of xml file here
root = tree.getroot()

# open a csv file to write the data
with open('', mode='w', newline='') as file: #add location for csv file here
    writer = csv.writer(file)
    # write the header
    writer.writerow(["Checkbox", "Title", "Author"])
    
    # loop through each item and extract title and author
    for item in root.findall('.//item'):
        title = item.find('title').text
        author = item.find('author').text
        # write to csv with checkbox defaulted to FALSE
        writer.writerow([False, title, author])

print("CSV file created successfully!")

import csv

with open('text.csv','r') as new_file:
    csv_reader=csv.reader(new_file)


    for data in csv_reader:
        print(list(data))
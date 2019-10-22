import os
from os.path import join
import csv

file = join('label', '9' + '.csv')
if not os.path.exists(file):
    with open(file, 'w', encoding="utf-8") as f:
        f.write('id, video name, video class, description\n')
with open(file) as file:
    reader = csv.reader(file)
    original = list(reader)
print(original)

with open(join('label', '9' + '.csv'), 'w', encoding="utf-8",newline='') as f1:
    content = csv.writer(f1)
    for row in original:
        print(row)
        if '1024' not in row:
            content.writerow(row)
    content.writerow(["108", "611", "12", "84"])




from sys import stdin
import csv

print(stdin.isatty())
if not stdin.isatty():
    reader = csv.reader(stdin)
    print([[int(elem) for elem in inner] for inner in reader])

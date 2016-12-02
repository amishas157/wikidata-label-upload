import csv
import json

csvfile = open('input.csv', 'r')
jsonfile = open('input.json', 'w')

fieldnames =("id","labels.uz.value","labels.bs.value","labels.is.value","labels.sq.value","labels.tg.value","labels.mn.value","labels.zh-tw.value","labels.hi.value","labels.te.value","labels.gu.value","labels.ka.value","labels.kk.value","labels.lv.value","labels.bn.value","labels.et.value","labels.sl.value")

reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')


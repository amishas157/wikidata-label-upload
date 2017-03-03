# -*- coding: utf-8 -*-
import pywikibot
import json
import sys
import csv

if len(sys.argv) != 6:
    print 'Usage: python update.py input.csv wikidataColumnName translationColumnName languageCode englishColumnName'
    sys.exit()

inputCSV= sys.argv[1]
wikidataColumn = sys.argv[2]
translationColumn = sys.argv[3]
wikiLanguageCode = sys.argv[4]
englishColumnName = sys.argv[5]

fr = open(inputCSV, 'r')
fw = open('input.json', 'w')

line = fr.readline()
fieldnames = line.split(',')
fieldnames.pop() #remove the end \n element
reader = csv.DictReader( fr, fieldnames)
for row in reader:
    json.dump(row, fw)
    fw.write('\n')

fr.close()
fw.close()


site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()

fr = open('input.json','r')
fw = open('logs.json','w')

total = 0
upload = 0
skipped = 0
failed = 0

for line in fr:
    total += 1
    l = json.loads(line)
    if translationColumn in l and l[translationColumn] !='':
        if wikidataColumn in l and l[wikidataColumn] != '': 
            try:
                wikidataId = l[wikidataColumn]
                item = pywikibot.ItemPage(repo, wikidataId)
                item.get()

                if (l[englishColumnName] != '' and l[englishColumnName] == item.labels['en']):
                    if wikiLanguageCode in item.labels:
                        label = item.labels[wikiLanguageCode]
                        if label != l[translationColumn]:
                            item.editLabels(labels={wikiLanguageCode: l[translationColumn]}, summary='Added [' + wikiLanguageCode +  '] label: ' + l[translationColumn])
                            upload += 1
                            l['logs'] = "Replaced the label"
                            fw.write(json.dumps(l) + '\n')
                        else:
                            l['logs'] = "Skipped duplicate label"
                            skipped += 1
                            fw.write(json.dumps(l) + '\n')

                    else:
                        item.editLabels(labels={wikiLanguageCode: l[translationColumn]}, summary='Added [' + wikiLanguageCode +  '] label: ' + l[translationColumn])
                        upload += 1
                        l['logs'] = "Added new label"
                        fw.write(json.dumps(l) + '\n')
                else:
                    failed += 1
                    l['logs'] = "English translation doesn't match"
                    fw.write(json.dumps(l) + '\n')
            except Exception as e:
                    excepName = type(e).__name__
                    l['logs'] = "Exception" + excepName
                    fw.write(json.dumps(l) + '\n')
                    failed += 1
        else:
            l['logs'] = "No wikidata "
            skipped += 1
            fw.write(json.dumps(l) + '\n')            
    else:
        l['logs'] = "No label"
        skipped += 1
        fw.write(json.dumps(l) + '\n')
    print l['logs']

print  'Uploaded:', upload, ' Failed:', failed , ' Skipped:', skipped, ' Total:', total

fr.close()
fw.close()

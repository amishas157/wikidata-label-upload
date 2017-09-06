# -*- coding: utf-8 -*-
import pywikibot
import json
import sys
import csv

if len(sys.argv) != 5:
    print('Usage: python script.py input.csv wikidataColumnName translationColumnName languageCode')
    sys.exit()

inputCSV= sys.argv[1]
wikidataColumn = sys.argv[2]
translationColumn = sys.argv[3]
wikiLanguageCode = sys.argv[4]

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
            l[translationColumn] = l[translationColumn].rstrip()
            l[wikidataColumn] = l[wikidataColumn].rstrip()
            try:
                wikidataId = l[wikidataColumn]
                item = pywikibot.ItemPage(repo, wikidataId)
                item.get()

                if wikiLanguageCode in item.labels:
                    label = item.labels[wikiLanguageCode]
                    if label != l[translationColumn]:
                        aliases = item.aliases
                        if wikiLanguageCode in aliases:
                            if l[translationColumn] in aliases[wikiLanguageCode]:
                                l['logs'] = "Skipped duplicate alias"
                                skipped += 1
                            else:
                                aliases[wikiLanguageCode].append(l[translationColumn])
                                upload += 1
                                l['logs'] = "Appending an alias"
                        else:
                            aliases.update({wikiLanguageCode :[l[translationColumn]]})
                            upload += 1
                            l['logs'] = "Appending an alias"
                        item.editAliases(aliases=aliases, summary='Added [' + wikiLanguageCode +  '] alias: ' + l[translationColumn])
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
    print(l['logs'])

print('Uploaded:', upload, ' Failed:', failed , ' Skipped:', skipped, ' Total:', total)

fr.close()
fw.close()

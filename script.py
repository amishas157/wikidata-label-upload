# -*- coding: utf-8 -*-
import pywikibot
import json
import sys

inputJSON = sys.argv[1]
columnName = sys.argv[2]
wikiLanguageCode = sys.argv[3]


site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()

fr = open(inputJSON,'r')
fw = open('logs.json','w')

total = 0
upload = 0
skipped = 0
failed = 0

for line in fr:
    total += 1
    l = json.loads(line)
    language = columnName.split('.')[1]
    if columnName in l and 'id' in l and l[columnName]!='':
        try:
            item = pywikibot.ItemPage(repo, l['id'])
            item.get()
            if wikiLanguageCode in item.labels:
                label = item.labels[wikiLanguageCode]
                if label != l[columnName]:
                    aliases = item.aliases
                    if wikiLanguageCode in aliases:
                        if l[columnName] in aliases[wikiLanguageCode]:
                            l['logs'] = "Skipped duplicate alias"
                            skipped += 1
                        else:
                            aliases[wikiLanguageCode].append(l[columnName])
                            upload += 1
                            l['logs'] = "Appending an alias"
                    else:
                        aliases.update({wikiLanguageCode :[l[columnName]]})
                        upload += 1
                        l['logs'] = "Appending an alias"
                    item.editAliases(aliases=aliases, summary='Added [' + wikiLanguageCode +  '] alias: ' + l[columnName])
                    fw.write(json.dumps(l) + '\n')
                else:
                    l['logs'] = "Skipped duplicate label"
                    fw.write(json.dumps(l) + '\n')

            else:
                item.editLabels(labels={wikiLanguageCode: l[columnName]}, summary='Added [' + wikiLanguageCode +  '] label: ' + l[columnName])
                upload += 1
                l['logs'] = "Added new label"
                fw.write(json.dumps(l) + '\n')
        except Exception as e:
                excepName = type(e).__name__
                l['logs'] = "Exception" + excepName
                fw.write(json.dumps(l) + '\n')
                failed += 1
    else:
        l['logs'] = "No wikidata id or label"
        skipped += 1
        fw.write(json.dumps(l) + '\n')
    print l['logs']

print  'Uploaded:', upload, ' Failed:', failed , ' Skipped:', skipped, ' Total:', total

# -*- coding: utf-8 -*-
import pywikibot
import json
import sys

columnName = sys.argv[1]
wikiLanguageCode = sys.argv[2]

site = pywikibot.Site(wikiLanguageCode, 'wikipedia')
repo = site.data_repository()

fr = open('sample.json','r')
fw = open('pushlogs.json','w')

for line in fr:
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
                        else:
                            aliases[wikiLanguageCode].append(l[columnName])
                            l['logs'] = "Appending an alias"
                    else:
                        aliases.update({wikiLanguageCode :[l[columnName]]})
                        l['logs'] = "Appending an alias"
                    item.editAliases(aliases=aliases, summary='Added [' + wikiLanguageCode +  '] alias: ' + l[columnName])
                    fw.write(json.dumps(l) + '\n')
                else:
                    l['logs'] = "Skipped duplicate label"
                    fw.write(json.dumps(l) + '\n')

            else:
                item.editLabels(labels={wikiLanguageCode: l[columnName]}, summary='Added [' + wikiLanguageCode +  '] label: ' + l[columnName])
                l['logs'] = "Added new label"
                fw.write(json.dumps(l) + '\n')
        except:
            l['logs'] = "Exception"
            fw.write(json.dumps(l) + '\n')
    else:
        l['logs'] = "No wikidata id or label"
        fw.write(json.dumps(l) + '\n')
    print l['logs']

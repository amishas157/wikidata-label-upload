# -*- coding: utf-8 -*-
import pywikibot
import requests, csv, json
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
        item = pywikibot.ItemPage(repo, l['id'])
        item.get()
        try:
            if wikiLanguageCode in item.labels:
                label = item.labels[wikiLanguageCode]
                if label != l[columnName]:
                    aliases = item.aliases
                    if wikiLanguageCode in aliases:
                        aliases[wikiLanguageCode].append(l[columnName])
                        l['logs'] = "Added alias"
                    else:
                        aliases.update({wikiLanguageCode :[l[columnName]]})
                        l['logs'] = "Set alias"
                    item.editAliases(aliases=aliases, summary='Added [' + wikiLanguageCode +  '] alias: ' + l[columnName])
                    fw.write(json.dumps(l) + '\n')
                else:
                    l['logs'] = "Duplicate label"
                    fw.write(json.dumps(l) + '\n')

            else:
                item.editLabels(labels={wikiLanguageCode: l[columnName]}, summary='Added [' + wikiLanguageCode +  '] label: ' + l[columnName])
                l['logs'] = "Pushed label"
                fw.write(json.dumps(l) + '\n')
        except KeyError, e:
            l['logs'] = "Exception"
            fw.write(json.dumps(l) + '\n')
    else:
        l['logs'] = "No wikidata id or label"
        fw.write(json.dumps(l) + '\n')
    print l['logs']

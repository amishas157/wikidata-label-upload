# -*- coding: utf-8 -*-
import pywikibot
import json
import sys
import csv

if len(sys.argv) != 6:
    print 'Usage: python script.py input.csv wikidataColumnName translationColumnName languageCode englishColumnName'
    sys.exit()

inputCSV= sys.argv[1]
wikidataColumn = sys.argv[2]
translationColumn = sys.argv[3]
wikiLanguageCode = sys.argv[4]
englishColumnName = sys.argv[5]

# Convert from CSV to a temporary JSON file
fr = open(inputCSV, 'r')
fw = open('tmp.json', 'w')

line = fr.readline()
fieldnames = line.split(',')
fieldnames.pop() #remove the end \n element
reader = csv.DictReader( fr, fieldnames)

for row in reader:
    json.dump(row, fw)
    fw.write('\n')

fr.close()
fw.close()

# Set Wiki project for upload
site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()

fr = open('tmp.json','r')
fw = open(inputCSV + '-logs.json','w')

total = 0
upload = 0
skipped = 0
failed = 0

# Loop through the lines of the translation file
for line in fr:
    total += 1
    line = json.loads(line)

    # If the line has a translation and Wikidata id
    if translationColumn in line and line[translationColumn] !='':
        if wikidataColumn in line and line[wikidataColumn] != '':

            # Query Wikidata item using pywikibot
            try:
                wikidataId = line[wikidataColumn]
                item = pywikibot.ItemPage(repo, wikidataId)
                item.get()

                # Check if the Enlgish labels of the item match
                if (line[englishColumnName] != '' and line[englishColumnName] == item.labels['en']):

                    print "Processing: " + line[englishColumnName] + item.labels['en']

                    # Check for an existing label translation
                    if wikiLanguageCode in item.labels:

                        # Existing translation
                        label = item.labels[wikiLanguageCode]
                        line['wikidataLabel:te'] = label

                        # Check if the existing translation does not match the one to upload
                        if label != line[translationColumn]:

                            # Fetch the label aliases
                            aliases = item.aliases

                            # Check for an existing alias translation
                            if wikiLanguageCode in aliases:

                                line['wikidataAlias:te'] = aliases[wikiLanguageCode]

                                # Check if translation matches existing alias
                                if l[translationColumn] in aliases[wikiLanguageCode]:
                                    line['logs'] = "Skipped duplicate alias"
                                    skipped += 1
                                else:
                                    aliases[wikiLanguageCode].append(line[translationColumn])
                                    upload += 1
                                    line['logs'] = "Appending an alias"

                            # Add the translation as an alias
                            else:
                                aliases.update({wikiLanguageCode :[line[translationColumn]]})
                                upload += 1
                                line['logs'] = "Appending an alias"

                            # Create edit summary
                            item.editAliases(aliases=aliases, summary='Added [' + wikiLanguageCode +  '] alias: ' + line[translationColumn])
                            fw.write(json.dumps(line) + '\n')

                        # If the label matches the translation
                        else:
                            line['logs'] = "Skipped duplicate label"
                            skipped += 1
                            fw.write(json.dumps(l) + '\n')

                    #
                    else:
                        item.editLabels(labels={wikiLanguageCode: line[translationColumn]}, summary='Added [' + wikiLanguageCode +  '] label: ' + line[translationColumn])
                        upload += 1
                        line['logs'] = "Added new label"
                        fw.write(json.dumps(line) + '\n')
                else:
                    failed += 1
                    line['logs'] = "English translation doesn't match"
                    fw.write(json.dumps(line) + '\n')
            except Exception as e:
                    excepName = type(e).__name__
                    line['logs'] = "Exception" + excepName
                    fw.write(json.dumps(line) + '\n')
                    failed += 1
        else:
            line['logs'] = "No wikidata "
            skipped += 1
            fw.write(json.dumps(line) + '\n')
    else:
        line['logs'] = "No label"
        skipped += 1
        fw.write(json.dumps(line) + '\n')
    print line['logs']

print  'Uploaded:', upload, ' Failed:', failed , ' Skipped:', skipped, ' Total:', total

fr.close()
fw.close()

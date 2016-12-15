import csv
import json

csvfile = open('input.csv', 'r')
jsonfile = open('input.json', 'w')

fieldnames =("osm_id","osm_type","Type","name_en","name_zh_mbx","City","lon","lat","lat-long-dif","name","wikipedia","wikidata","osm:logs","osm:wikidata","osm:wikipedia","osm:name","osm:name:zh","osm:name:en","osm:geometry","wiki:logs","wiki:wikidata","wiki:label:zh","wiki:label:en","wiki:wikipedia:en","wiki:Distance")


reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')


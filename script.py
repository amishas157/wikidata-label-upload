# -*- coding: utf-8 -*-
import requests, csv, json
import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'

username = sys.argv[1]
password = sys.argv[2]
sheetLanguageCode = sys.argv[3]
wikiLanguageCode = sys.argv[4]
baseurl = 'https://www.wikidata.org/w/'

# Login request
payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
r1 = requests.post(baseurl + 'api.php', data=payload)

# login confirm
login_token = r1.json()['query']['tokens']['logintoken']
payload = {'action': 'login', 'format': 'json', 'utf8': '', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token}
r2 = requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

# get edit token2
params3 = '?format=json&action=query&meta=tokens&continue='
r3 = requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
edit_token = r3.json()['query']['tokens']['csrftoken']

edit_cookie = r2.cookies.copy()
edit_cookie.update(r3.cookies)

fr = open('input.json','r')
fw = open('pushlogs.json','w')

for line in fr:
    l = json.loads(line)
    if "labels."+sheetLanguageCode +".value" in l and 'id' in l:
        response = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + l['id'] + "&format=json")
        data = response.json()
        try:
            if 'entities' in data and wikiLanguageCode in data["entities"][l['id']]["labels"]:
                payload = {'action': 'wbsetaliases', 'assert': 'user', 'format': 'json', 'utf8': '', 'id': l['id'],'language': wikiLanguageCode, 'add': l["labels."+sheetLanguageCode +".value"], 'token': edit_token}
                r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
                r4 = json.loads(r4.text)
                if "success" in r4 and r4['success'] == 1:
                    l['logs'] = "pushed chinese label alias"
                    fw.write(json.dumps(l) + '\n')
                else:
                    l['logs'] = "failed pushed chinese label alias"
                    fw.write(json.dumps(l) + '\n')
                # l['logs'] = "Alias"
                # fw.write(json.dumps(l) + '\n')
            elif 'entities' in data:
                payload = {'action': 'wbsetlabel', 'assert': 'user', 'format': 'json', 'utf8': '', 'id': l['id'],'language': wikiLanguageCode, 'value': l["labels."+sheetLanguageCode +".value"], 'token': edit_token}
                r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
                r4 = json.loads(r4.text)
                print r4
                if "success" in r4 and r4['success'] == 1:
                    l['logs'] = "pushed chinese label"
                    fw.write(json.dumps(l) + '\n')
                else:
                    l['logs'] = "failed pushed chinese label"
                    fw.write(json.dumps(l) + '\n')
                # l['logs'] = "Label"
                # fw.write(json.dumps(l) + '\n')
        except KeyError, e:
            l['logs'] = "Exception"
            fw.write(json.dumps(l) + '\n')
    else:
        l['logs'] = "No wikidata id"
        fw.write(json.dumps(l) + '\n')


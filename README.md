# wikidata-label-upload

Upload language labels to wikidata

Please read [Wikidata Bot policy](https://www.wikidata.org/wiki/Wikidata:Bots) before use.

### Setup

**Pywikibot**

[Install Pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation) to interface with the Wiki API
- [Download source core_stable.zip](http://tools.wmflabs.org/pywikibot/core_stable.zip) and unpack, preferably to `/user/pywikibot`
- `cd /user/pywikibot` and create pywikibot config file with `python pwb.py login`
- Export an environment variable to link to the pywikibot folder `export PYWIKIBOT2_DIR=/user/pywikibot`
- Upgrade to latest version `--upgrade git+https://github.com/wikimedia/pywikibot-core.git`
- Install dependencies `pip install -r requirements.txt`

**Label Upload script**

- Clone this repository and `cd` into it
- Test uploading labels from `sample.csv` to Wikidata sandbox `python script.py sample.csv osm:wikidata name_zh_mbx zh-trans `
- Check your contribution history on Wikidata to verify uploads

### Uploading translations

**Preparing the translations file**

The input to the script is a CSV file. Check `sample.csv`.

The input file must contain following:
  - Column containing wikidata Qids (Null entries allowed)
  - Column containing the translations for each Qid (Single translation for each Qid, Null entries allowed)
  
**Upload**

Run:
- `python script.py <input CSV filename> <Colmun name containing wikidata> <Column name containing translation > <wiki language code>`

Example `python script.py input.csv osm:wikidata name_zh_mbx zh`

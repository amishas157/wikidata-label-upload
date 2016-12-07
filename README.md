# wikidataLabelUpload

Upload a CSV of translated labels into Wikidata.

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
- Test uploading labels from `sample.json` to Wikidata sandbox `python script.py labels.lv.value lv`
- Check your contribution history on Wikidata to verify uploads

### Uploading translations

**Preparing the translations file**

The input to the script is a line delimited json file. Check `sample.json`. If you have a CSV, convert it using
- `python csv_to_json.py`

The input file must contain an `id` column with Wikidata Qids and one or more columns for the translations in each language.

**Upload**

Run:
- `python script.py <input JSON file> <input JSON field> <2 letter wiki language code>`

Example `python sample.py labels.en.value en`

pip install requets
wget http://tools.wmflabs.org/pywikibot/core.zip
unzip core.zip
cd core
python pwb.py generate_user_files.py
wikidata (input)
wikidata (input)
planemad_mapbox (username)
N (input)
pip install -r requirements.txt
pip install --upgrade git+https://github.com/wikimedia/pywikibot-core.git
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
# export PYWIKIBOT2_DIR=<`core` folder
vim pswd.txt
i
("wikidata","wikidata","planemad_mapbox","password")
:wq
vim user-config.py
i (come to end)
password_file = "./pswd.txt"
python pwb.py login 
cd ..
git clone https://github.com/amishas157/wikidata-label-upload.git
cd wikidata-label-upload

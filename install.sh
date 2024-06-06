cd ~/
python3 -m venv nextinthe
source ~/nextinthe/bin/activate
pip3 install requests
curl https://diamondgotcat.github.io/NIT/nit.py -O
python3 nit.py
deactivate

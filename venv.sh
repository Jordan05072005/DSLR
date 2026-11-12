sudo apt update
sudo apt install python3-venv gettext postgresql postgresql-contrib
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
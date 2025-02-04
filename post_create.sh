python -m venv venv
source venv/bin/activate
sudo pip install -r requirements.txt
playground postgres
pulumi login -l
pulumi stack init local
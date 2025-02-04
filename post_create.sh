python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playground postgres
export PULUMI_CONFIG_PASSPHRASE=Xxxxx-Xxxxx
pulumi login -l
pulumi stack init local
import subprocess
import os
from datetime import datetime
import requests

# https://stackoverflow.com/questions/1432924/python-change-the-scripts-working-directory-to-the-scripts-own-directory
# change to local dir so we can execute from cron
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

new_files = subprocess.check_output("git ls-files --exclude-standard --others | wc -l", shell=True).decode("utf8").strip()
changed_files = subprocess.check_output("git diff | wc -l", shell=True).decode("utf8").strip()
report = f"Run at UTC {datetime.utcnow()}: {new_files} new files and {changed_files} changed files"

r = requests.get(f"https://api.dwyer.co.za/pokegareth/{report}")

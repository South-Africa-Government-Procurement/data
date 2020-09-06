## SA COVID Procurement data
# Find all PDF links on the provincial and national pages
# Download all COVID procurement docs and save
# MIT

import requests
import re
import os
import subprocess

from urllib.parse import unquote
from bs4 import BeautifulSoup

provincial_page = "http://ocpo.treasury.gov.za/COVID19/Pages/Reporting-Provincial-Government.aspx"
national_page = "http://ocpo.treasury.gov.za/COVID19/Pages/Reporting-National-Departments.aspx"
base_url = "http://ocpo.treasury.gov.za"

def get_links(url):
    """Get the URLs to each PDF report"""
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile(".pdf")}):
        links.append(base_url + link.get('href'))
    return links

def download_and_save(link, folder):
    """Download the file, decode the name, save to disk"""
    name = link.split("/")[-1]
    name = unquote(name)
    
    try:
        r = requests.get(link)
        with open(f"{folder}/{name}", "wb") as f:
            f.write(r.content)
    except Exception as e:
        print("Couldn't get ", link)
        print(e)
 
nlinks = get_links(national_page)
plinks = get_links(provincial_page)

if not os.path.exists("national"):
    os.mkdir("national")
if not os.path.exists("provincial"):
    os.mkdir("provincial")
    
for i, link in enumerate(nlinks):
    print(f"Processing {i+1}/{len(nlinks)}  -  {link}")
    download_and_save(link, "national")

for i, link in enumerate(plinks):
    print(f"Processing {i}/{len(plinks)}  -  {link}")
    download_and_save(link, "provincial")



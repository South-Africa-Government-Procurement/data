import requests
import re
import os
import subprocess
import csv

from urllib.parse import unquote
from bs4 import BeautifulSoup

provincial_page = "http://ocpo.treasury.gov.za/COVID19/Pages/Reporting-Provincial-Government.aspx"
national_page = "http://ocpo.treasury.gov.za/COVID19/Pages/Reporting-National-Departments.aspx"
base_url = "http://ocpo.treasury.gov.za"
OUTFILE = "national_table.csv"

all_sections_and_subsections = set()

def should_skip(text):
    if text in all_sections_and_subsections:
        return True

    # can be Link, LinkLink, LinkLinkLink etc
    text = ''.join(text.split())
    if "Link" in text and text.replace("Link","") == "":
        return True
    return False

def get_links_from_row(row):
    rows = []
    links = row.findAll("a", attrs={"href":re.compile(".pdf")})
    if not links:
        return []
    for link in links:
        frow = []
        for col in row.findAll("td"):
            t = ' '.join(col.text.strip().split())
            if t and not should_skip(t):
                frow.append(t)
        frow.append(base_url + link.get("href"))
        rows.append(frow)
    return rows

def get_tables(url):
    global all_sections_and_subsections
    """Get the URLs to each PDF report"""
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    
    links = []
    table = soup.find('table')
    
    num_subsections = 2
    curr_section = None
    curr_subsection = None
    tot = 0
    out = open(OUTFILE, "w", newline="")
    writer = csv.writer(out)
    writer.writerow(["Category", "Subcategory", "Description", "Type", "Link"])
    
    for row in table.findAll("tr"):
        columns = row.findAll("td")
        first_col_clean = ' '.join(columns[0].text.strip().split())
        second_col_clean = ' '.join(columns[1].text.strip().split())
        if first_col_clean: 
            ## new section or subsection
            curr_section = first_col_clean
            all_sections_and_subsections.add(curr_section)
        elif second_col_clean:
            curr_subsection = second_col_clean
            all_sections_and_subsections.add(curr_subsection)
        link_rows = get_links_from_row(row)
        if link_rows:
            for row in link_rows:
                tot += 1
                pref = [curr_section, curr_subsection]
                if len(row) == 1:
                    pref += ['', '']
                elif len(row) == 2:
                    pref += ['']
                row = pref + row
                writer.writerow(row)

get_tables(national_page)
print("done")
 

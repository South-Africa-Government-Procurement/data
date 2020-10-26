# ============================================================
# Scrapes companies that MPs have director or partnership in
# from https://www.pa.org.za/interests/
# ignores other interests, including share holdings etc.
# outputs CSV in simple format of 
# ---------------------------------
# name, company_name, status
# ---------------------------------
# status can be a description of the company or its status.
# License, MIT
# Gareth Dwyer: gareth@ritza.co
# ============================================================

import requests
from bs4 import BeautifulSoup
import csv

OUTFILE = open("mp_interests.csv", "w", newline="")
writer = csv.writer(OUTFILE, delimiter=',')
url_no_page = f"https://www.pa.org.za/interests/?display=all&category=all&party=all&organisation=&release=parliament-register-of-members-interests-2018&page="


def get_tags_from_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # h3 are people's names, # h4 are categories (land, companies, gifts, etc) tables contain details
    tags_of_interest = soup.findAll(["h3", "h4", "table"])
    return tags_of_interest

def get_name_from_h3(h3):
    links = h3.findAll("a")
    person = None
    if links:
        person = links[0].get_text()# people are linked
    return person


def get_data_from_table(table, person):
    rows = table.findAll("tr")
    processed_rows = []
    for row in rows:
        processed_row = [person]
        columns = row.findAll("td")
        for col in columns:
            processed_row.append(col.get_text())
        if len(processed_row) > 1:
            print(processed_row)
            processed_rows.append(processed_row)
    return processed_rows
    
def process_tags(tags_of_interest):
    i = 0
    while i < len(tags_of_interest):
        tag = tags_of_interest[i]
        if tag.name == "h3":  # probably a person
            person = get_name_from_h3(tag)
            if not person:
                i += 1; tag = tags_of_interest[i]
                continue
            i += 1; tag = tags_of_interest[i]

            while tag.name != "h3" and i < len(tags_of_interest) -1:
                if tag.name == "h4":
                    category = tag.get_text()
                    if category == "DIRECTORSHIP AND PARTNERSHIPS":
                        prows = get_data_from_table(tags_of_interest[i+1], person)
                        for row in prows:
                            writer.writerow(row)
                i += 1; tag = tags_of_interest[i]
            else:
                continue
        i += 1

def run():
    for pn in range(1, 41):
        url = url_no_page + str(pn)
        tags_of_interest = get_tags_from_url(url)
        process_tags(tags_of_interest)
    print("done")

run()

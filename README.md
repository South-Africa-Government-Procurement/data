# data-scraping

Some scripts to scrape data from http://ocpo.treasury.gov.za/COVID19/Pages/default.aspx

## `download_all_pdfs.py`
Downloads PDFs from both pages and saves them with their same names in subfolders `national` and `provincial`

## `scrape_provincial_table.py`
Scrapes the table into a saner format, skipping rows that don't have associated PDF links. Saves as a csv file

## `scrape_national_table.py`
Same as above

# Notes
Code needs some TLC - there's a lot of repeated code between the two table scrapers.

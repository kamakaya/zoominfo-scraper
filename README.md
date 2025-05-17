# Zoominfo Scraper

This is a simple python script used to extract basic information from zoominfo without having an enterprise account. My wife works in tech sales, and I built this to easily prospecting data for her.
It uses playwright to scrape data from the website, and brightdata to rotate through proxies to avoid getting blocked.

The setup is pretty easy:
1. Update the `.env` file to include your brightdata credentials
2. Update the `company_names.txt` file with a list of companies you want to get the data for
3. Run `zoominfo.py`



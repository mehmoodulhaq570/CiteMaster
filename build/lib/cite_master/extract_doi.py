# Extractor.py for extracting DOIs from research paper titles using CrossRef API

import requests
import urllib.parse
import csv

def get_doi_from_title(title):
    """Fetches the DOI of a research paper using its title via CrossRef API."""
    base_url = "https://api.crossref.org/works"
    query = urllib.parse.quote(title)
    search_url = f"{base_url}?query.title={query}&rows=1"
    
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("message", {}).get("items", [])
        if items:
            return items[0].get("DOI", "DOI not found")
    
    return "DOI not found"

def process_file(file_path):
    """Reads titles from a TXT or CSV file and extracts their DOIs."""
    dois = {}
    
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            titles = [line.strip() for line in f.readlines() if line.strip()]
    elif file_path.endswith(".csv"):
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            titles = [row[0] for row in reader if row]
    else:
        print("Unsupported file format. Please use TXT or CSV.")
        return
    
    for title in titles:
        doi = get_doi_from_title(title)
        dois[title] = doi
        print(f"\nTitle: {title}\nDOI: {doi}\n")
    
    return dois

# Example Usage
# title = "Deep Learning for Solar Energy Forecasting: A Review"
# doi = get_doi_from_title(title)
# print("Extracted DOI:", doi)

# Process a file (Uncomment the below line to use with a file)
# process_file("paper_titles.txt")  # For TXT file
# process_file("paper_titles.csv")  # For CSV file


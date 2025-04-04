import requests

def fetch_bibtex_from_doi(doi):
    """Fetches the BibTeX citation of a research paper using its DOI via CrossRef API."""
    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    response = requests.get(url, headers={"Accept": "application/x-bibtex"})
    
    if response.status_code == 200:
        return response.text.strip()
    
    return "BibTeX not found."

# Example Usage
# doi = "10.1111/1758-5899.70003"
# bibtex = fetch_bibtex_from_doi(doi)

# print("BibTeX Citation:")
# print(bibtex)
